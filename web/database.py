from peewee import *
from . import config
db = PostgresqlDatabase(host=config.host, user=config.user, password=config.password, database=config.database)

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    username = CharField()
    password = CharField()
    api_key = CharField()
    timezone = IntegerField(default=-5)

class Text(BaseModel):
    text = TextField()
    time = IntegerField()
    location = CharField()
    user = ForeignKeyField(User, related_name='texts')
