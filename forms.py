import flask_wtf
import wtforms
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired


class LoginForm(flask_wtf.FlaskForm):
    password = wtforms.PasswordField('Код доступа (можно получить у бота по /get_code)', validators=[DataRequired()])
    remember_me = wtforms.BooleanField('Запомнить меня', default=True)
    submit = wtforms.SubmitField('Войти')
