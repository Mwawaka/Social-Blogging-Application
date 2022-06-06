import os
from app import db,create_app
from flask.cli import FlaskGroup


app=create_app(os.environ.get('FLASK_CONFIG') or 'default')
cli=FlaskGroup(app)


def make_shell_context():
    return dict(app=app,db=db)
manager.add_command('shell',Shell(make_context=make_shell_context))


if __name__=='main':
    manager.run()
    
    
    
# defines the Flask application instance ,and also includes a few tasks that help manage the application