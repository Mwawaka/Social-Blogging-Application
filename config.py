import os
basedir=os.path.abspath(os.path.dirname(__name__)) #gets the base directory path of our application

class Config:
    SECRET_KEY=os.environ.get('SECRET_KEY') #retrieves the secret_key set in the environment variable 
    SQLALCHEMY_COMMIT_ON_TEARDOWN=True      #enables automatic commits of database changes at the end of each request
    FLASKY_MAIL_SUBJECT_PREFIX=['Flasky']
    FLASKY_MAIL_SENDER=''
    FLASKY_ADMIN=os.environ.get('FLASKY_ADMIN')


