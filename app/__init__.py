from instance.config import config
from flask import Flask,  jsonify
from app.api.v1 import v1_blueprint
from app.api.v2 import v2_blueprint
from app.api.v2 import v2_blueprint
from app.api.v2.decorators import errors
from .api.v2 import v2_api
from app.api.v2.models.db import Db
from app.api.v2.models.users import User
from flask_jwt_extended import JWTManager
from app.api.v2.views import blacklist
from flask_cors import CORS
db_object = Db()

# this function returns the instance of the app


def create_app(config_name):
    """app factory creates the instance of the app"""
    app = Flask(__name__)
    db_object.create_tables()
    User.create_admin()
    jwt = JWTManager(app)
    CORS(app)
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_SECRET_KEY'] = '%****#@#'
    app.config.from_object(config[config_name])

    app.register_blueprint(v2_blueprint, url_prefix="/api/v2")
    app.register_blueprint(v1_blueprint, url_prefix="/api/v1")
    app.register_blueprint(errors)
    api = v2_api

    jwt._set_error_handler_callbacks(api)
    # this function hundles 404 errors

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist

    return app
