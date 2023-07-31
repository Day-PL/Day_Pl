from flask import Blueprint, request, render_template, url_for, redirect
from flask_login import login_user
from models.user_model import User
from flask_login import LoginManager, UserMixin

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('/')
def users():
    return '유저 홈'

@bp.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form["id"]
        pwd = request.form["pwd"]
        user = User.query.filter(User._id == id).first()
        print(f"디버깅용: id: {id} pwd: {pwd}")
        if user and user.check_pwd(pwd):
            login_user(user)
            print(f'로그인에 성공했습니다.')
            return redirect(url_for('browse.browse'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('users.login'))
        
    return render_template('auth/login.html')

# 로그인 매니저 생성
# login_manager = LoginManager(app)
login_manager = LoginManager()
login_manager.login_view = "login" # 로그인 페이지 URI 명시

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)