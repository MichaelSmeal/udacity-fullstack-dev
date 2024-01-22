# Coffee Shop Backend

## Getting Started

This is a Coffee Shop application. It has the options to display drinks, add, edit, or delete depending on roles.

Roles and Permissions:

- Manager
-- get:drinks
-- get:drinks-detail
-- post:drinks
-- patch:drinks
-- delete:drinks
- Barista
-- get:drinks
-- get:drinks-detail

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Errors

Errors are handled as json object messages

The api will return the following errors:

- 400: Return a bad request message
- 404: Return a not found message
- 422: Return an unprocessable message

## Resource Endpoint Library

### GET /drinks

#### General

- Return a list of all drinks short version
- No permissions required
- Drinks must be returned as object

#### Return sample

```shell
{
    "success": True,
    "drinks": [
        {
            "title": "Water",
            "recipe": [{
                "color": 1,
                "parts": "water",
            }]
        }
    ]
}
```

### GET /drinks-detail

#### General

- Returns a list of all drinks
- Require 'get:drinks-detail' permission
- Roles
- - Manager
- - Barista
- Drinks must be formated as object

#### Return sample

```shell
{
    "success": True,
    "drinks": [
        {
            "title": "Water",
            "recipe": [{
                "name": "Water",
                "color": 1,
                "parts": "water",
            }]
        }
    ]
}
```

### POST /drinks

#### General

- Post drink
- Require 'post:drinks' permission
- Roles
- - Manager
- When the add form is submitted with all of it"s fields filled out, a drink will be successfully submitted
- No data will be returned
- The form will clear and the drink will be added to the drink menu
- No data will be returned to the visual screen

#### Return sample

```shell
{
    "success": True,
    "drinks": [
        {
            "title": "Water",
            "recipe": [{
                "name": "Water",
                "color": 1,
                "parts": "water",
            }]
        }
    ]
}
```

### PATCH /drinks/1

#### General

- Patch drink
- Require 'patch:drinks' permission
- Roles
- - Manager
- The form will clear and the drink will be updated
- No data will be returned to the visual screen

#### Return sample

```shell
{
    "success": True,
    "drinks": [
        {
            "title": "Water",
            "recipe": [{
                "name": "Water",
                "color": 1,
                "parts": "water",
            }]
        }
    ]
}
```

### DELETE /drinks/1

#### General
- Delete drink
- Require 'delete:drinks' permission
- Roles
- - Manager
- The drink will be deleted from drink menu
- No data will be returned to the visual screen

#### Return sample

```shell
{
    "success": True,
    "drinks": id
}
```
