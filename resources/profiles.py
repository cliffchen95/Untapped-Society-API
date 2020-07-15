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
  print(payload)
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
    photo=payload['photo'],
    user=current_user.id
  )
  profile_dict = model_to_dict(profile)
  profile_dict['user'].pop('password')

  return jsonify(
    data={"profile": profile_dict},
    message=f"Successfully set up profile for user {profile_dict['user']['username']}",
    status=201
  ), 201


## profiles/update
## Profile update route: update specific field of information
@profiles.route('/update/<id>', methods=['PATCH'])
@login_required
def update_profile(id):
  payload = request.get_json()

  try:
    JobSeekerInfo.update(payload).where(
        (JobSeekerInfo.id == id) & 
        (JobSeekerInfo.user_id == current_user.id)).execute()
    updated = JobSeekerInfo.get_by_id(id)
    updated_dict = model_to_dict(updated)
    updated_dict['user'].pop('password')
    return jsonify(
      data={"updated_profile": updated_dict},
      message=f"Successfully updated profile with id {id}",
      status=200
    ), 200

  except models.DoesNotExist:
    return jsonify(
      data={},
      message="Profile not avaliable to update",
      status=400
    ), 400

## profiles/get
## Get current user's profile to display details
@profiles.route('/view/<id>', methods=['GET'])
@login_required
def view_profile(id):
    print('YAY')
    profile = models.JobSeekerInfo.get(JobSeekerInfo.id == current_user.id)
    profile_dict = model_to_dict(profile)
    profile_dict['user'].pop('password')
    
    return jsonify(profile_dict)

    return 'no'





