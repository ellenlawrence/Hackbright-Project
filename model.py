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

    user_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    username = db.Column(db.String(64), 
                         nullable=False)
    password = db.Column(db.String(64), 
                         nullable=False)
    img = db.Column(db.String(1000), 
                    nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<User user_id={self.user_id} username={self.username}>'


class City(db.Model):
    """Cities with associated destinations that users can choose from."""

    __tablename__ = 'cities'

    city_id = db.Column(db.Integer, 
                        autoincrement=True, 
                        primary_key=True)
    name = db.Column(db.Text, 
                     nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<City city_id={self.city_id} name={self.name}'


class Destination(db.Model):
    """Destinations users can add to their list and use to create a route."""

    __tablename__ = 'destinations'

    destination_id = db.Column(db.Integer, 
                               autoincrement=True, 
                               primary_key=True)
    city_id = db.Column(db.Integer, 
                        db.ForeignKey('cities.city_id'), 
                        nullable=False)
    name = db.Column(db.Text, 
                     nullable=False)
    address = db.Column(db.Text, 
                        nullable=False)

    city = db.relationship('City', 
                            backref='destinations')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f'<Destination destination_id={self.destination_id} name={self.name}'


class User_Destination(db.Model):
    """Destinations on user's Destination List."""

    __tablename__ = 'user_destinations'

    user_destination_id = db.Column(db.Integer, 
                                    autoincrement=True, 
                                    primary_key=True)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey('users.user_id'), 
                        nullable=False)
    destination_id = db.Column(db.Integer, 
                               db.ForeignKey('destinations.destination_id'), 
                               nullable=False)
        
    # define relationship to user
    user = db.relationship('User', 
                            backref='user_destinations')

    # define relationship to destination
    destination = db.relationship('Destination', 
                                   backref='user_destinations')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User_Destination 
                   user_destination_id={self.user_destination_id} 
                   user_id={self.user_id} 
                   destination_id={self.destination_id}>"""


##############################################################################
# Helper functions

def connect_to_db(app, uri='postgresql:///database'):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")



