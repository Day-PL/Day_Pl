from flask import Flask, request, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from utils import SECRET_KEY
from views import browse, new_course, populars, preferences, saves
from flask_login import LoginManager, UserMixin, login_user

from werkzeug.security import generate_password_hash, check_password_hash

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

class User(UserMixin, db.Model):
    def __init__(self):
        self.pwd_hash = None

    id         = db.Column(db.String(128), primary_key = True)
    _id        = db.Column(db.String(64), unique = True, nullable = False)
    pwd_hash   = db.Column(db.String(128),               nullable = False)
    name       = db.Column(db.String(64),                nullable = False)
    gender     = db.Column(db.String(64),                nullable = False)
    birthdate  = db.Column(db.DateTime,                  nullable = False)
    phone      = db.Column(db.String(32), unique = True, nullable = False)
    mail       = db.Column(db.String(32), unique = True, nullable = False)
    rq_terms   = db.Column(db.Boolean,                   nullable = False)
    op_terms   = db.Column(db.Boolean,                   nullable = False)
    sign_date  = db.Column(db.DateTime,                  nullable = False)

    def set_pwd(self, password):
        self.pwd_hash = generate_password_hash(password)
    def check_pwd(self, password):
        return check_password_hash(self.pwd_hash, password)

# 로그인 매니저 생성
login_manager = LoginManager(app)
login_manager.login_view = "users" # 로그인 페이지 URI 명시

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/users')
def users():
    return '유저 홈'

@app.route('/users/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        id = request.form["id"]
        pwd = request.form["pwd"]
        user = User.query.filter(User._id == id).first()
        print(f"디버깅용: id: {id} pwd: {pwd}")
        print(f"디버깅용: id: {id} pwd: {generate_password_hash(pwd)}")
        if user and user.check_pwd(pwd):
            login_user(user)
            print(f'로그인에 성공했습니다.')
            return redirect(url_for('browse.browse'))
        else:
            print(f'로그인에 실패횄습니다.')
            return redirect(url_for('login'))
        
    return render_template('auth/login.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)