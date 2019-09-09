import unittest
from unittest import TestCase
from server import app
from model import User, City, Destination, User_Destination, connect_to_db, db


class FlaskTests(TestCase):

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'ABC'

        # Logs in test user
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 1

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        
        user = User(username='correctusername', 
                    password='correctpassword')
        city = City(name='San Francisco')
        destination = Destination(city=city, 
                                  name='Mission Dolores Park', 
                                  address='Dolores St &, 19th St, San Francisco, CA 94114')

        db.session.add_all([user, city])
        db.session.commit()

    def test_wrong_password(self):
        """Make sure the check_credentials function is returning the correct 
        results."""

        result = self.client.get('/check_login',
                                  query_string={'username': 'correctusername', 'password': 'wrongpassword'},
                                  follow_redirects=True)

        self.assertIn(b'Incorrect password, please try again!', result.data)


    def test_wrong_username(self):
        """Make sure the check_credentials function is returning the correct 
        results."""

        result = self.client.get('/check_login',
                                  query_string={'username': 'wrongusername', 'password': 'correctpassword'},
                                  follow_redirects=True)

        self.assertIn(b'Username not recognized.', result.data)


    def test_add_destination(self):

        result = self.client.post('/1/map',
                                  data={"destination[]": 1})
    
        self.assertEqual(User_Destination.query.count(), 1)
        

    def tearDown(self):
        """Stuff to do after every test."""

        db.session.remove()
        
        # dropping old tables
        db.drop_all()
        db.engine.dispose()








if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()

