from datetime import datetime
from flask import render_template
from flask_login import login_required
from app.main import main
from app import db

@main.route('/',methods=['GET','POST'])
@login_required
def index():
    return render_template('home.html')
