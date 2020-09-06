import unittest
import os
import json
from app import create_app
from models import setup_db, db, Movies, Actors, db_drop_and_create_all
from flask_sqlalchemy import SQLAlchemy
from datetime import date

# Create dict with Authorization key and Bearer token as values. 
# Later used by test classes as Header
assistant_token = os.getenv('ASSISTANT_TOKEN')
director_token = os.getenv('DIRECTOR_TOKEN')
producer_token = os.getenv('PRODUCER_TOKEN')

casting_assistant_auth_header = {
    'Authorization': 'Bearer {}'.format(assistant_token)
}

casting_director_auth_header = {
    'Authorization': 'Bearer {}'.format(director_token)
}

executive_producer_auth_header = {
    'Authorization': 'Bearer {}'.format(producer_token)
}

class CastingTestCase(unittest.TestCase):
    
    def setUp(self):
        """Define test variables and initialize app."""
    
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)
        self.casting_director_auth_header = casting_director_auth_header
        self.casting_assistant_auth_header = casting_assistant_auth_header
        self.executive_producer_auth_header = executive_producer_auth_header
        

        db_drop_and_create_all()
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#----------------------------------------------------------------------------#
# Tests for POST actors
#----------------------------------------------------------------------------#

    def test_create_new_actor(self):
        """Test create new actor."""

        json_create_actor = {
            'name' : 'George Clooney',
            'gender' : "M"
        } 

        res = self.client().post('/actors', json = json_create_actor, headers = casting_director_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        
    def test_error_401_new_actor(self):
        """Test POST new actor w/o Authorization."""

        json_create_actor = {
            'name' : 'George Clooney',
            'gender' : "M"
        } 

        res = self.client().post('/actors', json = json_create_actor)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_error_400_create_new_actor(self):
        """Test Error POST new actor, mandatory missing."""

        json_create_actor_no_name = {
            'gender' : "M"
        } 

        res = self.client().post('/actors', json = json_create_actor_no_name, headers = casting_director_auth_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

#----------------------------------------------------------------------------#
# Tests for GET actors
#----------------------------------------------------------------------------#
    def test_get_all_actors(self):
        """Test GET all actors."""
        res = self.client().get('/actors', headers = casting_assistant_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actors']) > 0)

    def test_error_401_get_all_actors(self):
        """Test GET all actors without Authorization."""
        res = self.client().get('/actors')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
#----------------------------------------------------------------------------#
# Tests for PATCH actors
#----------------------------------------------------------------------------#

    def test_edit_actor(self):
        """Test PATCH existing actors"""
        json_edit_actor = {
            'name' : 'Bradley Cooper'
        } 
        res = self.client().patch('/actors/1', json = json_edit_actor, headers = casting_director_auth_header)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['actor']) > 0)
        
    def test_error_404_edit_actor(self):
        """Test PATCH with invalid id"""
        json_edit_actor = {
            'name' : 'Bradley Cooper'
        } 
        
        res = self.client().patch('/actors/123412', json = json_edit_actor, headers = casting_director_auth_header)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'not found')

    def test_error_castingassistant_edit_actor(self):
        """Test DELETE existing actor with missing permissions"""
        json_edit_actor = {
            'name' : 'Bradley Cooper'
        } 
        res = self.client().patch('/actors/1', json = json_edit_actor, headers = casting_assistant_auth_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
#----------------------------------------------------------------------------#
# Tests for DELETE actors
#----------------------------------------------------------------------------#

    def test_error_401_delete_actor(self):
        """Test DELETE existing actor w/o Authorization"""
        res = self.client().delete('/actors/1')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_error_cast_assistant_delete_actor(self):
        """Test DELETE existing actor with missing permissions"""
        res = self.client().delete('/actors/1', headers = casting_assistant_auth_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_delete_actor(self):
        """Test DELETE existing actor"""
        res = self.client().delete('/actors/1', headers = casting_director_auth_header)
        data = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_error_404_delete_actor(self):
        """Test DELETE actor not existing"""
        res = self.client().delete('/actors/15125', headers = casting_director_auth_header)
        data = res.get_json()
               
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'not found')

#----------------------------------------------------------------------------#
# Tests for POST movies
#----------------------------------------------------------------------------#

    def test_create_new_movie(self):
        """Test POST new movie."""

        json_create_movie = {
            'title' : 'Sparta',
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie, headers = executive_producer_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
        
    def test_error_422_create_new_movie(self):
        """Test Error POST new movie."""

        json_create_movie_without_name = {
            'release_date' : date.today()
        } 

        res = self.client().post('/movies', json = json_create_movie_without_name, headers = executive_producer_auth_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'bad request')

#----------------------------------------------------------------------------#
# Tests for /movies GET
#----------------------------------------------------------------------------#

    def test_get_all_movies(self):
        """Test GET all movies."""
        res = self.client().get('/movies', headers = casting_assistant_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movies']) > 0)

    def test_error_401_get_all_movies(self):
        """Test GET all movies without Authorization."""
        res = self.client().get('/movies')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies PATCH
#----------------------------------------------------------------------------#

    def test_edit_movie(self):
        """Test PATCH existing movies"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = executive_producer_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertTrue(len(data['movie']) > 0)

    def test_error_404_edit_movie(self):
        """Test PATCH with non valid id"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/123412', json = json_edit_movie, headers = executive_producer_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'not found')

    def test_error_castingassistant_edit_movie(self):
        """Test DELETE existing actor with missing permissions"""
        json_edit_movie = {
            'release_date' : date.today()
        } 
        res = self.client().patch('/movies/1', json = json_edit_movie, headers = casting_assistant_auth_header)
        data = res.get_json()
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

#----------------------------------------------------------------------------#
# Tests for /movies DELETE
#----------------------------------------------------------------------------#

    def test_error_401_delete_movie(self):
        """Test DELETE existing movie without Authorization"""
        res = self.client().delete('/movies/1')
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_error_castingassistant_delete_movie_assistant(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers = casting_assistant_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_error_castingdirector_delete_movie_director(self):
        """Test DELETE existing movie with wrong permissions"""
        res = self.client().delete('/movies/1', headers = casting_director_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])
        
    def test_delete_movie(self):
        """Test DELETE existing movie"""
        res = self.client().delete('/movies/1', headers = executive_producer_auth_header)
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        
    def test_error_404_delete_movie(self):
        """Test DELETE non existing movie"""
        res = self.client().delete('/movies/151251', headers = executive_producer_auth_header) 
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'] , 'not found')

if __name__ == '__main__':
    unittest.main()
