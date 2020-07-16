import models

JobPost = models.JobPost

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

jobposts = Blueprint('jobpost', 'jobpost')

# create a post
@jobposts.route('/create', methods=['POST'])
@login_required
def jobpost_create():
	payload = request.get_json()

	jobpost = JobPost.create(
		company=payload['company'],
		title=payload['title'],
	  description=payload['description'],
	  function=payload['function'],
	  officelocation=payload['officelocation'],
	  jobtype=payload['jobtype'],
	  educationlevel=payload['educationlevel'],
	  careerlevel=payload['careerlevel'],
	  compensation=payload['compensation']
		)

	jobpost_dict = model_to_dict(jobpost)
	jobpost_dict['company']['user'].pop('password')

	return jsonify(
		data={"jobpost": jobpost_dict},
		message=f"Successfully created job post: {jobpost_dict['title']}",
		status=201
		), 201

# view all jobs posted
@jobposts.route('/all', methods=['GET'])
def view_all_jobs():
	jobs = models.JobPost.select()
	
	jobs_dict = [model_to_dict(job) for job in jobs]
	
	for job in jobs_dict:
		job['company']['user'].pop('password')

	return jsonify(
		data = jobs_dict,
		message = f"Found all {len(jobs_dict)} posts",
		status = 200
	), 200

#update post
@jobposts.route('/update/<id>', methods=['PATCH'])
@login_required
def update_jobpost(id):
	payload = request.get_json()

	print(current_user)

	try: # if post id == id AND if company's user id = current user id
		JobPost.update(payload).where(
			(JobPost.id == id) & (
			JobPost.company_id == current_user.id) # is this correct
		).execute()
		
		updated = JobPost.get_by_id(id)
		updated_dict = model_to_dict(updated)
		updated_dict['company']['user'].pop('password')


		return jsonify(updated_dict)

	except models.DoesNotExist:
    
		return jsonify(
			data={},
			message="Post not avaliable to update",
			status=400
		), 400

	return "check term"

#destroy post
@jobposts.route('/delete/<id>', methods=['DELETE'])
@login_required
def delete_jobpost(id):

	jobpost = JobPost.get_by_id(id)
	jobpost_dict = model_to_dict(jobpost)

	if jobpost_dict['company']['user']["id"] == current_user.id:
		jobpost.delete_instance()

		return jsonify(
			data = {},
			message = f"Job post {jobpost_dict['title']} successfully deleted",
			status = 200
			), 200

	else:

		return jsonify(
			data = {},
			message = f"The current user does not have permission to delete this job post",
			status = 403
		), 403
