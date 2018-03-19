import os
import flask
from flask import Flask, abort
from models import db

app = Flask(__name__,static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

from rengine import get_ratings_list, get_friends_list, get_user_list, get_user_recommendations

@app.route("/user_list", methods=["GET"])
def user_list():
  data = {}
  data['user_list'] = get_user_list()
  response = flask.jsonify(data)
  return response

@app.route("/user/<int:user_id>/preferences_and_friends", methods=["GET"])
def user_preferences_and_friends(user_id):
  data = {}
  data['friends_list'] = get_friends_list(user_id)
  data['ratings_list'] = get_ratings_list(user_id)
  response = flask.jsonify(data)
  return response

@app.route("/user/<int:user_id>/recommendations", methods=["GET"])
def user_recommendations(user_id):
  if user_id > 10:
    abort(400)

  data = {}
  data['recommendations'] = get_user_recommendations(user_id)
  response = flask.jsonify(data)
  return response

@app.route('/')
def index():
  return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run()

  # TODO: refactor database queries and recommendations and api
  # Create global recommender class that load users and computes recommendations.
  # Have app call this class functions and in the case of failure send abort messages!

  # TODO: error handling and exceptions for recommendation algorithm
  # TODO: error handling and exceptions for api
  # TODO: api tests
  # TODO: api docs and recommendation algorithm docs
