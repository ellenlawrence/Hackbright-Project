"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for, abort)
from werkzeug.utils import secure_filename
from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy import func
import os

from model import User, City, Destination, User_Destination, connect_to_db, db

UPLOAD_FOLDER = '/Users/ellenlawrence/src/project/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ.get('SECRET_KEY')

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Displays signup page, with link to login page."""
    
    return render_template('homepage.html') # there will be a register form on the homepage


@app.route('/signup', methods=['POST'])
def process_registration():
    """Adds a new user to database when the user submits the signup form on the 
    homepage."""

    new_user_username = request.form.get('username')
    new_user_password = request.form.get('password')
    

    if User.query.filter(User.username==new_user_username).all() == []:
        
        new_user = User(username=new_user_username, 
                        password=new_user_password)

        db.session.add(new_user)
        db.session.commit()

    return redirect('/login')


@app.route('/login')
def login():
    """Displays login page."""

    return render_template('login.html')


@app.route('/check_login')
def check_credentials():
    """Handles submission of login form."""

    user_username = request.args.get('username')
    user_password = request.args.get('password')
    user_object = User.query.filter(User.username==user_username, User.password==user_password).all()

    if user_object:
        user_id = user_object[0].user_id
        session['user_id'] = user_id
        return redirect(f'/{user_id}/profile')

    elif User.query.filter(User.username==user_username, User.password!=user_password).all():
        flash('Incorrect password, please try again!') 
        return redirect('/login')
    else:
        flash('Username not recognized.')
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out."""

    session['user_id'] = None
    flash('You have been logged out.')

    return redirect('/login')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def checked_logged_in(user_id):
    """Throws error if user tries to access page when not logged in."""

    if session.get('user_id') != int(user_id):
        abort(403)


@app.route('/<user_id>/profile', methods=['GET', 'POST'])
def show_user_profile(user_id):
    """Displays user's username, profile picture, and their Destinations List 
    along with a button that links to the destination search page."""

    checked_logged_in(user_id)

    user = User.query.filter(User.user_id==user_id).one()
    username = user.username
    user_destinations = User_Destination.query.filter(User_Destination.user_id==user_id).all()
    user_destinations.sort(key=lambda d: d.destination.name)
    all_cities = City.query.all()
    user_cities = set()

    for d in user_destinations:

        user_cities.add(d.destination.city)

    try:
        file = request.files['prof-pic']
        
        if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                user.img = filename
                print(user.img)
                db.session.commit()
    except:
        pass

    return render_template('user_profile.html', 
                            username=username, 
                            user_id=user_id, 
                            user=user, 
                            user_destinations=user_destinations,
                            all_cities=all_cities,
                            user_cities=user_cities)


@app.route('/<user_id>/destination-search-results')
def search_for_destinations(user_id):
    """Searches database for destinations that match the user's input."""

    checked_logged_in(user_id)

    user = User.query.filter(User.user_id==user_id).one().username

    cities = City.query.all()

    user_input = request.args.get('destination')

    city_id = request.args.get('city')
    
    results = Destination.query.filter(Destination.city_id==city_id, Destination.name.ilike('%' + user_input + '%')).all()
    results.sort(key=lambda d: d.name)

    if results == []:
        flash('Your search returned no results. Please try again!')
        return redirect(f'/{user_id}/destination-search')


    return render_template('search_results.html', 
                            user=user, 
                            user_id=user_id, 
                            cities=cities, 
                            results=results)


@app.route('/<user_id>/map', methods=['POST'])
def update_destination_list(user_id):
    """Adds selected destinations to user's Destination List if they are not
    in there already."""

    checked_logged_in(user_id)

    user = User.query.filter(User.user_id==user_id).one().username

    destinations = request.form.getlist('destination[]')

    user_destinations = User_Destination.query.filter(User_Destination.user_id==user_id).all()
    
    def get_dest_id(User_Destination):

        return User_Destination.destination_id

    dest_ids = map(get_dest_id, user_destinations)

    for d in destinations:

        if int(d) not in dest_ids:
            user_destination = User_Destination(user_id=user_id, 
                                                destination_id=d)
            db.session.add(user_destination)
    
    db.session.commit()

    return redirect(f'/{user_id}/map')


@app.route('/<user_id>/map', methods=['GET'])
def show_map_and_destination_list(user_id):
    """Displays map centered at user's location along with the user's list of 
    destinations they have in their destination list on the right side of the 
    screen."""

    checked_logged_in(user_id)

    user = User.query.filter(User.user_id==user_id).one().username

    user_destinations = User_Destination.query.filter(User_Destination.user_id==user_id).all()
    user_destinations.sort(key=lambda d: d.destination.name) 

    destinations = []

    all_cities = City.query.all()

    cities = set()

    for d in user_destinations:

        destinations.append(d.destination)
        cities.add(d.destination.city)
    
    return render_template('map.html', 
                            user_id=user_id, 
                            user=user, 
                            cities=cities,
                            all_cities=all_cities,
                            destinations=destinations,
                            google_maps_key=os.environ.get('GOOGLE_MAPS_API_KEY'))

if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = False
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



