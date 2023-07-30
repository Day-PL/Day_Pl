from flask import Blueprint, request, render_template

bp = Blueprint('browse', __name__, url_prefix='/browse')

# <메인 페이지>
# 인기 TOP3 코스 보여주기
# 나의 플랜 만들기

@bp.route("/")
def browse():
    return render_template("browse.html")