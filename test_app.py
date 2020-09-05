import unittest
import os
from app import app, create_app
from models import setup_db, db, Movies, Actors
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))

database_path = os.environ['TEST_DATABASE_URL']

assistant_token = os.getenv('ASSISTANT_TOKEN')
director_token = os.getenv('DIRECTOR_TOKEN')
producer_token = os.getenv('PRODUCER_TOKEN')


def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(producer_token)}


class CastingTestCase(unittest.TestCase):

    def setUp(self):
        """Define test variables and initialize app."""
        #self.app = create_app()
        #self.app = self.app.test_client
        #self.database_path = database_path
        #app.config["SQLALCHEMY_DATABASE_URI"] = database_path
        #app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        #db.app = app
        #db.init_app(app)
        #db.create_all()

        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        #setup_db(self.app, self.database_path)

        # binds the app to the current context
        #with self.app.app_context():
        #    self.db = SQLAlchemy()
        #    self.db.init_app(self.app)
            # create all tables
        #    self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # movies endpoint tests

    def test_get_movies(self):
        res = self.app.get(
            '/movies', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_unauthorized(self):
        res = self.app.get(
            '/movies', headers=set_auth_header(''))
        self.assertEqual(res.status_code, 401)

    def test_add_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        res = self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_add_movie_fail(self):
        res = self.app.post(
            '/movies', json={}, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

    def test_add_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        res = self.app.post(
            '/movies', json=data, headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movies.query.first().id
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_edit_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movies.query.first().id
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_movie_fail(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movies.query.first().id

        data = {
            "title": '',
            "release_date": ''
        }
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)

    def test_delete_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))

        movie_id = Movies.query.first().id
        res = self.app.delete(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_delete_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))

        movie_id = Movies.query.first().id
        res = self.app.delete(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('director'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    # actors endpoint tests

    def test_get_actors(self):
        res = self.app.get(
            '/actors', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_actors_unauthorized(self):
        res = self.app.get(
            '/actors', headers=set_auth_header(''))
        self.assertEqual(res.status_code, 401)

    def test_add_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        res = self.app.post(
            '/actors', json=data, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_add_actor_fail(self):
        res = self.app.post(
            '/actors', json={}, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

    def test_add_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        res = self.app.post(
            '/actors', json=data, headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actors.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_edit_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actors.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_actor_fail(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actors.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', data={},
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_delete_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actors.query.first().id
        res = self.app.delete(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_delete_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actors.query.first().id
        res = self.app.delete(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
