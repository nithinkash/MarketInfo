from django.shortcuts import render
import time
from datetime import date
import zipfile, redis, logging
import pandas as pd
from urllib.request import Request, urlopen
from six import BytesIO

log = logging.getLogger(__name__)
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

def fetch_api():
    # instead of first getting the whole page and then extracting the URL using beutifulsoap i figured out that BSE always stores the file in EQ030321_CSV.ZIP format
    # so I've used the date to get current date and form the filename that can be requested directly.
    today_date = str(date.today()).split('-')[::-1]
    day, month = today_date[:2]
    url = 'https://www.bseindia.com/download/BhavCopy/Equity/EQ{0}{1}21_CSV.ZIP'.format(day,month)
    req=Request(url)
    req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64)')
    with urlopen(req) as zipresp:
        with zipfile.ZipFile(BytesIO(zipresp.read())) as zfile:
            zfile.extractall()

    time.sleep(2)
    df = pd.read_csv('EQ{0}{1}21.CSV'.format(day,month))
    df = df[['SC_CODE', 'SC_NAME', 'OPEN', 'HIGH', 'LOW', 'CLOSE']].copy()

    for index, row in df.iterrows():
        # Save every row in data frame with SC_CODE as key.
        r.hmset(row['SC_CODE'], row.to_dict())
        # Save SC_CODE using SC_NAME prefixed with equity as key for searching.
        r.set("equity:" + row['SC_NAME'], row['SC_CODE'])


def index(request):
    result = []
    for key in r.scan_iter("equity:*"):
        code = r.get(key)
        result.append(r.hgetall(code).copy())
    result = result[0:10]
    context={'result':result}
    return render(request, "search.html", {'search':result})

def search(request):
    searchItems = []
    query = request.GET.get('query', '')
    query=query.upper()
    for key in r.scan_iter("equity:" + query + "*"):
        code = r.get(key)
        searchItems.append(r.hgetall(code).copy())
    return render(request, "search.html",{'search':searchItems})
