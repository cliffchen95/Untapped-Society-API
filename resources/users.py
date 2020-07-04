import models

User = models.User

from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user

from playhouse.shortcuts import model_to_dict

users = Blueprint('users', 'users')

## /user/create
## User create route, create a new user
@users.route('/create', methods=['POST'])
def user_create():
  payload = request.get_json()
  payload['username'] = payload['username'].lower() ## usernames are not case sensitive

  try:
    User.get(User.username == payload['username'])
    return jsonify(
      data={},
      message=f"A user with username {payload['username']} already exists",
      status=401
    ), 401
  except models.DoesNotExist:
    created_user = User.create(
      username=payload['username'],
      password=payload['password'],
      jobseeker=True
    )

    login_user(created_user)

    created_user_dict = model_to_dict(created_user)
    created_user_dict.pop('password')

    return jsonify(
      data=created_user_dict,
      message=f"Successfully created a new user",
      status=201
    ), 201