# MarketInfo
Get your daily market updates from Bombay stock exchange

project hosted on [65.1.169.59](http://65.1.169.59/)

### INSTALLING AND RUNNING ###

```
git clone https://github.com/nithinkash/MarketInfo.git
```

This whole project is developed using django, uses jinja html template as a frontend and redis as a datastore.

```
pip install -r requirements.txt
```
This installs all the requirements for the project using pip (python package installer) 

execute this set of commands to create database tables and run the project
```
python manage.py migrate
python manage.py makemigrations
python manage.py runserver
```
If everything is done right this should start the server in localhost on port 8000 (default port)
But for this project we need another command which needs to be executed. 
```
python manage.py qcluster
```
Probably wondering why is this used for!!, I'll get to it after some time.

### PROJECT OVERVIEW ###

Main aim of this project is to create a django app to fetch the BhavFile from the BSE( Bombay stock exchnage) everyday at 6:00 PM IST, store it in redis and 
present it in a user friendly way. Main components of the app that I've used are

* Django
* DjangoQ
* Redis

#### DJango ####
As many of you may know is the light weight web framework fully written in python which handles and server's the web request.

#### DjangoQ ####
Python library that can be used for Async tasks handling and scheduling. Very light weight and easy to use library which runs in the background to serve scheduling
tasks like triggering a function call at some time of the day. Which exactly is the functionality we want here.
**python manage.py qcluster** was used to start the q_cluster which handles this async task.
Good thing about djangoQ is we can schedule the task through admin console with GUI at
```
/admin/django_q
```
#### Redis ####
Used to store the stock data which is in the CSV format as a list values, and can be retrieved very easily.


### HOSTING ###

I've hosted this on aws EC2 instance using WSGI and Apache server. [This](https://medium.com/saarthi-ai/ec2apachedjango-838e3f6014ab) medium article can give you a good
insight on deploying django apps using WSGI + apache.

One thing I've done to run q_cluster on cloud is to configure [supervisor](https://www.digitalocean.com/community/tutorials/how-to-install-and-manage-supervisor-on-ubuntu-and-debian-vps)
Supervisor's are used to run multiple processes and commands it can startup automatically after a reboot.
