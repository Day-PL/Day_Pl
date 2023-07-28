from flask import Blueprint, request, render_template

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/login')
def login():
    return render_template('auth/login.html')