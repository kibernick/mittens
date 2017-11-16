# Mittens

![Mittens](background.png "Mittens")

A scalable API service that collects JavaScript errors produced by visitors in multiple websites. Why mittens? Hot objects (like error logs) are best handled by wearing mitts!

* Python 3.6 - using the latest Python
* Flask - a micro-framework for web projects, that is flexible and has a great community
* uwsgi over nginx - a fast and pretty "standard" way of serving (C)Python
* MySQL - simple use case, so nothing too fancy, possibly would add queues 

## Features

* List, create and get error logs – (message) `content` and `meta` (data)
* Access control via `api_key` issued per tenant
* API documentation (Swagger) available at `http://127.0.0.1:5000/api/v1/`
* Filter desired fields in response with the `X-Fields` header

### Developer goodies

* Dependency management using `pip-tools` – quickly update, sync and install dependencies by editing [requirements.in](requirements.in) and doing `make pipup`
* [RESTful interface](mittens/logs/views.py) with `flask-restplus`
* DB migrations with `alembic`
* [Basic token authentication](mittens/auth.py)
* Run [all the tests](tests) with `make test`
* Access an IPython console with the Flask app context with `make console`

### Local development setup (sans Docker)

Make sure that you have [Python 3.6](.python-version) available on your system, and have the MySQL database, table and user setup as per [DevConfig](mittens/settings.py).

* Create a virtualenv inside your pyenv (or equivalent) for Python 3.6, and activate it
* Install all the dependencies: `pip install -r requirements.txt`
* Run the migrations: `FLASK_APP=local_api.py FLASK_DEBUG=1 flask db upgrade`
* Run the app server: `make api`

## TODO:

* Dockerfile
* Rate limiting on Nginx level, using `limit_req_zone` and `$http_x_forwarded_for`, for example:
```
limit_req_zone  $http_x_forwarded_for zone=my_zone:16m rate=1r/s;

server {

    location /my-api {

        limit_req zone=my_zone burst=10;

```
* Kubernetes (minikube) deployment

## Improvements

* Health-check endpoints
* Configuration management for deployment
* Don't use Integer as ID
* Pagination
* JWT auth tokens
* Admin panel with the ability to search over error log content and metadata
