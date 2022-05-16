# golden-memories-back
Flask Back-end for application Golden Memories

Using Flask to build a Restful API Server with Swagger document.

Integration with Gunicorn, Flask-smorest, Flask-Cors, Flask-Mongoengine and Flask-JWT-Extended extensions.

### Extension:
- Gunicorn: [Gunicorn](Gunicorn)

- Restful: [Flask-smorest](https://flask-smorest.readthedocs.io/en/latest/)

- Document-Object Mapper: [Flask-Mongoengine](http://docs.mongoengine.org/projects/flask-mongoengine/en/latest/)

- Flask-JWT-Extended: [Flask-JWT-Extended](https://flask-jwt-extended.readthedocs.io/en/stable/)



## Installation

Install with pip:

```
$ pip install -r requirements.txt
```

## Flask Application Structure 
```
.
|──────project/
| |────api/
| | |────auth.py
| | |────photo.py
| | |────user.py
| |────models/
| |────schemas/
| |────services/
| |────__init__.py
| |────app.py
| |────config.py
| |────extension.py
| |────util.py
|──────run.sh
|──────tests/

```


## Flask Configuration

#### The project configurations must be on the config.py at the `BaseConfig` class
#### You must supply your AWS S3 auth tokens

```
S3_ACCESS_KEY = ''
S3_SECRET_KEY = ''
```

##Flask settings for production
DEBUG = False 
TESTING = False
USE_RELOADER = False

##RAPIDOC api
The RAPIDOC api documentation URL is `/api/doc`

 
## Run Gunicorn
### Run flask for development
```
$ bash run.sh
```
In this project, Default port is `5000`

Rapidoc document page:  `http://127.0.0.1:5000/api/doc`

### Run flask for production

** Set development config in `config.py` **
** Run with gunicorn **

```
$ bash run.sh

```


## Api test with PyTest
Basic api test
```
$ python -m pytest tests/test_api.py::TestApi
```

## Changelog

- Version 0.1 : basic REST back-end project  
