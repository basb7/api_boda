import random

from datetime import datetime
from peewee import *


db = SqliteDatabase("./Database.db")


class Assistants(Model):
    names = CharField(max_length=20)
    telephone = CharField(max_length=15, null=True)
    cant_tikets = IntegerField()
    code = IntegerField()
    created_at = DateTimeField(default=datetime.now())
    confirmed = BooleanField(default=False)
    confirmation_date = DateTimeField(null=True)

    class Meta:
        database = db  # This model uses the "Database.db" database.


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
        user = Assistants.get_or_none(
            (Assistants.code == int(code)) & (Assistants.confirmed == True)
        )

        return user
    except Exception as e:
        print(e)
    finally:
        db.close()


def create(_names: str, _telephone: str, _cant_tikets: int, _code: int):
    try:
        db.connect()
        assistant = Assistants.create(
            names=_names, telephone=_telephone, cant_tikets=_cant_tikets, code=_code
        )
        assistant.save()
        return assistant
    except Exception as e:
        print(e)
    finally:
        db.close()


def get_all():
    try:
        db.connect()
        list = []
        for user in Assistants.select().dicts():
            list.append(user)

        return list
    except Exception as e:
        print(e)
    finally:
        db.close()
