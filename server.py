"""Movie Ratings."""

from jinja2 import StrictUndefined
from flask import (Flask, render_template, redirect, request, flash, session, jsonify, url_for)
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
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Displays signup page, with link to login page."""
    
    return render_template('homepage.html') # there will be a register form on the homepage


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/signup', methods=['POST'])
def process_registration():
    """Adds a new user to database when the user submits the signup form on the 
    homepage."""

    new_user_username = request.form.get('username')
    new_user_password = request.form.get('password')
    file = request.files['prof-pic']
    
    if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    if User.query.filter(User.username==new_user_username).all() == []:
        
        new_user = User(username=new_user_username, 
                        password=new_user_password,
                        img=filename)

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
        flash('Incorrect password, please try again!') # flash messages aren't working 
        return redirect('/login')
    else:
        flash('Username not recognized.')
        print('hello')
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out."""

    session['user_id'] = None
    flash('You have been logged out.') # you can update these to use AJAX in JS instead of being a flash message

    return redirect('/login')


@app.route('/<user_id>/profile')
def show_user_profile(user_id):
    """Displays user's username, profile picture, and their Destinations List 
    along with a button that links to the destination search page."""

    user = User.query.filter(User.user_id==user_id).one()
    username = user.username
    profile_pic = user.img
    user_destinations = User_Destination.query.filter(User_Destination.user_id==user_id).all()

    return render_template('user_profile.html', 
                            username=username, 
                            user_id=user_id, 
                            profile_pic=profile_pic, 
                            user_destinations=user_destinations)


@app.route('/<user_id>/destination-search')
def show_search_page(user_id):
    """Displays the destination search page."""

    user = User.query.filter(User.user_id==user_id).one().username 
    cities = City.query.all()


    return render_template('destination_search.html', 
                            user=user, 
                            user_id=user_id, 
                            cities=cities)


@app.route('/<user_id>/destination-search-results')
def search_for_destinations(user_id):
    """Searches database for destinations that match the user's input."""

    user = User.query.filter(User.user_id==user_id).one().username

    cities = City.query.all()

    user_input = request.args.get('destination')

    city_id = request.args.get('city')
    
    results = Destination.query.filter(Destination.city_id==city_id, Destination.name.ilike('%' + user_input + '%')).all()

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

    user = User.query.filter(User.user_id==user_id).one().username

    destinations = request.form.getlist('destination[]')
    print(destinations)

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

    user = User.query.filter(User.user_id==user_id).one().username

    user_destinations = User_Destination.query.filter(User_Destination.user_id==user_id).all() 

    destinations = []

    cities = set()

    for d in user_destinations:

        destinations.append(d.destination)
        cities.add(d.destination.city)
    
    return render_template('map.html', 
                            user_id=user_id, 
                            user=user, 
                            cities=cities,
                            destinations=destinations)

if __name__ == '__main__':
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')



