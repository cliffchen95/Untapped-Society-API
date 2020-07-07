import models

User = models.User

from flask import Blueprint, request, jsonify
from flask_login import login_user, current_user, logout_user, login_required

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

## user/login
## User login route
@users.route('/login', methods=["POST"])
def user_login():
  payload = request.get_json()
  payload['username'] = payload['username'].lower() ## usernames are not case sensitive
  
  try:
    user = User.get(User.username == payload['username'])
    user_dict = model_to_dict(user)
    if payload['password'] == user_dict['password']: ## Correct password
      login_user(user)
      user_dict.pop('password')
      return jsonify(
        data=user_dict,
        message=f"Successfully logged in {user_dict['username']}",
        status=200
      ), 200
    else:  ## Incorrect password
      return jsonify(
        data={},
        message="Incorrect password/username",
        status=401
      ), 401

  except models.DoesNotExist:  ## Incorrect username
    return jsonify(
      data={},
      message="Incorrect username/password",
      status=401
    ), 401

## user/logout
## User logout route
@users.route('logout', methods=['GET'])
@login_required
def user_logout():
  logout_user()
  return jsonify(
    data={},
    message="Successfully logged out",
    status=200
  ), 200

## user/update
## User update route
@users.route('update', methods=['PATCH'])
@login_required
def user_update():
  payload = request.get_json()

  User.update(payload).where(
    User.id == current_user.id).execute()
  
  return jsonify(
    data={},
    message=f"Successfully updated user with id {current_user.id}",
    status=200
  ), 200
