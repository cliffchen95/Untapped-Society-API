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
	print('payload', payload)
	jobpost = JobPost.create(
		company=current_user.id,
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
	print(jobpost_dict)

	return jsonify(
		data={"jobpost": jobpost_dict},
		message=f"Successfully created job post: {jobpost_dict['title']}",
		status=201
		), 201