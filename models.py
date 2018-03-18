from app import db
from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Session

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

def example_1():
  from sqlalchemy import create_engine
  db_string = "postgresql://localhost/recommend_app_test"
  db = create_engine(db_string)

  # Read
  result_set = db.execute("SELECT * FROM users")
  for r in result_set:
    print(r)

def example_2():
  from sqlalchemy import create_engine
  from sqlalchemy import Table, Column, String, MetaData, Integer

  db_string = "postgresql://localhost/recommend_app_test"
  db = create_engine(db_string)
  meta = MetaData(db)
  user_table = Table('users', meta,
                       Column('user_id', Integer),
                       Column('first_name', String),
                       Column('last_name', String))
  with db.connect() as conn:
    #user_table.create()
    select_statement = user_table.select()
    result_set = conn.execute(select_statement)
    for r in result_set:
      print(r)

def example_3():
  from sqlalchemy import create_engine
  from sqlalchemy import Column, String, Integer
  from sqlalchemy.ext.declarative import declarative_base
  from sqlalchemy.orm import sessionmaker

  db_string = "postgresql://localhost/recommend_app_test"
  db = create_engine(db_string)
  base = declarative_base()
  class User(base):
    __tablename__ = 'users'

    user_id = Column(Integer,primary_key=True)
    first_name = Column(String)
    last_name = Column(String)

  Session = sessionmaker(db)
  session = Session()
  base.metadata.create_all(db)

  users = session.query(User)
  for user in users:
    print(user.user_id, user.first_name)

if __name__=='__main__':



  #DBSession = scoped_session(sessionmaker())
  #print(DBSession)

  #lUsers = DBSession.query(User)  # returns a Query object.
  #print(lUsers)

  #base = declarative_base()
  Session = sessionmaker(db)
  session = Session()
  #db.Model.metadata.create_all(db)

  users = session.query(User)
  for user in users:
    print(user.user_id, user.first_name)

  #example_1()
  #example_2()
  example_3()
  #for user in lUsers:
  #  print(user)
  #  #print(user.user_id, user.first_name)

