from flask import make_response, render_template
from wtforms.form import Form
from wtforms import SelectField, TextAreaField, HiddenField, DecimalField, SubmitField, StringField
from wtforms.validators import Required

class MainForm(Form):
    amount = DecimalField(places=2, validators=[Required()])
    currency = SelectField(choices=[('840','USD'),('643','RUB'),('978','EUR'),('980','UAH')])
    prod_descript = TextAreaField(u'Описание продукта')
    submit = SubmitField()

def create_form(fields, from_data):
    class DynamicForm(Form): pass

    for field in fields:
        fvalue = from_data.get(field)
        setattr(DynamicForm, field, setField(fvalue))

    return DynamicForm()

def setField(val=None):
    return StringField(default='' if val is None else val)