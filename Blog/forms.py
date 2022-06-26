from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from Blog.models import User

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[DataRequired(), Length(min=4, max=32)],
        render_kw={"placeholder": "Username"}

    )

    email = StringField(
        "Email",
        validators=[DataRequired(), Email(),],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4, max=16)],
        render_kw={"placeholder": "Password"}
    )

    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"placeholder": "Conifrm Password"}
    )

    submit = SubmitField("Continue")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user :
            raise ValidationError('Username is taken. Please choose another one.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user :
            raise ValidationError('Email is taken. Please choose another one.')


class LoginForm(FlaskForm):
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        'Password',
        validators=[DataRequired(), Length(min=4, max=16)],
        render_kw={"placeholder": "Password"}
    )

    remember = BooleanField("Remember Me")

    submit = SubmitField("Continue")

