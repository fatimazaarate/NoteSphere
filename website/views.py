from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def home():
  return render_template("home.html")

@views.route('/notes_space')
def notes():
  return render_template("notes_space.html")
