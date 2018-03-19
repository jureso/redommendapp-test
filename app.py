import os
import flask
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import pandas as pd



app = Flask(__name__,static_url_path='')
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

import models

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
  #response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/preferences_and_friends", methods=["GET"])
def user_preferences_and_friends(user_id):
  data = {}
  # TODO: check if the list should be truncated?
  data['friends_list'] = get_friends_list(user_id)
  data['ratings_list'] = get_ratings_list(user_id)
  response = flask.jsonify(data)
  #response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route("/user/<int:user_id>/recommendations", methods=["GET"])
def user_recommendations(user_id):
  data = {}
  data['recommendations'] = get_user_recommendations(user_id)
  response = flask.jsonify(data)
  #response.headers.add('Access-Control-Allow-Origin', '*')
  return response

@app.route('/')
def index():
  return app.send_static_file('index.html')

if __name__ == '__main__':
  app.run()

  # TODO: error handling and exceptions for recommendation algorithm
  # TODO: error handling and exceptions for api
  # TODO: api tests
  # TODO: api docs and recommendation algorithm docs
