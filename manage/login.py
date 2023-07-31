# from flask_login import LoginManager
# from app import app
# from models.user_model import User

# # 로그인 매니저 생성
# login_manager = LoginManager(app)
# login_manager.login_view = "users" # 로그인 페이지 URI 명시

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)