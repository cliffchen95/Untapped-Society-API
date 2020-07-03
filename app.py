from flask import Flask 

PORT=8000
DEBUG=True

app = Flask(__name__)

@app.route('/')
def hello():
  return 'Server running'

if __name__ == '__main__':
  app.run(debug=DEBUG, port=PORT)