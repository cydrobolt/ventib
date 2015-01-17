from peewee import *
from . import config
db = PostgresqlDatabase(host='104.131.66.35', user='pennappsxi', password=config.password)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    password = CharField()
    api_key = CharField()

class Text(BaseModel):
    text = TextField()
    time = IntegerField()
    location = CharField()
    user = ForeignKeyField(User, related_name='texts')
