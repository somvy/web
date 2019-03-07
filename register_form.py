from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Length


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired(), Length(min=4, max=50)])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, max=128)])
    password_again = PasswordField('Повторите пароль', validators=[DataRequired(), Length(min=8, max=128)])
    email = StringField('E-mail', validators=[Email()])
    mode = SelectField('Режим пользователя', choices=['User', 'Moder', 'Admin'])
    submit = SubmitField('Зарегистрироваться')
