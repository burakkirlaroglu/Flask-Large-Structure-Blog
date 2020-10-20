from flask_wtf import FlaskForm
from blog.user.models import User
from wtforms import TextField, PasswordField, BooleanField, TextAreaField, SubmitField
from wtforms.validators import Required, EqualTo, Email


class LoginForm(FlaskForm):
    email = TextField('Email Address', [Required(), Email()])
    password = PasswordField("Password", [Required()])


class RegisterForm(FlaskForm):
    name = TextField("Name", [Required()])
    email = TextField("Email Address", [Required(), Email()])
    password = PasswordField('Password', [Required()])

    confirm = PasswordField("Repeat Password", [
        Required(),
        EqualTo('password', message="Password must match!!")
    ])

    acceept_policy = BooleanField('I accept Policy', [Required()])

class ArticleForm(FlaskForm):
    title = TextField("Title", [Required()])
    content = TextAreaField("Content", [Required()])



class RequestResetForm(FlaskForm):
    email = TextField("Email Address", [Required(), Email()])
    submit = SubmitField("Request Password Reset" )

    def validate_email(self, email):
        user = User.query.filter_by(email = email.data).first()
        if user is None:
            raise ValidationError("There is no account.")

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', [Required()])

    confirm_password = PasswordField("Repeat Password", [
        Required(),
        EqualTo('password', message="Password must match")
    ])

    submit = SubmitField("Reset Password")