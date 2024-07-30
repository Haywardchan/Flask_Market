from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, IntegerField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from home.models import User, Item

class RegisterForm(FlaskForm):
    
    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists!')
    def validate_email_addr(self, email_address_to_check):
        email_address = User.query.filter_by(email_addr=email_address_to_check.data).first()
        if email_address:
            raise ValidationError('Email address already exists!')
        
    username = StringField(label='username:', validators=[Length(min=2, max=30), DataRequired()])
    email_addr = StringField(label='email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='comfirm password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')
 
class LoginForm(FlaskForm):
    username=StringField(label='Username:', validators=[DataRequired()])
    password=PasswordField(label='Password:', validators=[DataRequired()])
    submit=SubmitField(label='Sign in')

class AddItemForm(FlaskForm):

    def validate_name(self, name_to_check):
        item = Item.query.filter_by(name=name_to_check.data).first()
        if item:
            raise ValidationError('Item already exists!')
        
    item_name=StringField(label='Item:', validators=[DataRequired()])
    count=IntegerField(label='Count:', validators=[DataRequired()])
    consumption=IntegerField(label='Consumption rate (How many are used per day):', validators=[DataRequired()])
    description=TextAreaField(label='Description (if any):')
    submit=SubmitField(label='Add item')