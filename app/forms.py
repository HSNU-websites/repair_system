from flask_wtf import FlaskForm
from flask_wtf.recaptcha import Recaptcha, RecaptchaField
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.validators import DataRequired

from .db_helper import render_buildings, render_items


class LoginForm(FlaskForm):
    username = StringField(
        "帳號(學號): ", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "密碼: ", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    submit = SubmitField("登入")


class ReportForm(FlaskForm):
    building = SelectField(
        "大樓: ", choices=render_buildings(), validators=[DataRequired()]
    )
    place = StringField("地點: ", validators=[DataRequired()])
    item = SelectField("損壞物件: ", choices=render_items(), validators=[DataRequired()])
    description = StringField("狀況描述: ", validators=[DataRequired()])
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Please click 'I am not a robot.'")]
    )
    submit = SubmitField("報修")
