from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(),Length(min=4, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(),Length(min=4, max=128)])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')
