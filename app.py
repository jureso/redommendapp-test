import os
import flask
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import json
app = Flask(__name__,static_url_path='')

import pandas as pd

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


def get_user_list():
  users = models.User.query.all()
  user_list = [{'user_id': user.user_id,
                'first_name': user.first_name,
                'last_name': user.last_name} for user in users]
  return user_list

def get_place_list():
  places = models.Place.query.all()
  user_list = [{'place_id': place.place_id,
                'place_name': place.place_name,} for place in places]
  return user_list

def get_friends_list(user_id):
  friends = db.session.query(models.User) \
    .join(models.Friend, models.Friend.friend_user_id == models.User.user_id) \
    .filter(models.Friend.user_id == user_id).all()
  friends_list = [{'user_id': f.user_id,
                   'first_name': f.first_name,
                   'last_name': f.last_name} for f in friends]
  return friends_list

def get_ratings_list(user_id):
  ratings = db.session.query(models.Place, models.Rating) \
    .join(models.Rating, models.Rating.place_id == models.Place.place_id) \
    .filter(models.Rating.user_id == user_id) \
    .order_by(models.Rating.rating.desc()).all()

  ratings_list = [{'place_id': t[0].place_id,
                   'place_name': t[0].place_name,
                   'rating': t[1].rating} for t in ratings]
  return ratings_list

def get_user_recommendations(user_id, rating_lower_threshold = 3, n_recommendations = 3):

  place_list = get_place_list()
  place_id2name = {r['place_id']: r['place_name'] for r in place_list}

  friends_list = get_friends_list(user_id)
  friends_id_list = [f['user_id'] for f in friends_list]

  ratings_friends = db.session.query(models.Rating)\
                      .filter(models.Rating.user_id.in_(friends_id_list))\
                      .all()


  if len(ratings_friends) > 0:
    rating_friends_pd = pd.concat(
      [pd.DataFrame([[rf.user_id, rf.place_id, rf.rating]],
                    columns=['user_id', 'place_id', 'rating'])
       for rf in ratings_friends], ignore_index=True)

    rating_friends_pd = rating_friends_pd.infer_objects()
    pivot_table = pd.pivot_table(rating_friends_pd, values='rating',
                                 index=['place_id'], columns=['user_id'])
    pivot_table_mean = pivot_table.mean(axis=1)
    pivot_table_mean.sort_values(ascending=False, inplace=True)

    recommendations_list = []
    for p_id, r in pivot_table_mean.items():
      print(p_id, r)
      if r >= rating_lower_threshold:
        recommendations_list.append({'place_id': p_id, 'prediction': int(r),
                                     'place_name': place_id2name[p_id]})
      if len(recommendations_list) >= n_recommendations:
        break
  else:
    recommendations_list = []

  if len(recommendations_list) < n_recommendations:
    # add recommendations from all users
    pass

  return recommendations_list

@app.route("/user_list", methods=["GET"])
def user_list():
  data = {}
  data['user_list'] = get_user_list()
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/preferences_and_friends", methods=["GET"])
def user_preferences_and_friends(user_id):
  data = {}
  # TODO: check if the list should be truncated?
  data['friends_list'] = get_friends_list()
  data['ratings_list'] = get_ratings_list()
  response = flask.jsonify(data)
  response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/recommendations2", methods=["GET"])
def user_recommendations2(user_id):
  data = {}
  data['recommendations'] = get_user_recommendations(user_id)
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
  from models import Friend, Rating, User, Place
  import pandas as pd
  user_id = 0
  rating_lower_threshold = 3
  n_recommendations = 3

  # rating algorithm: return 3 best restaurants, that you haven't rated yet
  # case: not enough resturants, add by average rating
  # case: to much restaurant, skip additional

  user_list = get_user_list()
  place_list = get_place_list()
  place_id2name = {r['place_id']: r['place_name'] for r in place_list}

  friends_list = get_friends_list(user_id)
  friends_id_list = [f['user_id'] for f in friends_list]

  ratings_list = get_ratings_list(user_id)

  #print(ratings)

  ratings_friends = db.session.query(models.Rating).filter(models.Rating.user_id.in_(friends_id_list)).all()
  print(ratings_friends)

  print(ratings_friends[0])
  print(ratings_friends[0].user_id)
  print(type(ratings_friends[0]))

  rating_friends_pd = pd.concat([pd.DataFrame([[rf.user_id, rf.place_id, rf.rating]],
                                              columns=['user_id', 'place_id', 'rating'])
                                              for rf in ratings_friends],ignore_index=True)
  rating_friends_pd= rating_friends_pd.infer_objects()
  pivot_table = pd.pivot_table(rating_friends_pd, values='rating', index=['place_id'], columns=['user_id'])
  pivot_table_mean = pivot_table.mean(axis=1)
  pivot_table_mean.sort_values(ascending=False, inplace=True)

  recommendations_list = []
  for p_id, r in pivot_table_mean.items():
    print(p_id, r)
    if r >= rating_lower_threshold:
      recommendations_list.append({'place_id': p_id, 'prediction': int(r), 'place_name': place_id2name[p_id]})
    if len(recommendations_list) >= n_recommendations:
      break

  if len(recommendations_list) < n_recommendations:
    # add recommendations from all users
    pass



  print(recommendations_list)

  return flask.jsonify(str(models.Place.query.get(5)))

if __name__ == '__main__':
  app.run()

  # TODO: error handling and exceptions
  # TODO: tests
  # TODO: docs
