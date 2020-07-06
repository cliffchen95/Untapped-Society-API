import models

JobSeekerInfo = models.JobSeekerInfo

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

profiles = Blueprint('profiles', 'profiles')

## profiles/create
## Profile create route: create a profile related to the current user
@profiles.route('/create', methods=['POST'])
@login_required
def create_profile():
  payload = request.get_json()
  profile = JobSeekerInfo.create(
    education=payload['education'],
    name=payload['name'],
    date_of_birth=payload['date_of_birth'],
    email=payload['email'],
    location=payload['location'],
    language=payload['language'],
    ethinicity=payload['ethinicity'],
    skillset=payload['skillset'],
    industry=payload['industry'],
    payrange=payload['payrange'],
    user=current_user.id
  )
  profile_dict = model_to_dict(profile)
  profile_dict['user'].pop('password')

  return jsonify(
    data={"profile": profile_dict},
    message=f"Successfully set up profile for user {profile_dict['user']['username']}",
    status=201
  ), 201
  