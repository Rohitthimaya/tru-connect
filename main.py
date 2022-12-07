from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room
import os

# Creating a server
app = Flask(__name__)
app.app_context().push()
app.secret_key = os.environ.get("KEY")

# Initialize Flask-SocketIO
socketio = SocketIO(app)
ROOMS = ["lounge", "Tru News", "Programming", "Meet Up"]

# CREATE DATABASE
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///new-users-collection.db"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL",  "sqlite:///new-users-collection.db")

# it will silence the deprecation warning in the console.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# CREATE TABLE
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String, nullable=False)


db.create_all()

# allUsers = User.query.all()
# for user in allUsers:
#     if(user.is_authenticated):
#         print(user.name)


# Home Page Route
@app.route("/", methods=["GET", "POST"])
def homePage():
    return render_template("index.html", logged_in=current_user.is_authenticated)


# Sign In Page Route
@app.route("/signin", methods=["GET", "POST"])
def signIn():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']

        # Find user by email entered.
        user = User.query.filter_by(email=email).first()

        # Check stored password hash against entered password hashed.
        if not user:
            flash("That email does not exist, please try again.")
            return redirect(url_for('signIn'))
        # Password incorrect
        elif not check_password_hash(user.password, password):
            flash('Password incorrect, please try again.')
            return redirect(url_for('signIn'))
        # Email and password are correct
        else:
            login_user(user)
            return redirect(url_for('homePage'))
    return render_template("sign.html", logged_in=current_user.is_authenticated)


# Register Page Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form['email']

        if User.query.filter_by(email=request.form.get('email')).first():
            # User already exists
            flash("You've already signed up with that email, log in instead!")
            return redirect(url_for('signIn'))

        name = request.form['name']
        hash_and_salted_password = generate_password_hash(
            request.form.get('password'),
            method='pbkdf2:sha256',
            salt_length=8
        )
        if email != "":
            truEmail = email.split("@")
            if (truEmail[1] != "mytru.ca"):
                flash("Please Enter Tru Email Only.")
                return redirect(url_for('register'))
            else:
                new_user = User(name=name, email=email, password=hash_and_salted_password)
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user)
                return redirect(url_for("homePage"))
        else:
            return redirect(url_for("register"))
    return render_template("register.html", logged_in=current_user.is_authenticated)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('homePage'))


@app.route("/connect", methods=["GET", "POST"])
@login_required
def connect():
    return render_template("connect.html", logged_in=current_user.is_authenticated, username=current_user.name,
                           rooms=ROOMS)


@app.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    return render_template("feedback.html", logged_in=current_user.is_authenticated)


@app.route("/story", methods=["GET", "POST"])
@login_required
def storyPage():
    return render_template("story.html", logged_in=current_user.is_authenticated)


@socketio.on('message')
def message(data):
    print(f"\n\n{data}\n\n")
    send({'msg': data['msg'], 'username': data['username']}, room=data['room'])


@socketio.on('join')
def join(data):
    join_room(data['room'])
    send({'msg': data['username'] + " has joined the " + data['room'] + " room"}, room=data['room'])


@socketio.on('leave')
def leave(data):
    leave_room(data['room'])
    send({'msg': data['username'] + " has left the " + data['room'] + " room"}, room=data['room'])


if __name__ == "__main__":
    app.run(debug=True)
    # socketio.run(app, debug=True)