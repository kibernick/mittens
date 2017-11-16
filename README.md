# Mittens

![Mittens](background.png "Mittens")

A scalable API service that collects JavaScript errors produced by visitors in multiple websites. Why mittens? Hot objects (like error logs) are best handled by wearing mitts! 

## Features

* List, create and get error logs – (message) `content` and `meta` (data)
* Access control via `api_key` issued per tenant
* API documentation (Swagger) available at `http://127.0.0.1:5000/api/v1/`
* Filter desired fields in response with the `X-Fields` header

### Developer goodies

* Dependency management using `pip-tools`
* RESTful interface with `flask-restplus`
* DB migrations with `alembic`
* Basic token authentication
* `make test`

## TODO:

* Dockerfile
* Rate limiting on Nginx level

## Improvements

* Health-check endpoints
* Configuration management for deployment
* Don't use Integer as ID
* Pagination
* JWT auth tokens
* Admin panel with search over error log content and metadata.
