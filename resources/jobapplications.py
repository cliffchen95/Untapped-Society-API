import models

JobApplication = models.JobApplication

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

jobapplications = Blueprint('jobapplication', 'jobapplication')

# create 
# when user clicks apply, it adds their profile info onto the job post they click on
# id in route is job post id
@jobapplications.route('/<id>/create', methods=['POST'])
@login_required
def apply_to_job(id):

	jobpost = models.JobPost.get_by_id(id)

	userprofile = models.JobSeekerInfo.get(
		models.JobSeekerInfo.user_id == current_user.id)

	jobapplication = JobApplication.create(
		jobseeker = current_user.id,
		position = jobpost
		)

	jobapplication_dict = model_to_dict(jobapplication)
	jobapplication_dict['position']['company']['user'].pop('password')
	jobapplication_dict['jobseeker']['user'].pop('password')

	return jsonify(jobapplication_dict)
	# return "hi"

# read
# person who posted job should be able to see all applicants 
# id in route is job post id
@jobapplications.route('/all/<id>', methods=['GET'])
@login_required
def view_applications(id):

	jobpost = models.JobPost.get_by_id(id)
	jobpost_dict = model_to_dict(jobpost)

	#if the current user is associated w the job post company id 
	if current_user.id == jobpost_dict['company']['user']['id']:
		
		#get all applications that are associated with this job post
		applications = JobApplication.select().where(JobApplication.position_id == id)
		application_dicts = [model_to_dict(application) for application in applications]

		for application_dict in application_dicts:
			application_dict['jobseeker']['user'].pop('password')
			application_dict['position']['company']['user'].pop('password')

		return jsonify(application_dicts)

	else:
		return jsonify(
			data={},
			message="Job post not avaliable to view",
			status=400
		), 400


	return jsonify(jobpost_dict)










