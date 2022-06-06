from crypt import methods
from datetime import datetime

from flask import render_template
from app.main import main
from app import db

@main.route('/',methods=['GET','POST'])
def index():
    return render_template('base.html')
