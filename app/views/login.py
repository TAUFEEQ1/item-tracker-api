from datetime import timedelta
from flask import request,jsonify
from app.models import User
from hashlib import sha256
from flask_jwt_extended import create_access_token

def hash_passkey(key:str):
    return sha256(key.encode()).hexdigest()

def login():
    username = request.form.get("username", None)
    password = request.form.get("passkey", None)
    password = hash_passkey(password)

    user:User = User.query.filter_by(username=username).first()

    if user is None  or user.password != password:
        return "Bad username or password", 401

    access_token = create_access_token(identity=username,expires_delta=timedelta(days=1))
    return jsonify(access_token=access_token,first_name=user.first_name,last_name=user.last_name,username=user.username)