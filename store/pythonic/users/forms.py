from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from custom.custom_fields import EgyptPhoneField, EgyptPhone


class RegistrationForm(FlaskForm):
    username = StringField('Usernaem', validators=[DataRequired(), Length(min=2, max=25)])
    phone = EgyptPhoneField('Phone Number', validators=[DataRequired(), EgyptPhone()])
    password = PasswordField('Password', validators=[DataRequired(), 
        Regexp(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&_])[A-Za-z\d@$!%*?&_]{8,32}$")])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign in')




class VerifyForm(FlaskForm):
    code = StringField('Verification Code', validators=[
        DataRequired(),
        Length(min=6, max=6, message="Code must be 6 digits")
    ])
    submit = SubmitField('Verify')



class LoginForm(FlaskForm):
    phone = EgyptPhoneField('Phone Number', validators=[DataRequired(), EgyptPhone()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
