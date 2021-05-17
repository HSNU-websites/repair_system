from flask_wtf import FlaskForm
from flask_wtf.recaptcha import Recaptcha
from flask_wtf.recaptcha import RecaptchaField
from wtforms import PasswordField
from wtforms import SelectField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


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
        "大樓: ", validators=[DataRequired()]
    )  # choices will be added when rendered
    location = StringField("地點: ", validators=[DataRequired()])
    item = SelectField("損壞物件: ", validators=[DataRequired()])
    description = StringField("狀況描述: ", validators=[DataRequired()])
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Please click 'I am not a robot.'")]
    )
    submit = SubmitField("報修")


class ReportsFilterForm(FlaskForm):
    username = StringField("報修人學號: ")
    classnum = StringField("班級: ")
    submit = SubmitField("送出")
