from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('data.sqlite')

class User(UserMixin, Model):
  username=CharField(unique=True)
  password=CharField()
  jobseeker=BooleanField() ## True if the User is a Job seeker
  
  class Meta:
    database = DATABASE

class JobSeekerInfo(Model):
  education=CharField()
  name=CharField()
  date_of_birth=DateField()
  email=CharField()
  location=CharField()
  language=CharField()
  ethinicity=CharField()
  skillset=CharField()
  industry=CharField()
  payrange=CharField()

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User, JobSeekerInfo], safe=True)
  print('connected to database')

  DATABASE.close()
