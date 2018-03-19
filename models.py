from app import db
from sqlalchemy import String, Integer

class User(db.Model):
  __tablename__ = 'users'

  user_id = db.Column(Integer, primary_key=True)
  first_name = db.Column(String)
  last_name = db.Column(String)

  def __repr__(self):
    return '<user_id: %d, first_name: %s, last_name: %s>' % (self.user_id, self.first_name, self.last_name)


class Place(db.Model):
  __tablename__ = 'places'

  place_id = db.Column(Integer, primary_key=True)
  place_name = db.Column(String)

  def __repr__(self):
    return '<place_id: %d, place_name: %s>' % (
    self.place_id, self.place_name)

class Friend(db.Model):
  __tablename__ = 'friends'

  user_id = db.Column(Integer, primary_key=True)
  friend_user_id = db.Column(Integer, primary_key=True)
  def __repr__(self):
    return '<user_id: %d, friend_user_id: %d>' % (
    self.user_id, self.friend_user_id)

class Rating(db.Model):
  __tablename__ = 'ratings'

  user_id = db.Column(Integer, primary_key=True)
  place_id = db.Column(Integer, primary_key=True)
  rating = db.Column(Integer)

  def __repr__(self):
    return '<user_id: %d, place_id: %d, rating: %d>' % (
      self.user_id, self.place_id, self.rating)