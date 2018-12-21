import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tabledef import *

engine = create_engine('sqlite:///mydatabase.db', echo = True)

Session = sessionmaker(bind=engine)
sess = Session()

user = User("admin", "password")
sess.add(user)

user = User("satyam", "satyam56")
sess.add(user)

user = User("dummy", "1234")
sess.add(user)

#commit to record to database
sess.commit()