import logging
import requests

from hashlib import sha256
from flask import render_template, make_response, session, redirect, jsonify
from .forms import *
from .models import *

"""

"""
class Payment:
    """

    """
    def __init__(self, request, settings, **kwargs):
        self.request = request
        self.form = request.form.to_dict()
        self.settings = settings
        self.extra = kwargs

    # Creates a signature by SHA256
    def __create_sign(self, required_keys, **request_obj):
        if len(request_obj.keys())!=0:
            sort_keys = sorted([key for key in required_keys])
            self.sign = sha256(bytes(':'.join([request_obj.get(elem) for elem in sort_keys])\
            +request_obj['STORE_SECRET'],encoding='utf-8')).hexdigest()
        else:
            print('Ooops')
    
    '''
    Делаем запросы на сервер методом post Content-Type=application/json
    и возвращаем json ответа
    '''
    def payload_data(self, from_data, req_keys, **kwargs):
        #req_keys = ('amount, currency, shop_id, shop_order_id, payway') -- for INVOICE
        payload = {}.fromkeys(req_keys)
        for key in req_keys:
            payload[key] = from_data[key]
        payload['sign']=self.sign

        r_obj = requests.post(from_data['link'], json=payload)
        return r_obj.json()

    # This method creates a dynamic form instance by data and fields (optional)
    # Use it for making requests: PAY or INVOICE
    def form_method(self, data, from_fields=None):
        flds = list(from_fields) if from_fields else data.keys()
        self.__create_sign(flds, **data)
        if 'sign' not in flds:
            data['sign']=self.sign
            flds.append('sign')
        if 'payway' in flds:
            d1 = {**self.payload_data(data, from_fields)['data']}
            d2 = {**d1['data']}
            form = create_form(d2.keys(), d2)
            return render_template('form_template.html', resform=form,
                context={'formmethod':d1['method'],'action':d1['url']})
        form = create_form(flds, data)
        return render_template('form_template.html', resform=form,
        context={'formmethod':data['meth'],'action':data['link']})

    '''
    Отдельный метод для USD
    '''
    def create_payload_usd_data(self, data, from_fields=None):
        req_keys = ('payer_currency','shop_currency','shop_id','shop_order_id','shop_amount')
        #looks like a crutch >:(
        payload = {
            'payer_currency':data.get('currency'),
            'shop_currency':data.get('STORE_CURRENCY'),
            'shop_id':data.get('shop_id'),
            'shop_order_id':data.get('shop_order_id'),
            'shop_amount':data.get('amount')
        }
        self.__create_sign(req_keys, **{**payload, 'STORE_SECRET':data['STORE_SECRET']})
        payload['sign']=self.sign
        r_obj = requests.post(data['link'], json=payload)
        return redirect(r_obj.json().get('data').get('url'))

    def make_result(self, modelParams, by_field, value):
        try:
            param = modelParams.get(modelParams.payCurrency==Currency.get(Currency.code==value))
        except Exception as e:
            print(e)
        else:
            dt = {
                **self.form,
                **self.settings,
                'link': param.action,
                'meth':param.method,
                }
            o_id = RegisteredOperation.create(
                currency=Currency.get(Currency.code==dt['currency']),
                amount=dt['amount'],
                description=dt['prod_descript'],
            )
            dt['shop_order_id']=str(o_id.id)

            return getattr(self, str(param.payMethod))(data=dt,
                           from_fields=str(param.requirementFields).split(', '))