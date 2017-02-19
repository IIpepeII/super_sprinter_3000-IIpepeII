from flaskr.connectdatabase import ConnectDatabase
from peewee import *


class Userstories(Model):

    story_title = CharField(default="nothing")
    user_story = TextField(default="anything")
    acceptance_criteria = TextField(default="something")
    business_value = IntegerField(default=100)
    estimation = FloatField(default=0.5)
    status = CharField(default='1')


    class Meta:
        database = ConnectDatabase.db