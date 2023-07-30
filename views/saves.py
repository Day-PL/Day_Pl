from flask import Blueprint, request, render_template

bp = Blueprint('saves', __name__, url_prefix='/saves')

@bp.route('/')
def saves():
    return render_template('save.html')