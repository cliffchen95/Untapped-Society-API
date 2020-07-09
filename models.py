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
  user=ForeignKeyField(User, backref="JobSeekerInfo")

  class Meta:
    database = DATABASE

class CompanyInfo(Model):
  user=ForeignKeyField(User, backref="CompanyInfo")
  name=CharField(unique = True)
  description=CharField()
  tagline=CharField()
  address=CharField()
  industry=CharField(null = True)
  website=CharField(null = True)
  linkedin=CharField(null = True)
  twitter=CharField(null = True)
  github=CharField(null = True)
  facebook=CharField(null = True)
  instagram=CharField(null = True)
  pinterest=CharField(null = True)
  youtube=CharField(null = True)
  employer=CharField(null = True)

  class Meta:
    database = DATABASE

class JobPost(Model):
  company=ForeignKeyField(CompanyInfo, backref="Posting")
  title=CharField()
  description=CharField()

  class Meta:
    database = DATABASE

class JobApplication(Model):
  user=ForeignKeyField(User, backref="Application")
  position=ForeignKeyField(JobPost, backref="Job")

  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables(
    [
      User, 
      JobSeekerInfo,
      CompanyInfo,
      JobPost,
      JobApplication
    ], 
    safe=True
  )
  print('connected to database')

  DATABASE.close()
