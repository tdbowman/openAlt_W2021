from flask_wtf import Form, RecaptchaField
from wtforms import TextField, SubmitField, TextAreaField
from wtforms.validators import Length, Email, Required

class ResultForm(Form):
    email = TextField('Email Address:', validators=[Required(), Email()])
    recaptcha = RecaptchaField()
    submit = SubmitField('Get Results!')

