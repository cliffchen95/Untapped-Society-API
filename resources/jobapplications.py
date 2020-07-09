import models

JobApplication = models.JobApplication

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

jobapplications = Blueprint('jobapplication', 'jobapplication')

# create 
# when user clicks apply, it adds their profile info onto the job post they click on
@jobapplications.route('/<id>/create', methods=['POST'])
@login_required
def apply_to_job(id):
	# current user details need to be associated with job post that matches the id?

	jobpost = models.JobPost.get_by_id(id)
	print(current_user.id)

	userprofile = models.JobSeekerInfo.get(
		models.JobSeekerInfo.user_id == current_user.id)

	print("userprofile", userprofile)

	jobapplication = JobApplication.create(
		jobseeker = current_user.id,
		position = userprofile
		)

	jobapplication_dict = model_to_dict(jobapplication)
	jobapplication_dict['position']['company']['user'].pop('password')
	jobapplication_dict['jobseeker']['user'].pop('password')

	return jsonify(jobapplication_dict)
	# return "hi"

# read
# person who posted job should be able to see all applicants 
@jobapplications.route('/<id>/all', methods=['GET'])
@login_required
def view_applications(id):
	#if the current user is associated w the job post company id 


	return "view_applications"