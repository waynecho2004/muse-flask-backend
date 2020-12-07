# import * means import everything from peewee
# Peewee: a simple and small ORM for Postgres
from peewee import *
import datetime

# Connect to a Postgres database.
DATABASE = PostgresqlDatabase('flask_music_app', host='localhost', port=5432)

class Song(Model):
    title = CharField()
    artist = CharField()
    album = CharField()
    created_at = DateTimeField(default=datetime.datetime.now)

    # Meta class provides any special instructions for the Song class object
    class Meta:
        database = DATABASE

def initialize():
    DATABASE.connect()
    DATABASE.create_tables([Song], safe=True)
    print("TABLES Created")
    # It's a good practice to close database after query is executed
    DATABASE.close() 