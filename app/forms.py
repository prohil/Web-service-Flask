from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, HiddenField,IntegerField
from wtforms import validators


class RecognizeForm(FlaskForm):
    btn_recognize = SubmitField('Распознать')
    address_field = StringField('', validators=[validators.DataRequired()])
    #address_field = StringField('', validators=[validators.DataRequired(), validators.URL(1, "Введите адрес!")])


class SearchDbForm(FlaskForm):
    btn_search = SubmitField('Поиск')
    #site_search_field = StringField('', validators=[validators.DataRequired(), validators.URL(1, "Введите адрес!")])
    site_search_field = StringField('', validators=[validators.DataRequired()])



#extra validator try to load the site (can be write with a mistake: https://goole.com)



