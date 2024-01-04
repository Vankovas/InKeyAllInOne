# InKeyDev
In this project there are 3 main apps - ``InKeyUser``, which is responsible 
for the user side of the story, the ``InKeyCreator``, which focuses on music 
creators and the ``InKeyAccountManagement`` which focuses on authentication.
Beside this 3 apps, there is teh ``Core`` folder which includes all of the base
Django settings.

# Live URL
https://inkey-backend.herokuapp.com/users/


# API Documentation
You can find documentation at ``/doc``<br>
Live link:
``https://inkey-backend.herokuapp.com/doc/``

# Set up
Make sure you have python 3.6 and pip installed. You can skip step 1., 2.
and 3. if you are using PyCharm or some IDE which creates virtual environment
for you.
1. ``pip install virtualenv``
1. ``virtualenv venv``
1. ``source venv/Scripts/activate`` on Windows, or ``source venv/bin/activate`` on Ubuntu
1. ``pip instal -r reqirements.txt``
1. ``copy .env.example .env`` on Windows, or ``cp .env.example .env`` on Ubuntu
1. ``manage.py migrate``
1. ``manage.py runserver``

# How to develop

### Create user
``manage.py createuser``


### Create admin
``manage.py createsuperuser``

## Tests
### Create Test
There is no command to create a test, so just find one and copy paste it,
then just change the names and stuff. You can find an example test in 
``./account_management/tests/test_user_view.py``


### Run Tests
In order to run all tests, just run
```shell script
manage.py test
```

For code coverage:
```shell script
coverage run --source='.' --omit='./venv/*' manage.py test
coverage report
```
For a nicer view, you can even run 
```shell script
coverage run --source='.' --omit='./venv/*' manage.py test
coverage html
```
which creates an html page with reports for each file


### Run Specific Tests
If you want to run a specific app's tests, run:
```shell script
manage.py test {appname}
```
where {appname} is the name of your app. You can even specify
which file to run with
```shell script
manage.py test {appname}.tests.{filename}
```
where {filename} is the filename you want WITHOUT .py


## Migrations


### Make Migrations
In Django, if you edit the the Model classes, it basically needs to
change the database. Therefore, if you change Model classes, run:
```shell script
manage.py makemigrations
```


### Push Migrations
This will create all the SQL code and everything needed to change the 
database according to your changes. HOWEVER IT WON'T PUSH IT.
When you are sure your changes are good and ready for the app, just
push them with this command:
```shell script
manage.py migrate
```


### Other stuff with migrations
You can rollback previous migrations, edit data in the database and other
stuff (usually migrations only change the structure of the DB and not 
the data). Look em up here:
* https://docs.djangoproject.com/en/3.0/topics/migrations/
* https://docs.djangoproject.com/en/3.0/ref/migration-operations/

# Useful stuff
* https://docs.djangoproject.com/en/3.0/intro/ - Django tutorial, really useful
* https://django-rest-framework-simplejwt.readthedocs.io/en/latest/index.html - the jwt stuff we use
* https://www.django-rest-framework.org/ - Django REST Framework (drf for short)
