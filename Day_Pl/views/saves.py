from flask import Blueprint, request, render_template
from flask_login import current_user

bp = Blueprint('saves', __name__, url_prefix='/saves')

@bp.route('/')
def saves():
    return render_template('saves.html', current_user = current_user)