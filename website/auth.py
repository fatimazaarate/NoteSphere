from flask import Blueprint, render_template, request, flash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
  data = request.form
  print(data)
  return render_template('login.html')

@auth.route('/logout')
def logout():
  return 'Logout'

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  if request.method == 'POST':
    email = request.form.get('email')
    username = request.form.get('username')
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')

    if len(email) < 5:
      flash('Email must be greater than 3 characters.', category='error')
    elif len(username) < 2:
      flash('First name must be greater than 1 character.', category='error')
    elif password1 != password2:
      flash('Passwords don\'t match.', category='error')
    elif len(password1) < 6:
      flash('Password must be at least 6 characters.', category='error')
    else:
      flash('Account created with success!', category='success')

  return render_template('sign_up.html')

