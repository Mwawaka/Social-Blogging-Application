
import os
from app import db,create_app
from flask_script import Shell,Manager


app=create_app(os.environ.get('FLASK_CONFIG') or 'default')
manager=Manager(app)


def make_shell_context():
    return dict(app=app,db=db)
manager.add_command('shell',Shell(make_context=make_shell_context))


if __name__=='main':
    manager.run()