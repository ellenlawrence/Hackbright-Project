"""Models and database functions for project."""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = 'users'

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    # img_url = db. Column(db.String(1000), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<User user_id={self.user_id} username={self.username}>'


class City(db.Model):
    """Cities with associated destinations that users can choose from."""

    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.Text)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<City city_id={self.city_id} name={self.name}'


class Destination(db.Model):
    """Destinations users can add to their favorites and use to create a route."""

    __tablename__ = 'destinations'

    destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.city_id'))
    name = db.Column(db.Text)
    address = db.Column(db.Text)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<Destination destination_id={self.destination_id} name={self.name}'

class Visited_Destination(db.Model):
    """User ratings of movies"""

    __tablename__ = 'visited_destinations'

    visited_destination_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('destinations.destination_id'))


    # define relationship to user
    user = db.relationship('User', backref='visited_destinations')

    # define relationship to movie
    destination = db.relationship('Destination', backref='visited_destinations')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Visited_Destination 
                   visited_destination_id={self.visited_destination_id} 
                   user_id={self.user_id} 
                   destination_id={self.destination_id}>"""

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///database'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")



