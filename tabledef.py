from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import UniqueConstraint
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

engine = create_engine('sqlite:///mydatabase.db', echo=True)

Base = declarative_base()

class User(Base):
	__tablename__ = "userdata"

	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)
	sex = Column(String)
	pet = Column(String)

#---------------------------------------------------------------#
	def __init__(self, username, password, sex, pet):

		self.username = username
		self.password = password
		self.sex = sex
		self.pet = pet

#create tables
Base.metadata.create_all(engine)