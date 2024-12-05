from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from .models import User

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
    render_kw={"placeholder": "username"})
    
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)],
    render_kw={"placeholder": "password"})

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("Username already exists")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
    render_kw={"placeholder": "username"})
    
    password = StringField(validators=[InputRequired(), Length(min=4, max=20)],
    render_kw={"placeholder": "password"})

    submit = SubmitField("Login")