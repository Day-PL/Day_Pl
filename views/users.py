from flask import Blueprint, request, render_template, redirect, url_for
from models.user_model import User
from flask_login import login_user

print('디버깅용: bp 이전 줄')
bp = Blueprint('users', __name__, url_prefix='/users')
print('디버깅용: bp 이후 줄')


# # 로그인 매니저 생성
# login_manager = LoginManager(app)
# login_manager.login_view = "users" # 로그인 페이지 URI 명시

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

@bp.route('/')
def users():
    return '유저 홈'

@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form["id"]
        pwd = request.form["pwd"]
        user = User.query.filter(User._id == id).first()
        if user and user.check_pwd(pwd):
            login_user(user)
            print(f'로그인에 성공했습니다.')
            return redirect(url_for("browse"))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for("auth/login.html"))
        
    return render_template('auth/login.html')
