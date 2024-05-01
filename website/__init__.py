from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

db = SQLAlchemy()
NOTESPHERE_DB = 'database.db'


def create_app():
	app = Flask(__name__)
	app.config['SECRET_KEY'] = 'not secret'
	app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{NOTESPHERE_DB}'
	db.init_app(app)

	from .views import views
	from .auth import auth

	app.register_blueprint(views, url_prefix='/')
	app.register_blueprint(auth, url_prefix='/')

	from .models import User, Note

	create_db(app)

	return app

def create_db(app):
	with app.app_context():
		if not path.exists('website/' + NOTESPHERE_DB):
			db.create_all()
			print('Created Database!')
