# Catalogue Project
Create a Django app that implements a catalogue of music.

## Getting started
### Set up a virtualenv

```shell
$ python3 -m venv .venv
$ source venv/bin/activate
```

### Install dependencies

```shell
$ pip install -r requirements.txt
```

### Initialize the development database

```shell
$ python manage.py migrate
$ python manage.py loaddata initial_data
```

### Create superuser to access django admin

```shell
$ python manage.py createsuperuser
```

### Run the server

```shell
$ python manage.py runserver
```

Log into the Django admin:

[admin/](http://localhost:8000/admin/)

Browse the REST API at:

[api/v1/](http://localhost:8000/api/v1/)

### Run the default test case

```shell
$ python manage.py test
```