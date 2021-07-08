from flask_wtf import FlaskForm
from wtforms import PasswordField, SelectField, StringField, SubmitField, HiddenField
from wtforms.fields.html5 import EmailField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from flask_wtf.recaptcha import RecaptchaField
from wtforms.validators import DataRequired, ValidationError, Length


class LoginForm(FlaskForm):
    username = StringField(
        "帳號(學號): ", validators=[DataRequired()], render_kw={"placeholder": "Username"}
    )
    password = PasswordField(
        "密碼: ", validators=[DataRequired()], render_kw={"placeholder": "Password"}
    )
    recaptcha = RecaptchaField()
    submit = SubmitField("登入")


class ReportForm(FlaskForm):
    building = SelectField(
        "大樓: ", validators=[DataRequired()]
    )  # choices will be added when rendered
    location = StringField(
        "地點 (限 200 字內): ", validators=[DataRequired(), Length(max=200)]
    )
    item = SelectField("損壞物件: ", validators=[DataRequired()])
    description = StringField(
        "狀況描述 (限 200 字內): ", validators=[DataRequired(), Length(max=200)]
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


class UserFilterForm(FlaskForm):
    form_name = HiddenField(render_kw={"value": "filter"})
    upper = IntegerField(
        "", render_kw={"placeholder": "Student ID"}
    )
    lower = IntegerField(
        "", render_kw={"placeholder": "Student ID"}
    )
    submit = SubmitField("送出")


class AddOneUserForm(FlaskForm):
    username = StringField(
        "學號 (登入帳號): ",
        validators=[DataRequired(), Length(max=16)],
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
        "密碼: ",
        validators=[
            DataRequired(),
            Length(min=6, message="Password is too short (at least 6 characters)."),
        ],
        render_kw={"placeholder": "Password"},
    )
    email = EmailField("電子郵件 (僅管理員需要): ", render_kw={"placeholder": "Email"})
    submit = SubmitField("新增")

    def validate_email(self, field):
        if self.classnum.data == "0" and self.email.data == "":
            raise ValidationError("Email is required for admin.")


class AddUsersByFileForm(FlaskForm):
    csv_file = FileField(
        "CSV file",
        validators=[FileRequired(), FileAllowed(["csv"], "Only csv is allowed.")],
    )
    submit = SubmitField("新增")


class UserSettingForm(FlaskForm):
    email = EmailField("Email: ", render_kw={"placeholder": "Email"})
    password = PasswordField("密碼: ", render_kw={"placeholder": "未更改"})
    submit = SubmitField("更改")

    def validate_password(self, field):
        if type(field.data) is str:
            if field.data != "" and len(field.data) < 6:
                raise ValidationError("Password is too short (at least 6 characters).")
        else:
            raise ValidationError("Invalid.")


class RestoreForm(FlaskForm):
    file = FileField("", validators=[FileRequired(), FileAllowed(["xz"])])
    submit = SubmitField("上傳")
