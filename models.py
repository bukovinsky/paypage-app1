import datetime
from peewee import *

pay_db = SqliteDatabase('database/pay.db')

class Currency(Model):
    code = IntegerField()
    name = CharField(unique=True)
    class Meta:
        database = pay_db

class MethodSetting(Model):
    qwe = TextField()
    link = TextField()
    method = TextField()
    fields = TextField()


class RegisteredOperation(Model):
    currency = ForeignKeyField(Currency, backref='registeredoperations')
    amount = DecimalField(decimal_places=2)
    dttime_oper = DateTimeField(default=datetime.datetime.now)
    description = TextField()
    order_id = IntegerField()
    class Meta:
        database = pay_db
"""
class PaymentParams(Model):
    payMethod = CharField()
    payCurrency = ForeignKeyField(Currency)
    requirementFields = CharField()
    method = CharField()
    action = CharField()
    class Meta:
        database = pay_db
"""

pay_db.connect()
pay_db.create_tables([Currency, RegisteredOperation])#PaymentParams

#param = PaymentParams.get(PaymentParams.payCurrency==Currency.get(Currency.code==840))

#print(param)