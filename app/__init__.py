from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_moment import Moment
from config import config
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate

db = SQLAlchemy()
mail = Mail()
moment = Moment()
bcrypt=Bcrypt()
login_manager=LoginManager()
#login_view attribute sets the end point for the login page .Flask will redirect to the login page when anonymous user tries to access a protected page 
login_manager.login_view='auth.login'
migrate=Migrate()
# Factory Function

def create_app(config_name):
    app = Flask(__name__)

    # from_object() method ensures that the configurations in the config.py can be imported directly into the application
    app.config.from_object(config[config_name])

    config[config_name].init_app(app)
    # .init_app() ensures complete initializtion of the extensions declared above

    db.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)
    # Registering the main blueprint

    from app.main import main as main_bp
    app.register_blueprint(main_bp)

    from app.auth import auth as auth_bp
    app.register_blueprint(auth_bp,url_prefix='/auth')

    return app
