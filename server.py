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
    """Homepage."""
    
    return render_template('homepage.html') # there will be buttons to either login or register on the homepage


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
    user_id = user_object[0].user_id

    if user_object:
        session['user_id'] = user_id
        flash('You are now logged in!')
        return redirect('/users/'+str(user_id))

    elif User.query.filter(User.email==user_email, User.password!=user_password).all():
        flash('Incorrect password, please try again!') # you can update these to use AJAX in JS instead of being a flash message 
        return redirect('/login')
    else:
        flash('Email address is not recognized, please register.') # you can update these to use AJAX in JS instead of being a flash message
        return redirect('/register')


@app.route('/register')
def register():
    """Displays registration page."""

    return render_template('register.html')


@app.route('/register', methods=["POST"])
def process_registration():
    """Adds a new user to database"""

    new_user_username = request.form.get('username')
    new_user_password = request.form.get('password')

    if User.query.filter(User.username==new_user_username).all() == []:
        
        new_user = User(username=new_user_username, 
                        password=new_user_password)

        db.session.add(new_user)
        db.session.commit()

    return redirect('/login')


@app.route('/logout')
def logout():
    """Logs user out."""

    session['user_id'] = None
    flash('You have been logged out.') # you can update these to use AJAX in JS instead of being a flash message

    return redirect('/login')


@app.route('/users/<user_id>')
def show_user_profile(user_id):
    """Displays user's Destination List and Past Destinations"""

    user = User.query.filter(User.user_id==user_id).one()
    ratings = Rating.query.filter(Rating.user_id==user_id).all()

    return render_template("user_info.html", user=user,ratings=ratings)



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



