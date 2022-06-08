from datetime import datetime
from flask import render_template
from flask_login import login_required
from app.main import main

@main.route('/')
def landing():
    return render_template('landing.html')

@main.route('/home',methods=['GET','POST'])
@login_required
def index():
    return render_template('home.html')
