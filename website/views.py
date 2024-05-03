from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)


@views.route('/')
def home():
  return render_template("home.html", user=current_user)

@views.route('/notes_space')
@login_required
def notes():
  return render_template("notes_space.html", user=current_user)
