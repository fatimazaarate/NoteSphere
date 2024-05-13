from website import db
from flask_login import UserMixin
from sqlalchemy.sql import func


# Define a model for storing notes
class Note(db.Model):
  # Define columns for the Note table
  id = db.Column(db.Integer, primary_key=True)
  text = db.Column(db.String(10000))
  date = db.Column(db.DateTime(timezone=True), default=func.now())
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Define a model for storing users
class User(db.Model, UserMixin):
  # Define columns for the User table
  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(128), unique=True)
  password = db.Column(db.String(128))
  username = db.Column(db.String(128))
  notes = db.relationship('Note')
