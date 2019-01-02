from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///mydatabase.db', echo=True)
Base = declarative_base()

class User(Base):
	__tablename__ = "nuserdata"

	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)
	email = Column(String)
	contactinfo = Column(String)
	time = Column(String)
	sex = Column(String)
	personality = Column(String)
	color = Column(String)
	welcome = Column(String)
	irritate = Column(String)
	timepass = Column(String)
	drink = Column(String)
	movies = Column(String)
	chill = Column(String)

#---------------------------------------------------------------#
	def __init__(self, username, password, email, contactinfo, time, sex, personality, color, welcome, irritate, timepass, drink, movies, chill):

		self.username = username
		self.password = password
		self.email = email
		self.contactinfo = contactinfo
		self.time = time
		self.sex = sex
		self.personality = personality
		self.color = color
		self.welcome = welcome
		self.irritate = irritate
		self.timepass = timepass
		self.drink = drink
		self.movies = movies
		self.chill = chill

#create tables
Base.metadata.create_all(engine)
