from flask.ext.wtf import Form
from flask.ext.wtf.html5 import URLField
from wtforms.widgets import TextInput
from wtforms.validators import DataRequired
from wtforms import StringField

class VueTextInput(TextInput):
  def __call__(self, field, **kwargs):
    for key in list(kwargs):
        if key.startswith('v_'):
            elements = key.split('_')
            element = 'v-' + elements[1]
            if  len(elements) >= 3:
                element += ":" + elements[2]
            if len(elements) > 3:
                element += '.' + '.'.join(elements[3:])

            kwargs[element] = kwargs.pop(key)
    return super(VueTextInput, self).__call__(field, **kwargs)

class ValidateForm(Form):
  dcat_url = StringField('dcat_url', validators=[DataRequired()], widget=VueTextInput())
