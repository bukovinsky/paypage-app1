import logging
from flask import Flask, render_template, session, redirect, url_for, request, make_response
from application.forms import MainForm, create_form
import requests
# application
from application.views import Payment
from application.models import *

# Basic configuration for logging
logging.basicConfig(filename='loggingg.log', filemode='w', level=logging.DEBUG)

STORE_SETTINGS = {
    'STORE_SECRET':'SecretKey01',
    'STORE_CURRENCY':'840',
    'shop_id':'5',
    'currencies':('978', '840', '643', '980'),
    'payway':'payeer_rub',
    #'form_fields': list(MainForm._meta.fields.keys()),
}

DATABASE = {
    'name':'database/pbase.db',
    'engine':'peewee.SqliteDatabase'
}
SECRET_KEY = 'd0231b4d850c657d6f5d31a56c68469c14ebd26ad3151dd18bde5e90b585f9c8'

CURRENCIES_METHODS = {
    '0':'',
    '978':'',
    '840':'',
    '643':'',
}


app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/', methods=['GET','POST'])
def index():
    frm = MainForm()
    if request.method=='POST':
        paym = Payment(request, STORE_SETTINGS)
        return make_response(paym.make_result(PaymentParams, 'payCurrency', request.form.get('currency')))

    return render_template('spa_application.html', frm=frm)

if __name__ == '__main__':
    app.run(debug=True)