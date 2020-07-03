from flask import Flask 

import models

PORT=8000
DEBUG=True

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Server running'

if __name__ == '__main__':
  models.initialize()
  app.run(debug=DEBUG, port=PORT)