from flask import Flask   
import os                

from iphone.extensions import db, login_manager, bcrypt, migrate
from iphone.models import User, Type, Iphone
from iphone.core.routes import core_bp
from iphone.users.routes import users_bp
from iphone.iphone.routes import iphone_bp  

def create_app():
    app = Flask(__name__)

    uri = os.environ.get('DATABASE_URL')
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    login_manager.login_view = 'users.login'
    login_manager.login_message = 'Please login before access this page!'
    login_manager.login_message_category = 'warning'

    app.register_blueprint(core_bp)
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(iphone_bp, url_prefix='/iphones')

    return app