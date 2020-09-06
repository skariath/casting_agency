from sqlalchemy import Column, String, create_engine
from sqlalchemy import Table, Integer, ForeignKey, Date
from flask_sqlalchemy import SQLAlchemy
import json
import os
from datetime import date


db = SQLAlchemy()

database_path = os.environ['DATABASE_URL']


'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''


def setup_db(app, database_path=database_path):
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


def db_drop_and_create_all():
    """drops the database tables and starts fresh
    can be used to initialize a clean database"""
    db.drop_all()
    db.create_all()
    db_init_records()


def db_init_records():
    '''this will initialize the database with some test records.'''

    new_actor = (Actors(name='Brad Pitt', gender='Male'))

    new_movie = (Movies(title='Fight Club', release_date=date.today()))

    new_relationship = movie_actor_relationship.insert().values(
        Movie_id=new_movie.id,
        Actor_id=new_actor.id,
    )

    new_actor.insert()
    new_movie.insert()
    db.session.execute(new_relationship)
    db.session.commit()


# Table to capture the N:N relationship between movies and actors
movie_actor_relationship = db.Table(
    'movie_actor_relationship',
    db.Model.metadata,
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actors.id'))
)


class Movies(db.Model):

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date = Column(Date, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"

    def insert(self):
        """inserts a new record into movies table
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a record from the movies table
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """updates a movies table record
        """
        db.session.commit()

    def format(self):
        """returns a formatted response of the movie"""
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            }


class Actors(db.Model):

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    gender = Column(String(6), nullable=False)
    movies = db.relationship('Movies', secondary=movie_actor_relationship,
                             backref='movies_list', lazy=True)

    def __repr__(self):
        return f"<Actor {self.id} {self.name}>"

    def insert(self):
        """inserts a new record into the actors table
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a record from the actors table
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """updates a record in the actors table
        """
        db.session.commit()

    def format(self):
        """returns a formatted response of the actor"""
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
        }
