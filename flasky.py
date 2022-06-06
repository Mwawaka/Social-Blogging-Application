import os
from app import db,create_app

app=create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

if __name__=='__main__':
    app.run()
    
    
    
# defines the Flask application instance ,and also includes a few tasks that help manage the application