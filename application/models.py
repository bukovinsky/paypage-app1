import datetime
from peewee import *
from flask_peewee import *

pay_db = SqliteDatabase('database/pay.db')

class Currency(Model):
    code = IntegerField()
    name = CharField(unique=True)
    class Meta:
        database = pay_db

class RegisteredOperation(Model):
    currency = ForeignKeyField(Currency, backref='registeredoperations')
    amount = DecimalField(decimal_places=2)
    dttime_oper = DateTimeField(default=datetime.datetime.now)
    description = TextField()
    class Meta:
        database = pay_db

class PaymentParams(Model):
    payMethod = TextField()
    payCurrency = ForeignKeyField(Currency)
    requirementFields = TextField()
    method = TextField(default='GET')
    action = TextField()
    class Meta:
        database = pay_db

pay_db.connect()
pay_db.create_tables([Currency, RegisteredOperation, PaymentParams])