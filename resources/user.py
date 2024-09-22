import os
from db import db
import requests
from blocklist import BLOCKLIST
from models import UserModel
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt
from schemas import UserSchema, UserRegisterSchema
from passlib.hash import pbkdf2_sha256
from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

blp = Blueprint("users", __name__, description="Operation on users")

# send simple mail from mailgun client to the registered used each time you register using your username and email id
def send_simple_message(to, subject, body):
    domain = os.getenv("MAILGUN_DOMAIN")
    return requests.post(
  		f"https://api.mailgun.net/v3/{domain}/messages",
  		auth=("api", os.getenv("MAILGUN_API_KEY")),
  		data={"from": f"Excited User <mailgun@{domain}>",
  			"to": [to],
  			"subject": subject,
  			"text": body})

# NOTE: Currently we have added JWT requirement i.e Bearer token requirement for only item and user. We can extend it to other entities such as stores and tags too

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserRegisterSchema)
    def post(self, user_data):
        # find if there already exists a user with the given username or email. remember get_or_404 doesn't take kwargs as arguments hence we need to use filter to see if a user with username exists
        try:
            user = UserModel.query.filter(
                or_(
                UserModel.username == user_data["username"], 
                UserModel.email == user_data["email"]
                )
            ).first()
        except IntegrityError:
            abort(409, message="User with this username or email already exists in database.")

        user = UserModel(
            username=user_data["username"],
            email=user_data["email"],
            password=pbkdf2_sha256.hash(user_data["password"]) 
        )
        db.session.add(user)
        db.session.commit()

        # send a successful sign up message to the email id of the user.
        send_simple_message(
            to=user.email,
            subject="Successfully signed up.",
            body=f"Hi {user.username}! You have successfully signed up for the Stores REST API."
        )

        return {"message": "User created successfully."}, 201

@blp.route("/refresh")
class TokenRefresh(MethodView):
    @jwt_required(refresh=True) # refresh=True signifies that this endpoint requires a refresh token
    def post(self):
        current_user = get_jwt_identity() # get_jwt_identity will give us the user id in this case since we set identity=user.id
        new_token = create_access_token(identity=current_user, fresh=False) # create new access token that is non fresh
         # Make it clear that when to add the refresh token to the blocklist will depend on the app design
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti)
        return {"access_token": new_token}, 200

@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        # check if user with a username exists in db
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        # if user exists and it's password matches the hashed password then we will grant the access token to the user
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True) # fresh=True specifies that this is a new and fresh token for a user session
            refresh_token = create_refresh_token(identity=user.id) # refresh token is being created so that the endpoints that are hit frequently do not require fresh tokens each time as fresh tokens may generate after just a span of minutes causing irritation to the user as they would require loggin in again and again. 
            #Hence we create refresh tokens. These tokens will be refreshed each time we hit refresh endpoint. However for critical operations such as deletes, we will always prefer to use a fresh token 

            send_simple_message(
                to=user.email,
                subject="Successfully logged in.",
                body=f"Hi {user.username}! You have successfully logged in for the Stores REST API."
            )

            return {"access_token": access_token, "refresh_token": refresh_token}
        
        abort(404, message="User Not Found.")

@blp.route("/logout")
class UserLogout(MethodView):
    # add jwt to blocklist at the time of logout so that the access token can no longer be repeated
    @jwt_required()
    def post(self):
        jwt = get_jwt()
        BLOCKLIST.add(jwt.get("jti"))
        return {"message":"Succesfully logged out."}


@blp.route("/users")
class GetUsers(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema(many=True)) # without this blp.response decorator, it would throw error in the return user statement at the end of the method. It will complain saying expected was a json but received a UserObject. the decorator jsonifies the userobject implicitly
    def get(self):
       return UserModel.query.all()

@blp.route("/user/<int:user_id>")
class User(MethodView):
    @jwt_required()
    @blp.response(200, UserSchema) # without this blp.response decorator, it would throw error in the return user statement at the end of the method. It will complain saying expected was a json but received a UserObject. the decorator jsonifies the userobject implicitly
    def get(self, user_id):
       user = UserModel.query.get_or_404(user_id)
       return user

    @jwt_required()
    def delete(self, user_id):
       user = UserModel.query.get_or_404(user_id)
       db.session.delete(user)
       db.session.commit()
       return {"message": "User deleted successfully."}, 200

