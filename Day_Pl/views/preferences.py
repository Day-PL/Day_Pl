from flask import Blueprint, request, render_template

bp = Blueprint('preferences', __name__, url_prefix='/preferences')

@bp.route('/')
def preferences():
    return render_template('preferences.html')