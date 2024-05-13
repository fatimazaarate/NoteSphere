from flask import Blueprint, render_template, flash, request, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from datetime import datetime


# Define a Blueprint for the views
views = Blueprint('views', __name__)

# Route for the home page
@views.route('/')
def home():
  # Render the home page template and pass the current user
  return render_template("home.html", user=current_user)

# Route for the notes space page
@views.route('/notes_space', methods=['GET', 'POST'])
@login_required  # Requires the user to be logged in
def notes():
   # If the request method is POST (i.e., form submission)
  if request.method == 'POST':
    note = request.form.get('note')  # Get the note text from the form

    if len(note) < 1:  # If the note is too short
      flash('Note is too short!', category='error')  # Flash an error message
    else:
      # Add current date and time to the note text
      note_text_with_datetime = f"{note}\n{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

      # Create a new Note object and add it to the database
      new_note = Note(text=note_text_with_datetime, user_id=current_user.id)
      db.session.add(new_note)
      db.session.commit() # Commit the transaction to the database
      flash('Note added!', category='success')  # Flash a success message

  # Render the notes space page template and pass the current user
  return render_template("notes_space.html", user=current_user)

# Route for deleting a note
@views.route('/delete-note', methods=['POST'])
def delete_note():
  note = json.loads(request.data)  # Load the JSON data from the request
  noteId = note['noteId']  # Get the ID of the note to be deleted
  note = Note.query.get(noteId)  # Query the database to get the note object

  if note:  # If the note exists
    if note.user_id == current_user.id:  # If the note belongs to the current user
      db.session.delete(note)  # Delete the note from the database
      db.session.commit()  # Commit the transaction to the database
      flash('Note deleted.', category='success')  # Flash a success message
      
  # Return a JSON response with a success message    
  return jsonify({'message': 'Note deleted.', 'category': 'success'})  