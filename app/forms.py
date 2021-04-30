from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField, Recaptcha
from wtforms import StringField, PasswordField, SubmitField, SelectField
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
        "大樓: ", choices=[], validators=[DataRequired()]
    )  # TODO choices
    place = StringField("地點: ", validators=[DataRequired()])
    item = SelectField(
        "損壞物件: ", choices=[], validators=[DataRequired()]
    )  # TODO choices
    description = StringField("狀況描述: ", validators=[DataRequired()])
    recaptcha = RecaptchaField(
        validators=[Recaptcha(message="Please click 'I am not a robot.'")]
    )
    submit = SubmitField("報修")
