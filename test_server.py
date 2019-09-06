import unittest
from unittest import TestCase
from server import app
from model import User, City, Destination, User_Destination, connect_to_db, db


# def example_data():
#     """Create some sample data."""

#     user1 = User('username1', 'password1')

#     db.session.add(user1)
#     db.session.commit()


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # dropping old tables
        db.drop_all()

        # Create tables and add sample data
        db.create_all()
        
        self.user = User(user_id=1, username='username1', password='password1')
        # self.city = 
        # self.destination = Destination()

        db.session.add(self.user)
        db.session.commit()

    def test_check_credentials(self):
        """Make sure the check_credentials function is returning the correct 
        results."""

        result = self.client.get("/check_login",
                                  query_string={"username": "username1", "password": "123"},
                                  follow_redirects=True)

        self.assertIn(b"Incorrect password, please try again!", result.data)

    def test_add_destination(self):

        # result = self.client.post("/{}/map".format(self.user.user_id),
        #                           data={"destination[]": self.destination.destination_id})
        self.assertNotEqual(User_Destination.query.all(), [])








if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()

