from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import Email, DataRequired, Length


class RegistrationForm(FlaskForm):
    username = StringField(validators=[DataRequired()])
    password = PasswordField(validators=[DataRequired(), Length(min=8)])
    password_again = PasswordField(validators=[DataRequired(), Length(min=8)])
    email = EmailField(validators=[DataRequired(), Email()])
    submit = SubmitField("Регистрация")


class LoginForm(FlaskForm):
    email = EmailField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField("Войти")
