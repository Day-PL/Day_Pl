from flask import Flask
from constant import SECRET_KEY
from views import browse, new_course, populars, preferences, saves, users
from models.user_model import db
from views.users import login_manager

app = Flask(__name__)
app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///daypl.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(browse.bp)
app.register_blueprint(new_course.bp)
app.register_blueprint(populars.bp)
app.register_blueprint(preferences.bp)
app.register_blueprint(saves.bp)
app.register_blueprint(users.bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=8080, debug=True)