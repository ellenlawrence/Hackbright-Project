"""Utility file to seed database"""

from sqlalchemy import func
from model import User, City, Destination, Past_Destination

from model import connect_to_db, db
from server import app

def load_users():
    """Load users into database."""

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    User.query.delete()

    user = User(username='jhacks', password='password123')

    db.session.add(user)

    db.session.commit()


def load_cities():
    """Load all the available cities users can choose from."""

    City.query.delete()

    for row in open('seed_data/u.cities'):

        row = row.rstrip()
        city_id, name = row.split('|')

        city = City(city_id=city_id, name=name)
        
        db.session.add(city)

    db.session.commit()


def load_destinations():
    """Load the destinations for each city."""

    for row in open('seed_data/u.destinations'):

        row = row.rstrip()
        destination_id, city_id, name, address = row.split('|')

        destination = Destination(destination_id=destination_id, city_id=city_id, name=name, address=address)

        db.session.add(destination)

    db.session.commit()


def load_past_destinations():
    """Load the destinations users have routed to in the past."""

    for row in open('seed_data/u.past_destinations'):

        row = row.rstrip()
        past_destination_id, user_id, destination_id = row.split('|')

        past_destination = Past_Destination(past_destination_id=past_destination_id, user_id=user_id, destination_id=destination_id)

        db.session.add(past_destination)

    db.session.commit()

def set_val_user_id():
    """Set value for the next user_id after seeding database"""

    # Get the Max user_id in the database
    result = db.session.query(func.max(User.user_id)).one()
    max_id = int(result[0])

    # Set the value for the next user_id to be max_id + 1
    query = "SELECT setval('users_user_id_seq', :new_id)"
    db.session.execute(query, {'new_id': max_id + 1})
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    load_users()
    load_cities()
    load_destinations()
    load_past_destinations()


