from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        note = request.form.get('note') # Tabela do HTML 
    return render_template("home.html", user=current_user)

@views.route('/dashresultado', methods=['POST'])
def search():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_string']
        search = '%{}%'.format(search_value)
        results = Note.query.filter(Note.query.Dashboard.like(search)).all()
        return render_template(home, user=current_user, Dashboard=results)
    else:
        return redirect('/')