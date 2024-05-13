from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager


# Initialize SQLAlchemy database object
db = SQLAlchemy()
# Name of the database file
NOTESPHERE_DB = 'database.db'

# Function to create the Flask application
def create_app():
	app = Flask(__name__)
	# Secret key for session management
	app.config['SECRET_KEY'] = 'not secret'
	# Database URI for SQLAlchemy
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOTESPHERE_DB}'
	# Initialize SQLAlchemy with the app
	db.init_app(app)

	# Import views and authentication blueprints
	from .views import views
	from .auth import auth

	# Register blueprints with the app
	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	# Register blueprints with the app
	from .models import User, Note

	# Create the database if it doesn't exist
	create_db(app)

	# Initialize Flask-Login
	login_manager = LoginManager()
	login_manager.login_view = 'auth.login'
	login_manager.init_app(app)

	# User loader function for Flask-Login
	@login_manager.user_loader
	def load_user(id):
		return User.query.get(int(id))

	return app

# Function to create the database
def create_db(app):
	with app.app_context():
		if not path.exists('website/' + NOTESPHERE_DB):
			# Create all tables if the database file doesn't exist
			db.create_all()
			print('Created Database!')
