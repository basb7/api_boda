import random

from datetime import datetime
from peewee import *


db = SqliteDatabase('./Database.db')

class Assistants(Model):
    name = CharField(max_length=20)
    lastname = CharField(max_length=20)
    telephone = CharField(max_length=15)
    code = IntegerField(default=random.randint(100,999))
    created_at = DateTimeField(default=datetime.now())
    confirmed = BooleanField(default=False)
    confirmation_date = DateTimeField(null=True)

    class Meta:
        database = db # This model uses the "Database.db" database.


def create_tables():
    try:
        db.connect()
        db.create_tables([Assistants])
    except Exception as e:
        print(e)
    finally:
        db.close()


def get(code: int):
    try:
        db.connect()
        user = Assistants.get_or_none(Assistants.code == int(code))
        
        # update confirmed to True
        if user:
            user.confirmed = True
            user.confirmation_date = datetime.now()
            user.save()
        
        return user
    except Exception as e:
        print(e)
    finally:
        db.close()


def check_confirmed(code: int):
    try:
        db.connect()
        user = Assistants.get_or_none((Assistants.code == int(code)) & (Assistants.confirmed == True))

        return user
    except Exception as e:
        print(e)
    finally:
        db.close()


def create():
    try:
        db.connect()
        assistant = Assistants.create(name="Juan", lastname="Perez", telephone="99999999", code=321)
        assistant.save()
        return assistant
    except Exception as e:
        print(e)
    finally:
        db.close()