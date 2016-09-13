from mongoengine import *

class ClassifiedCategory(Document):
    result_id = StringField()
    text = StringField()
