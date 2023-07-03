from flask import Flask
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from .utils import db
from .auth.auth import auth_namespace
from .updates.user_profile_update import user_update_namespace
from .banks.bank import bank_namespace
from .bvn.bvnverify import bvn_namespace


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dft6562589101753'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'eff56820lops_get6312'
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=2)
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)
    db.init_app(app)
    with app.app_context():
        db.create_all()
    JWTManager(app)
    Migrate(app, db)
    api = Api(app, title='Api for Application')
    api.add_namespace(auth_namespace, path='/app_api/api')
    api.add_namespace(user_update_namespace, path='/app_api/api/update')
    api.add_namespace(bank_namespace, path='/app_api/api/bank')
    api.add_namespace(bvn_namespace, path='/app_api/api/bvn')

    return app
