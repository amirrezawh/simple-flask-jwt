from types import MethodType
from flask import Flask, jsonify, request
import os
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from db import db_init, db
from models import User


app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'users.db')
app.config['JWT_SECRET_KEY'] = 'super-secret'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db_init(app)


jwt = JWTManager(app)

#serializer
marsh = Marshmallow(app)
class UserSerializer(marsh.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password')

user_data = UserSerializer()


@app.route('/api/v1/write-profile', methods=["post"])
def writeProfile():
    email = request.json['email']
    username = request.json['username']
    password = request.json['password']

    if User.query.filter_by(email=email).first():
        return jsonify("Email already exists."), 403

    if User.query.filter_by(username=username).first():
        return jsonify("Username already exist.")

    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    return jsonify("User created."), 201

@app.route('/api/v1/get-profile/<int:id>')
def getProfile(id: int):
    user = User.query.filter_by(id=id).first()
    if user:
        result = user_data.dump(user)
        return jsonify(result), 200
    return jsonify("User not found"), 404

@app.route('/api/v1/login', methods=["POST"])
def login():
    if 'email' in request.json:
        email = request.json["email"]
        password = request.json["password"]
        if User.query.filter_by(email=email,password=password).first():
            token = create_access_token(identity=email)
            return jsonify(token), 201
    else:
        username = request.json["username"]
        password = request.json["password"]
        if User.query.filter_by(username=username,password=password).first():
            token = create_access_token(identity=username)
            return jsonify(token), 201
    
    return jsonify("login failed!"), 403

@app.route('/api/v1/test', methods=["GET"])
@jwt_required()
def test():
    identity = get_jwt_identity()
    return jsonify({"logged in as:" : identity}), 200