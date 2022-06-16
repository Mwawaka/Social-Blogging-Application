from flask import render_template
from flask_login import login_required
from app.main import main

@main.route('/')
@main.route('/home',methods=['GET','POST'])
@login_required
def landing():
    return render_template('landing.html')

#profile pages route
