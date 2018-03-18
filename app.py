import os
import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__,static_url_path='')

import config
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


import models

users = {}
users[0] = {'user_id': 0, 'first_name': 'Jure', 'last_name': 'Sokolic'}
users[1] = {'user_id': 1, 'first_name': 'Neja', 'last_name': 'Markocic'}
users[2] = {'user_id': 2, 'first_name': 'Zarja', 'last_name': 'Cibej'}
users[3] = {'user_id': 3, 'first_name': 'Faris', 'last_name': 'Zacina'}

preferences = {}
preferences[0] = [{'place_id': 0, 'name': 'McDonalds'}, {'place_id': 4, 'name': 'Wasabi'}]
preferences[1] = [{'place_id': 4, 'name': 'Wasabi'}]
preferences[2] = []
preferences[3] = []

friends = {}
friends[0] = [{'user_id': 1, 'first_name': 'Neja', 'last_name': 'Markocic'}, {'user_id': 2, 'first_name': 'Zarja', 'last_name': 'Cibej'}]
friends[1] = []
friends[2] = [{'user_id': 1, 'first_name': 'Neja', 'last_name': 'Markocic'}]
friends[3] = []

@app.route("/user_list", methods=["GET"])
def user_list():
  data = {}
  data['user_list'] = list(users.values())
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/preferences", methods=["GET"])
def user_preferences(user_id):
  data = {}
  data['preferences'] = preferences[user_id]
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/friends", methods=["GET"])
def user_friends(user_id):
  data = {}
  data['friends'] = friends[user_id]
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/recommendations", methods=["GET"])
def user_recommendations(user_id):
  data = {}
  data['recommendations'] = preferences[user_id]
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response


@app.route("/recommend/<int:user_id>", methods=["GET"])
def recommend(user_id):
  recommendations = {}
  recommendations['recommendations'] = ['McDonalds', 'Wahaca', str(user_id)]
  return json.dumps(recommendations)


@app.route('/')
def index():
  return app.send_static_file('index.html')

@app.route('/test_db')
def test_db():
  print(models.Place.query.get(5))
  return flask.jsonify(str(models.Place.query.get(5)))

if __name__ == '__main__':
  app.run()

