from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,TextAreaField,SelectField
from wtforms.validators import DataRequired

class BlogPostForm(FlaskForm):

    title = StringField('Title', validators=[DataRequired()])
    tip = SelectField('Select Prediction', choices=[('cpp', 'C++')])
    text = TextAreaField('Text', validators=[DataRequired()])
    submit = SubmitField("Post !")
