from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment

from config import config
db=SQLAlchemy()
mail=Mail()
moment=Moment()


# Factory Function

def create_app(config_name):
    app=Flask(__name__)
    
    app.config.from_object(config[config_name]) #from_object() method ensures that the configurations in the config.py can be imported directly into the application
    
    config[config_name].init_app(app) #.init_app() ensures complete initializtion of the extensions declared above 
    
    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    
    
    #Registering the main blueprint
    from app.main import main as main_bp
    app.register_blueprint(main_bp)
    return app