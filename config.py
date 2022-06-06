import os
basedir=os.path.abspath(os.path.dirname(__file__)) #gets the base directory path of our application

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') #retrieves the secret_key set in the environment variable 
    
    MAIL_SERVER='smtp.mailtrap.io'
    MAIL_PORT='2525'
    MAIL_USE_TLS=True
    MAIL_USE_SSL=False
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    FLASKY_MAIL_SUBJECT_PREFIX=['Flasky']
    FLASKY_MAIL_SENDER=''
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG=True
   
    SQLALCHEMY_DATABASE_URI='sqlite:///dev.db'
    #os.environ.get('DEV_DATABASE_URL' or 'sqlite:///' +os.path.join(basedir,'development.db'))
    
class TestingConfig(Config):
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL')
    
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI=os.environ.get('PRODUCTION_DATABASE_URL')
    
config={
    'development':DevelopmentConfig,
    'testing':TestingConfig,
    'production':ProductionConfig,
    
    'default':DevelopmentConfig
}