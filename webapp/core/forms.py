from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo
from wtforms import ValidationError

class SelectForm(FlaskForm):

    select1 = IntegerField('Number')
    submit = SubmitField('Submit')
