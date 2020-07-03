from peewee import *

DATABASE = SqliteDatabase('data.sqlite')

class User(Model):
  username=CharField(unique=True)
  password=CharField()
  jobseeker=BooleanField() ## True if the User is a Job seeker
  class Meta:
    database = DATABASE

def initialize():
  DATABASE.connect()
  DATABASE.create_tables([User], safe=True)
  print('connected to database')

  DATABASE.close()
