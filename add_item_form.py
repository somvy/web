from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length


class AddItemForm(FlaskForm):
    name = StringField('Название товара', validators=[DataRequired(), Length(min=4, max=50)])
    image = TextAreaField('Ссылка на изображение', validators=[DataRequired(), Length(min=4, max=400)])
    price = StringField('Цена', validators=[DataRequired(), Length(min=1, max=10)])
    info = TextAreaField('Описание ', validators=[DataRequired(), Length(min=1, max=500)])
    count = StringField('Количество ', validators=[DataRequired(), Length(min=1, max=9)])
    submit = SubmitField('Добавить товар')
