from flask import Blueprint

from app.models import Permission

main=Blueprint('main',__name__)

from app.main import error,views

@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

# context processor makes the constants in Permission class available to all templates during rendering 