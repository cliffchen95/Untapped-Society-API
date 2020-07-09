import models

JobApplication = models.JobApplication

from flask import Blueprint, request, jsonify
from flask_login import current_user, login_required

from playhouse.shortcuts import model_to_dict

jobapplications = Blueprint('jobapplication', 'jobapplication')

