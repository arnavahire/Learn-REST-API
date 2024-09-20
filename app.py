
import os
from flask import Flask, jsonify
from flask_smorest import Api 
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from dotenv import load_dotenv
import models
from db import db
from blocklist import BLOCKLIST
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tag import blp as TagBlueprint
from resources.user import blp as UserBlueprint

def create_app(db_url=None):

    app = Flask(__name__) # Flask Convention
    load_dotenv()

    #App configuration
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores Rest Api" 
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"  #  creates a swagger ui url at <localhost:port/swagger-ui>
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") # if database url exists to connect to db client then use that, otherwise sqlite will be used by default
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # connect sqlAlchemy to the flask app using init_app
    db.init_app(app)
    migrate = Migrate(app, db) # this will create database tables using flask-migrate

    # connects flask app to flask_smorest functionality
    api = Api(app)

    # config for setting up jwt for user authentication
    app.config["JWT_SECRET_KEY"] = "291470591102923449172424126390369569460"
    JWT = JWTManager(app)

    # in case a fresh token is not provided for an endpoint where fresh token is a must (delete item endpoint in our case), the following error message would be thrown
    @JWT.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return(
            jsonify({"description": "Token is not fresh.", "error": "Fresh token required."}),
            401
        )


    # check if the jwt payload has the token which is in blocklist
    @JWT.token_in_blocklist_loader
    def check_if_token_in_blocklsit(jwt_header, jwt_payload):
        return jwt_payload["jti"] in BLOCKLIST

    # revoke the token at the time of logout
    @JWT.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"description":"The token has been revoked", "error":"token revoked"}),
            401
        )

    # We can use JWT to add or use additional headers that we could use in our logic. additional_claims_loader get called when jwt is being created.
    # In this case our goal is to find out if a user is admin and if the user is admin then we can perform delete operation on item. If not an admin then user can't delete item from database.
    # So we will create a header called is_admin which will have True value when identity is 1  . i.e if user id is 1. All other user ids are considered non-admins. We can change that to any number for testing. We are just using identity=1 for example
    @JWT.additional_claims_loader
    def add_claims_to_jwt(identity): # grabbed from /login method of the user
        if identity == 1:
            return {"is_admin":True}
        return {"is_admin":False}

    # JWT custom error message we created which will be thrown when the token used is expired
    @JWT.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return(
            jsonify({"message": "Your token has expired.", "error":"Token expired"}),
            401
        )

    # JWT custom error message we created which will be thrown when an invalid token is used
    @JWT.invalid_token_loader
    def invalid_token_callback(error):
        return(
            jsonify({"message":"Invalid token has been used.", "error":"Invalid token"}),
            401
        )

    # JWT custom error message we created which will be thrown when no token is used
    @JWT.unauthorized_loader
    def missing_token_callback(error):
        return(
            jsonify({"message":"No token has been used.", "error":"Missing token"})
        )

    # NOTE: Not required since we are using flask-migrate to create database tables
    # # create all tables
    # with app.app_context():
    #     db.create_all()

    #register blueprints
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(TagBlueprint)
    api.register_blueprint(UserBlueprint)

    return app
