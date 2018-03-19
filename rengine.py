import models
from models import db
import pandas as pd

class REngine(object):
  """REngine interfaces with the database to query user information and computes user recommendations."""
  def __init__(self):
    self.user_list = None
    self.place_list = None

  def init(self):
    self.__set_user_list()
    self.__set_place_list()

  def get_user_list(self):
    """Returns list of users in our database."""
    if self.user_list is None:
      self.__set_user_list()
    return self.user_list

  def __set_user_list(self):
    users = models.User.query.all()
    self.user_list = [{'user_id': user.user_id,
                       'first_name': user.first_name,
                       'last_name': user.last_name} for user in users]
    self._user_id_list = [u['user_id'] for u in self.user_list]

  def get_place_list(self):
    """Returns list of places in our database."""
    if self.place_list is None:
      self.__set_place_list()
    return self.place_list

  def __set_place_list(self):
    places = models.Place.query.all()
    self.place_list = [{'place_id': place.place_id,
                  'place_name': place.place_name,} for place in places]
    self._place_id2name = {r['place_id']: r['place_name'] for r in
                           self.place_list}

  def get_friends_list(self, user_id):
    """Returns list of friends of a user."""
    if user_id not in self._user_id_list:
      return []
    else:
      friends = db.session.query(models.User) \
        .join(models.Friend,
              models.Friend.friend_user_id == models.User.user_id) \
        .filter(models.Friend.user_id == user_id).all()
      friends_list = [{'user_id': f.user_id,
                       'first_name': f.first_name,
                       'last_name': f.last_name} for f in friends]
      return friends_list

  def get_ratings_list(self,user_id):
    """Returns place ratings of a user."""
    if user_id not in self._user_id_list:
      return []
    else:
      ratings = db.session.query(models.Place, models.Rating) \
        .join(models.Rating, models.Rating.place_id == models.Place.place_id) \
        .filter(models.Rating.user_id == user_id) \
        .order_by(models.Rating.rating.desc()).all()

      ratings_list = [{'place_id': t[0].place_id,
                       'place_name': t[0].place_name,
                       'rating': t[1].rating} for t in ratings]
      return ratings_list

  def get_user_recommendations(self, user_id, rating_lower_threshold = 3, n_recommendations = 3):
    """Returns recommended places to visit for a user."""
    if user_id not in self._user_id_list:
      return []
    else:
      # List of all friends of the user
      friends_list = self.get_friends_list(user_id)
      friends_id_list = [f['user_id'] for f in friends_list]

      # Ratings of places by the friends of the user
      ratings_friends = db.session.query(models.Rating)\
                          .filter(models.Rating.user_id.in_(friends_id_list))\
                          .all()

      # We make sure that friends did rate some restaurants
      if len(ratings_friends) > 0:
        # We convert rating to pandas DataFrame
        rating_friends_pd = pd.concat(
          [pd.DataFrame([[rf.user_id, rf.place_id, rf.rating]],
                        columns=['user_id', 'place_id', 'rating'])
           for rf in ratings_friends], ignore_index=True)
        # Assigns correct type to the columns
        rating_friends_pd = rating_friends_pd.infer_objects()


        pivot_table = pd.pivot_table(rating_friends_pd, values='rating',
                                     index=['place_id'], columns=['user_id'])
        # Predicted ratings are obtained from average ratings of user's friends
        pivot_table_mean = pivot_table.mean(axis=1)
        pivot_table_mean.sort_values(ascending=False, inplace=True)

        recommendations_list = []
        # We filter recommendations that are bellow threshold and only provide n_recommendations number of recommendations
        for p_id, r in pivot_table_mean.items():
          if r >= rating_lower_threshold:
            recommendations_list.append({'place_id': p_id, 'prediction': int(r),
                                         'place_name': self._place_id2name[p_id]})
          if len(recommendations_list) >= n_recommendations:
            break
      else:
        recommendations_list = []

      # TODO: implement additional recommendations if we do not have enough recommendations by friends
      if len(recommendations_list) < n_recommendations:
        pass

      return recommendations_list