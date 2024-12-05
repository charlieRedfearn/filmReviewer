from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager()
login_manager.init_app(app)


babel = Babel(app)

@babel.localeselector
def select_locale():
    return get_locale()

admin = Admin(app,template_mode='bootstrap4')

migrate = Migrate(app, db)

from app import views, models