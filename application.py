from flask import Flask, render_template, redirect, request, make_response
import requests
from forms import *
from hashlib import sha256
from models import *
from views import *


STORE_SETTINGS = {
    'payway':'payeer_rub',
    'secret_key':'SecretKey01',
    'store_currency':'840',
    'shop_id':'5',
    'shop_order_id':'53861',
    'ways':{
        'eur':{
            'method':'GET',
            'link':'https://pay.piastrix.com/ru/pay'
        },
        'rub':{
            'method':'POST',
            'link':'https://core.piastrix.com/invoice/create'
        },
        'usd':{
            'method':'POST',
            'link':'https://core.piastrix.com/bill/create'
        }
    }
}

app = Flask(__name__)



"""
    Запись в базу на основе существующей формы.
    -- data
"""
def record_to_database(forModel, data):
    db.connect()
    forModel.create(**data)

@app.route('/', methods=['GET', 'POST'])
def main_application():
    frm = MainForm()
    if request.method=='POST':
        cur = request.form.get('currency')
        frm = request.form.to_dict()
        data = {**frm,**STORE_SETTINGS}
        std_keys=('currency','shop_id','shop_order_id','amount','payway')
        
        if cur=='978':
            data['sign']=create_sign(std_keys[:-1], **data)
            l_form = create_form(('currency','shop_id','shop_order_id','amount','sign'), data)
            return render_template('form_template.html', resform=l_form, context={'method':'GET', 'action':data['ways']['eur']['link']})

        elif cur=='840':
            req_keys = ('payer_currency','shop_currency','shop_id','shop_order_id','shop_amount')
            payload = {
                'payer_currency':data.get('currency'),
                'shop_currency':data.get('store_currency'),
                'shop_id':data.get('shop_id'),
                'shop_order_id':data.get('shop_order_id'),
                'shop_amount':data.get('amount'),
            }
            payload['sign']=create_sign(req_keys, **{**payload, \
                'secret_key':data['secret_key']})
            post_r = requests.post('https://core.piastrix.com/bill/create', json=payload)
            return redirect(post_r.json().get('data').get('url'))

        elif cur=='643':
            payload = {}.fromkeys(std_keys)
            for key in payload.keys():
                payload[key]=data.get(key)
            post_r = requests.post('https://core.piastrix.com/invoice/create',\
                json={**payload, 'sign':create_sign(std_keys, **{**payload, 'secret_key':data['secret_key']})})
            r_data = post_r.json().get('data')
            print(r_data.get('data'))
            fm = create_form(r_data.get('data').keys(), r_data.get('data'))
            print(r_data.get('method'))
            print(post_r.json())
            return render_template('form_template.html', resform=fm, context={'method':'GET', 'action':r_data.get('url')})
    else:
        return render_template('spa_application.html', frm=frm)


if __name__ == '__main__':
    app.run(debug=True)