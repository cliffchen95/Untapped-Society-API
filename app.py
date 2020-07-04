from flask import Flask 
from flask_login import LoginManager

import models
from resources.users import users

PORT=8000
DEBUG=True

app = Flask(__name__)

app.secret_key = "somekey"

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

@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': 'User not logged in'
    },
    message="You must be logged in",
    status=401
  ), 401

app.register_blueprint(users, url_prefix='/api/v1/users')

@app.route('/')
def hello():
  return 'Server running'

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)