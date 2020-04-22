# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

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

## Tasks

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
    - in API Settings:
        - Enable RBAC
        - Enable Add Permissions in the Access Token
5. Create new API permissions:
    - `get:drinks-detail`
    - `post:drinks`
    - `patch:drinks`
    - `delete:drinks`
6. Create new roles for:
    - Barista -> JWT = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA2Mjg2NDU0NTQ3MzQxMDE2MzEyIiwiYXVkIjpbIkNvZmZlZSIsImh0dHBzOi8vcGFuY2hvYi5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg3NTU3NjI0LCJleHAiOjE1ODc1NjQ4MjQsImF6cCI6InlZQjNBczZhT2M0dDcycFFWQXM2a2dqRjRMWGdKMUZhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImdldDpkcmlua3MtZGV0YWlsIl19.Gk25GZhYQexb1mIXaRNGO--qZiBVbSaGOzQHxuAXQq4SlEzMCCtXRj8szX2oy_l-hRourRKrZsED8obi1lR172Dass56bAcP7cZ-3rdxK3v3kZOpDuTL6SofvPPtudS7Y28whzRc1FfYhfXv-8enSk_hwlwrgvdAVo4W7mY_q44wiHrxxw7JVVbNMuWbTHGw3CqUvXEJ-Ll7qozV2htR5caNszJGGgU9tQp0F7QjYk6hj08ypFOVZ7XGJ1mlfWiXBW-0Dsh4AKU0cAUgzVKzcTKtD4eCLx7ojObkGC0eYhrX--gg9c88yS3IBzxFegKFcWMxAGSF8tE1RQNnyN6s9A
        - can `get:drinks-detail`
    - Manager -> JWT = eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkFkMFVJY2NsTU1HWnF5a2hRSm5zcSJ9.eyJpc3MiOiJodHRwczovL3BhbmNob2IuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA2Mjg2NDU0NTQ3MzQxMDE2MzEyIiwiYXVkIjpbIkNvZmZlZSIsImh0dHBzOi8vcGFuY2hvYi5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTg3NTU3NzUwLCJleHAiOjE1ODc1NjQ5NTAsImF6cCI6InlZQjNBczZhT2M0dDcycFFWQXM2a2dqRjRMWGdKMUZhIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTpkcmlua3MiLCJnZXQ6ZHJpbmtzLWRldGFpbCIsInBhdGNoOmRyaW5rcyIsInBvc3Q6ZHJpbmtzIl19.CV35njGK392cEAT4R__pEpDDcfWm5-f2FxUqw8ic9LGKDFlGOo0DrD5SNotyf4h91WCzDiJqmM1T8U2MScb5Qq5Tk-s-ihNr9m-QAr48quzZFyct2Hmaft7Pxy5xdt-RQ0nt7zF-VVAiuHwwpoIP18jGIyYP5_ajs5gPGIeBSIPF6dB_jpcSHlVsop_x-6mBtE2h46Y6XK7QXJwTzyIE0-OQVPMG-6styfjIR324aHBS-8-Pf3oH0yJzdo_HC3owQsOIIsSRayFeFvluX3tG8PTxCbTy8OIgKcHpboTuwo1UrfBEssUUJ4LXa-8A9wPnKX04TUVLibMys25DYbMP5Q
        - can perform all actions
7. Test your endpoints with [Postman](https://getpostman.com). 
    - Register 2 users - assign the Barista role to one and Manager role to the other.
    - Sign into each account and make note of the JWT.
    - Import the postman collection `./starter_code/backend/udacity-fsnd-udaspicelatte.postman_collection.json`
    - Right-clicking the collection folder for barista and manager, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
    - Run the collection and correct any errors.
    - Export the collection overwriting the one we've included so that we have your proper JWTs during review!

### Implement The Server

There are `@TODO` comments throughout the `./backend/src`. We recommend tackling the files in order and from top to bottom:

1. `./src/auth/auth.py`
2. `./src/api.py`
