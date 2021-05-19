from flask_wtf import FlaskForm
from flask_wtf.recaptcha import Recaptcha
from flask_wtf.recaptcha import RecaptchaField
from wtforms import PasswordField, SelectField, StringField, SubmitField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, ValidationError


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
    username = StringField(
        "報修人學號: ",
        render_kw={"placeholder": "Username"},
    )
    classnum = StringField(
        "班級: ",
        render_kw={"placeholder": "Class Number"},
    )
    submit = SubmitField("送出")


class AddOneUserForm(FlaskForm):
    username = StringField(
        "學號 (登入帳號): ",
        validators=[DataRequired()],
        render_kw={"placeholder": "Username"},
    )
    name = StringField(
        "姓名: ",
        validators=[DataRequired()],
        render_kw={"placeholder": "Name"},
    )
    classnum = StringField(
        "班號 (管理員請填 0): ",
        validators=[DataRequired()],
        render_kw={"placeholder": "Class Number"},
    )
    password = PasswordField(
        "密碼: ", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    email = EmailField("電子郵件 (僅管理員需要)", render_kw={"placeholder": "Email"})
    submit = SubmitField("新增")

    def validate_email(self, field):
        if self.classnum.data == "0" and self.email.data == "":
            raise ValidationError("Email is required for admin.")


class AddUsersByFileForm(FlaskForm):
    pass
