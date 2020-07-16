from flask import Flask, jsonify, g
from flask_login import LoginManager

import os
from flask_cors import CORS

import models
from resources.users import users
from resources.profiles import profiles
from resources.jobposts import jobposts
from resources.companies import companies
from resources.jobapplications import jobapplications

PORT=8000
DEBUG=True

app = Flask(__name__)

app.secret_key = "os.environ.get('SECRET_KEY')"

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
  try:
    print("loading the following user")
    user = models.User.get_by_id(user_id)
    return user
  except models.DoesNotExist:
    return None

## unauthorized handler, called after login_required call and 
## no user is logged in
@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': 'User not logged in'
    },
    message="You must be logged in",
    status=401
  ), 401

## CORS implementation
CORS(users, origins=['http://localhost:3000', 'https://untapped-society.herokuapp.com'], supports_credentials=True)
CORS(profiles, origins=['http://localhost:3000', 'https://untapped-society.herokuapp.com'], supports_credentials=True)
CORS(jobposts, origins=['http://localhost:3000', 'https://untapped-society.herokuapp.com'], supports_credentials=True)
CORS(companies, origins=['http://localhost:3000', 'https://untapped-society.herokuapp.com'], supports_credentials=True)
CORS(jobapplications, origins=['http://localhost:3000', "https://untapped-society.herokuapp.com"], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(profiles, url_prefix='/api/v1/profiles')
app.register_blueprint(jobposts, url_prefix='/api/v1/jobposts')
app.register_blueprint(companies, url_prefix='/api/v1/companies')
app.register_blueprint(jobapplications, url_prefix='/api/v1/jobapplications')

@app.before_request
def before_request():
  g.db = models.DATABASE
  g.db.connect()

@app.after_request
def after_request(response):
  g.db.close()
  return response

@app.route('/')
def hello():
  return 'Server running'

if 'ON_HEROKU' in os.environ: 
  print('\non heroku!')
  models.initialize()

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)