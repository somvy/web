from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length
 
class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired(),Length(min=4, max=100)])
    content = TextAreaField('Текст новости', validators=[DataRequired(),Length(min=4, max=1000)])
    submit = SubmitField('Добавить')