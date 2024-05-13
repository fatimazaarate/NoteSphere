from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


# Define a Blueprint for authentication-related routes
auth = Blueprint('auth', __name__)

# Route for login page
@auth.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
    email = request.form.get('email')
    password = request.form.get('password')

    # Check if the user exists
    user = User.query.filter_by(email=email).first()

    if user:
      # Check if the password is correct
      if check_password_hash(user.password, password):
        flash('Logged in successfully!', category='success')
        login_user(user, remember=True) # Log in the user
        return redirect(url_for('views.notes')) # Redirect to notes page after successful login
      else:
        flash('Incorrect password, try again.', category='error')
    else:
        flash('Email does not exist.', category='error')

  return render_template('login.html', user=current_user)

# Route for logout
@auth.route('/logout')
@login_required  # Requires the user to be logged in
def logout():
  logout_user()  # Log out the user
  return redirect(url_for('auth.login'))  # Redirect to login page after logout

# Route for sign up page
@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    # Check if the email is already in use
    user = User.query.filter_by(email=email).first()

    if user:
      flash('Email already exist.', category='error')
    elif len(email) < 5:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(username) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 6:
      flash('Password must be at least 6 characters.', category='error')
    else:
       # Create a new user and add it to the database
      new_user = User(email=email, username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'))
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user, remember=True) # Log in the newly registered user

      flash('Account created with success!', category='success')

      return redirect(url_for('views.notes'))  # Redirect to notes page after successful registration

  return render_template('sign_up.html', user=current_user)
