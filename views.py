from models import *

"""
Создавать подпись будем этой ф-цией.
    -- required_keys -- требуемые ключи словаря для упорядочивания и формирования строки
    -- **request_obj -- словарь с данными запроса к сервису, на основе которого будет формироваться подпись,..
    .. из выбраных элементов
"""
def create_sign(required_keys, **request_obj):
    if len(request_obj.keys())!=0:
        sort_keys = sorted([key for key in required_keys])
        print(':'.join([request_obj.get(elem) for elem in sort_keys])+request_obj['secret_key'])
        return sha256(bytes(':'.join([request_obj.get(elem) for elem in sort_keys])\
        +request_obj['secret_key'],encoding='utf-8')).hexdigest()
    else:
        print('Ooops')

def record_to_db():
    
