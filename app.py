from flask import Flask
from views import browse, new_course, populars, preferences, saves, users
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from utils import SECRET_KEY


app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daypl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

app.register_blueprint(browse.bp)
app.register_blueprint(new_course.bp)
app.register_blueprint(populars.bp)
app.register_blueprint(preferences.bp)
app.register_blueprint(saves.bp)
app.register_blueprint(users.bp)

# 로그인 매니저 생성
login_manager = LoginManager(app)
login_manager.login_view = "users" # 로그인 페이지 URI 명시
