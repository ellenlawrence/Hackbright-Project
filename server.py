"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import User, City, Destination, Past_Destination, connect_to_db, db


app = Flask(__name__)

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
        flash('You are now logged in!')
        return redirect('/' + str(user_id) + '/profile')

    elif User.query.filter(User.username==user_username, User.password!=user_password).all():
        flash('Incorrect password, please try again!') # update these to use AJAX in JS instead of being a flash message 
        return redirect('/login')
    else:
        flash('Email address is not recognized, please signup.') # update these to use AJAX in JS instead of being a flash message
        return redirect('/')


@app.route('/logout')
def logout():
    """Logs user out."""

    session['user_id'] = None
    flash('You have been logged out.') # you can update these to use AJAX in JS instead of being a flash message

    return redirect('/login')


@app.route('/<user_id>/profile')
def show_user_profile(user_id):
    """Displays user's username, photo(?), and Past Destinations along with a 
    button that links to the destination search page."""

    user = User.query.filter(User.user_id==user_id).one().username
    
    past_destinations = Past_Destination.query.filter(Past_Destination.user_id==user_id).all()

    return render_template('user_profile.html', user=user, user_id=user_id, past_destinations=past_destinations)


@app.route('/<user_id>/destination-search')
def show_search_page(user_id):
    """Displays the destination search page."""

    # shows user's username at the top in the same place it was at in the profile (find out how to do this with sessions maybe)
    user = User.query.filter(User.user_id==user_id).one().username 
    cities = City.query.all()

    # not sure how to make it so that once user selects a city, the search results will only display destinations in that city.
    # destinations = Destination.query.filter(Destination.city_id==?)

    return render_template('destination_search.html', user=user, user_id=user_id, cities=cities)


@app.route('/<user_id>/destination-search-results')
def search_for_destinations(user_id):
    """Searches database for destinations that match the user's input."""

    # shows user's username at the top in the same place it was at in the profile (find out how to do this with sessions maybe)
    user = User.query.filter(User.user_id==user_id).one().username

    user_input = request.args.get('destination')

    results = Destination.query.filter(Destination.name.like('%' + user_input + '%')).all() # need to get search to recognize matches regardless of letter case

    if results == []:
        flash('Your search returned no results. Please try again!') # you should update these to use AJAX in JS instead of being a flash message
        return redirect('/' + str(user_id) +'/destination-search')

    return render_template('search_results.html', user=user, user_id=user_id, results=results)


@app.route('/<user_id>/map')
def show_map_and_destination_list(user_id):
    """Displays map centered at user's location along with the user's list of 
    destinations they have in their destination list on the right side of the 
    screen."""

    # not sure how to store user's new destination selections

    user = User.query.filter(User.user_id==user_id).one().username

    destinations = request.args.get('destination')

    return render_template('map.html', user_id=user_id, user=user, destinations=destinations)


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



