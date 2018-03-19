import os
import flask
from flask import Flask, abort
from models import db

app = Flask(__name__,static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from rengine import REngine
re = REngine()

@app.route("/user_list", methods=["GET"])
def user_list():
  """Returns a list of users in our recommender system."""
  try:
    data = {}
    data['user_list'] = re.get_user_list()
  except Exception as e:
    print(e)
    abort(400)
  response = flask.jsonify(data)
  return response

@app.route("/user/<int:user_id>/preferences_and_friends", methods=["GET"])
def user_preferences_and_friends(user_id):
  """For a given user_id return a list of user's friends and places ratings."""
  try:
    data = {}
    data['friends_list'] = re.get_friends_list(user_id)
    data['ratings_list'] = re.get_ratings_list(user_id)
  except Exception as e:
    print(e)
    abort(400)
  response = flask.jsonify(data)
  return response

@app.route("/user/<int:user_id>/recommendations", methods=["GET"])
def user_recommendations(user_id):
  """For a give user_id returns a list of places that the user should visit."""
  try:
    data = {}
    data['recommendations'] = re.get_user_recommendations(user_id)
  except Exception as e:
    print(e)
    abort(400)
  response = flask.jsonify(data)
  return response

@app.route('/')
def index():
  return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run()

  #TODO: When an account is selected on the UI recommendations of places to go should be listed for that account with probabilities % that the match is appropriate
