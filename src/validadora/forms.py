from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class ValidateForm(Form):
    dcat_url = StringField('dcat_url', validators=[DataRequired()])