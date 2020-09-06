# Capstone Project - Casting Agency
### Udacity Full Stack Nano Degree 
Content
Motivation
Start Project locally
API Documentation
Authentification

## About
Casting Agency application models a company that is responsible for producing movies as well as managing and assigning actors to those movies.

## Motivations & Covered Topics
This is the capstone project for the Udacity Full Stack Nano Degree course. It covers all technical topics completed as a part of the course

1. Database modeling with [postgres](https://www.postgresql.org/docs/) & [sqlalchemy](https://docs.sqlalchemy.org/en/13/). Covered in [models.py](models.py)
2. CRUD Operations on database with [Flask](https://flask.palletsprojects.com/en/1.1.x/). Covered in [app.py](app.py)
3. Automated testing with Unittest. Covered in [test_app.py](test_app.py)
4. Authorization & Role based Authentification with [Auth0](https://auth0.com/). Covered in [auth.py](auth.py)
5. Deployment on [Heroku](https://devcenter.heroku.com/)

## Start Project locally
Make sure you cd into the correct folder (with all app files) before following the setup steps. Also, you need the latest version of Python 3 and postgres installed on your machine.

To start and run the local development server,

1. Initialize and activate a virtualenv:

`$ virtualenv --no-site-packages env_castingagency`

`$ source env_castingagency/scripts/activate`

2. Install the dependencies:

`$ pip install -r requirements.txt`
This will install all of the required packages we selected within the `requirements.txt` file.

Running this project locally means that it can´t access Herokus env variables. To fix this, you need to edit a few informations in [setup.sh](setup.sh), so it can correctly connect to a local database

3. Change database config so it can connect to your local postgres database
Open [setup.sh](setup.sh) with your editor of choice.
Set database url as:

`DATABASE_URL="postgres://<username>:<password>@<hostname>:<port>/<databasename>"`

Just change username, password and port to whatever you choose while installing postgres.
hostname is typically localhost and port is typically 5432.
databasename is the name of the database you created.

4. Setup Auth0 If you only want to test the API, you can simply take the existing bearer tokens in [setup.sh](setup.sh). Please note that the tokens are valid only for 24 hours.
If you chose to set up Auth0, modify the following with the new bearer tokens: 
`ASSISTANT_TOKEN`, `DIRECTOR_TOKEN`, `PRODUCER_TOKEN`

Please scroll down to read Set Up Authentication to follow steps to set up Auth0

5. Run the development server:

`$ python app.py`

To execute tests, run

`$ python test_app.py`
If you choose to run all tests, it should give this response if everything went fine:

```
$ python test_app.py
.........................
----------------------------------------------------------------------
Ran 24 tests in <x>s

OK
```

## API Documentation

Here you can find all existing endpoints, which methods can be used, how to work with them & example responses you´ll get.

Additionally, common pitfalls & error messages are explained, if applicable.

### Base URL
https://sk-udacity-capstone.herokuapp.com


### Available Endpoints
#### 1. GET /actors
Get a list of all actors.

`$ curl -X GET https://sk-udacity-capstone.herokuapp.com/actors`

Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
Request Arguments:None
Request Headers: None
Requires permission: read:actors
Returns:
List of dict of actors with following fields:
integer id
string name
string gender
boolean success

##### Example response
```
{
  "actors": [
    {
      "gender": "Male",
      "id": 1,
      "name": "Brad Pitt"
    }
  ],
  "success": true
}
```
#### 2. POST /actors
Insert new actor into database.

`$ curl -X POST https://sk-udacity-capstone.herokuapp.com/actors`

Request Arguments: None
Request Headers: (application/json) 1. string name (required) 2. string gender
Requires permission: write:actors
Returns:
name of the newly created actor
boolean success

##### Example response
```
{
    "actor": "Brad Pitt"
    "success": true
}
```

##### Errors
If you try to create a new actor without a required field for ex; name, it will throw a 400 error:

`$ curl -X POST https://sk-udacity-capstone.herokuapp.com/actors`
will return

```
{
  "error": 400,
  "success": false
  "message": "bad request"
}
```

### 3. PATCH /actors
Edit an existing Actor

`$ curl -X PATCH https://sk-udacity-capstone.herokuapp.com/actors/1`
Request Arguments: integer id from actor you want to update
Request Headers: (application/json) 1. string name 2. string gender
Requires permission: update:actors
Returns:
integer id from updated actor
boolean success
List of dict of actors with following fields:
integer id
string name
string gender

##### Example response
```
{
    "actor": [
        {
            "gender": "Male",
            "id": 1,
            "name": "George Clooney"
        }
    ],
    "success": true
}
```

##### Errors
If you try to update an actor with an invalid id it will throw a 404 error:

`$ curl -X PATCH https://sk-udacity-capstone.herokuapp.com/actors/2125`
will return
```
{
  "error": 404,
  "message": "not found",
  "success": false
}
```

#### 4. DELETE /actors
Delete an existing Actor

`$ curl -X DELETE https://sk-udacity-capstone.herokuapp.com/actors/1`
Request Arguments: integer id from actor you want to delete
Request Headers: None
Requires permission: delete:actors
Returns:
integer id from deleted actor
boolean success

##### Example response
```
{
    "delete" : 1
    "success": true
}
```

##### Errors
If you try to delete actor with an invalid id, it will throw an 404 error:

`$ curl -X DELETE https://sk-udacity-capstone.herokuapp.com/actors/2125`
will return
```
{
  "error": 404,
  "message": "not found",
  "success": false
}
```

#### 5. GET /movies
Get a list of all movies.

`$ curl -X GET https://sk-udacity-capstone.herokuapp.com/movies`

Fetches a list of dictionaries of examples in which the keys are the ids with all available fields
Request Arguments: None
Request Headers: None
Requires permission: read:movies
Returns:
List of dict of movies with following fields:
integer id
string name
date release_date
boolean success

##### Example response
```
{
  "movies": [
    {
      "id": 1,
      "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
      "title": "Fight Club"
    }
  ],
  "success": true
}
```

#### 6. POST /movies
Insert a new Movie into database.

`$ curl -X POST https://sk-udacity-capstone.herokuapp.com/movies`
Request Arguments: None
Request Headers: (application/json) 1. string title (required) 2. date release_date (required)
Requires permission: write:movies
Returns:
integer id from newly created movie
boolean success

##### Example response
```
{
    "id": 1
    "success": true
}
```
##### Errors
If you try to create a new movie without a required field for ex; title, it will throw a 400 error:

`$ curl -X POST https://sk-udacity-capstone.herokuapp.com/movies`
will return
```
{
  "error": 400,
  "message": "bad request",
  "success": false
}
```

#### 7. PATCH /movies
Edit an existing Movie

`$ curl -X PATCH https://sk-udacity-capstone.herokuapp.com/movies/1`
Request Arguments: integer id from movie you want to update
Request Headers: (application/json) 1. string title 2. date release_date
Requires permission: update:movies
Returns:
integer id from updated movie
boolean success
List of dict of movies with following fields:
integer id
string title
date release_date

##### Example response
```
{
    "created": 1,
    "movie": [
        {
            "id": 1,
            "release_date": "Sun, 16 Feb 2020 00:00:00 GMT",
            "title": "Sparta"
        }
    ],
    "success": true
}
```

##### Errors
If you try to update an movie with an invalid id it will throw an 404 error:

`$ curl -X PATCH https://artist-capstone-fsnd-matthew.herokuapp.com/movies/2125`
will return
```
{
  "error": 404,
  "message": "not found",
  "success": false
}
```

#### 8. DELETE /movies
Delete an existing movie

`$ curl -X DELETE https://sk-udacity-capstone.herokuapp.com/movies/1`
Request Arguments: integer id from movie you want to delete
Request Headers: None
Requires permission: delete:movies
Returns:
integer id from deleted movie
boolean success

##### Example response
```
{
    "delete": 1,
    "success": true
}
```

##### Errors
If you try to delete movie with an invalid id, it will throw a 404 error:

`$ curl -X DELETE https://sk-udacity-capstone.herokuapp.com/movies/2125`
will return
```
{
  "error": 404,
  "message": "not found",
  "success": false
}
```
### Existing Roles
Three roles with distinct permission sets have been already setup

1. Casting Assistant:
`GET /actors (read:actors)`: Can see all actors
`GET /movies (read:movies)`: Can see all movies

2. Casting Director (everything from Casting Assistant plus)
`POST /actors (write:actors)`: Can create new Actors
`PATCH /actors (update:actors)`: Can edit existing Actors
`DELETE /actors (delete:actors)`: Can remove existing Actors from database
`PATCH /movies (update:movies)`: Can edit existing Movies

3. Exectutive Dircector (everything from Casting Director plus)
`POST /movies (write:movies)`: Can create new Movies
`DELETE /movies (delete:movies)`: Can remove existing Motives from database

In your API Calls, add them as Header, with Authorization as key and the Bearer token as value. Don´t forget to also prepend Bearer to the token (seperated by space).

For example: (Bearer token for Executive Director)
```
{
    "Authorization": "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InYxaU54YnF6dDRFY0o0VDh6Zkw1RCJ9.eyJpc3MiOiJodHRwczovL2Rldi0zNDV1N3Itdy51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NWY1MzNjZTIxNDYxNjEwMDZkMjYwNjY4IiwiYXVkIjoiY2FzdGluZ19hZ2VuY3kiLCJpYXQiOjE1OTkzODIxOTAsImV4cCI6MTU5OTQ2ODU5MCwiYXpwIjoiT2J5Wkp5R1A2QTZXMGRLTVJzbFNSYWoxcElTbXBMQ3QiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwid3JpdGU6YWN0b3JzIiwid3JpdGU6bW92aWVzIl19.XYBTTX2XMynZkg6Wu50p_zFOiCRtPcO1LUECX2F7BbMT_l8BZvGDrneZM129VUc2RB_w7TZHITlC83podoAJ8zY30uhJxgqGTS--Ef0RjQe7hWv79SVFnQ_gxLDkVMieiu2zdXFeO__qcLvEyOMNoIHL7LkAnSN5bbX6UBbuvK4-xD3e1uUdTJqyTwtg50ZmsV_qi78zFRSatQFu0s8SSBmt8UKJpX6OcKJOyC_fl5i7E1rY-x_E54-0pIUtJRPI_6GEKnHYbW3JxwyH_Bbqdp3Tl3FOZt_N998rOqH0iwIaJ4JFwIcjCXisz4pntNVkmMu0_Np4RvmcnpiSUJ6LFQ"
}
```

### Set Up Authentication
All API Endpoints are decorated with Auth0 permissions. To use the project locally, you need to config Auth0 accordingly

#### Auth0 set up for local use

##### Create an App & API
1. Login to https://manage.auth0.com/
2. Click on Applications Tab
3. Create Application
4. Give a name for ex; capstone_castingagency and select "Single Page Web Application"
5. Go to Settings and find domain. Copy & paste it into [setup.sh](setup.sh) => `AUTH0_DOMAIN` (i.e. replace `dev-345u7r-w.us.auth0.com`)
6. Click on API Tab
7. Create a new API:
    Name: `casting_agency`
    Identifier: `casting_agency`
    Keep Algorithm as it is
8. Go to Settings and find `Identifier`. Copy & paste it into [setup.sh](setup.sh) => `API_AUDIENCE` (i.e. replace `casting_agency`)

##### Create Roles & Permissions
1. `Enable RBAC` in your API (API => Click on your API Name => Settings = Enable RBAC => Save)
2. Check the button `Add Permissions` in the `Access Token`.
3. In the API tab, Click on `Permissions`.
4. Create & assign all needed permissions accordingly.
5. After you created all permissions this app needs, create a new Role under `Users and Roles` => `Roles` => `Create Roles`. 
6. Give it a descriptive name like `Casting Assistant`.
7. Under `Permissions`, assign all permissions you want this role to have.
8. Create additional `Roles` and assign `Permissions` as needed

##### Auth0 to use existing API
Temporary bearer tokens for all 3 roles have been included in the [setup.sh](setup.sh) file.
