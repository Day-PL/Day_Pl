from flask import Blueprint, request, render_template

bp = Blueprint('new_course', __name__, url_prefix='/new-course')

@bp.route('/')
def new_course():
    return render_template('new_course.html')