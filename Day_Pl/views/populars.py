from flask import Blueprint, request, render_template

bp = Blueprint('populars', __name__, url_prefix='/populars')

@bp.route('/')
def populars():
    return render_template('populars.html')