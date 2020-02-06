"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, session)

from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, Rating, Movie


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
    return render_template("homepage.html")

@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/register", methods=["GET"])
def register_form():

    return render_template('register_form.html')


@app.route("/register", methods=["POST"])
def register_process():

    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter_by(email=email).all():
        return redirect("/")

    else:
        # add to database
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
     

    return redirect("/")



@app.route("/login", methods=["GET"])
def login_form():

    return render_template('login_form.html')



@app.route("/login", methods=["POST"])
def login_process():

    email = request.form.get('email')
    password = request.form.get('password')

    if User.query.filter(email == email, password == password).all():
        
        
        # query user_id
        user = User.query.filter(email ==email, password ==password).all()

        # add user_id to Flask Session
        if session.get('user_id') is not None:
            session['user_id'] = user.user_id
        else:
            session['user_id'] = []

        
        flash("Logged in! Hi {user.user_id}")
        
        return redirect("/")

    else:
        flash("Invalid Email and Password")
        
        return redirect("/")
     

    return redirect("/")



    #check if email is in users table (if email field is not null)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
