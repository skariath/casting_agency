Casting Agency
Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

Hosted on heroku. https://sk-udacity-capstone.herokuapp.com/

Motivation
This is the capstone project for the Udacity Full Stack Nano Degree.

Dependencies
All dependencies are listed in the requirements.txt file. They can be installed by running pip3 install -r requirements.txt.

Authentication
The API has three registered users:

Assistant
email: assistant@casting.com
password: Assistant1
Director
email: director@casting.com
password: Director1
Producer
email: producer@casting.com
password: Producer1
The Auth0 domain and api audience can be found in setup.sh.

Endpoints
The endpoints are as follows:

GET '/movies' This endpoint fetches all the movies in the database and displays them as json

GET '/actors' This endpoint fetches all the actors in the databse and displays them as json

POST '/movies/create' This endpoint will create a new movie in the database based on the json that is in the body of the request

POST '/actors/create' This endpoint will create a new actor in the database based on the json that is in the body of the request

DELETE '/movies/delete/int:movie_id' This endpoint will delete the movie that corresponds to the movie ID that is passed into the url

DELETE '/actors/delete/int:actor_id' This endpoint will delete the actor that corresponds to the actor ID that is passed into the url

PATCH '/actors/patch/int:actor_id' This endpoint will modify the actor that corresponds to the actor ID that is passed into the url based on the json that is passed into the body of the request

PATCH '/movies/patch/int:movie_id' This endpoint will modify the movie that corresponds to the movie ID that is passed into the url based on the json that is passed into the body of the request

Tests
To run the tests, run python3 test_app.py.