# Run this file in order to create the necessary tables
from web.database import *
from peewee import create_model_tables
create_model_tables([User, Text])
