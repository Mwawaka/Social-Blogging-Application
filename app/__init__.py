from math import sqrt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment

db=SQLAlchemy()
mail=Mail()
moment=Moment()