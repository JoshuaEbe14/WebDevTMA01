from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField, TextAreaField, IntegerField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL, InputRequired, NumberRange
from wtforms import Form

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AuthorForm(Form):
    class Meta:
        csrf = False

    author_name = StringField('Author Name')
    is_illustrator = BooleanField('Illustrator')

class AddBookForm(FlaskForm):
    genres = SelectMultipleField('Choose multiple Genres', coerce=str, validators=[DataRequired(message='Select at least one genre')])
    title = StringField('Title', validators=[DataRequired(message='Title is required')])
    category = SelectField('Choose a category', choices=[('Children', 'Children'), ('Teens', 'Teens'), ('Adult', 'Adult')], validators=[DataRequired(message='Category is required')])
    url = StringField('URL for Cover', validators=[DataRequired(message='Cover URL is required'), URL(message='Enter a valid URL')])
    description = TextAreaField('Description', validators=[DataRequired(message='Description is required')])
    authors = FieldList(FormField(AuthorForm), min_entries=1, label='Authors')
    
    pages = IntegerField('Number of pages', validators=[InputRequired(message='Pages is required'), NumberRange(min=1, message='Pages must be at least 1')])
    copies = IntegerField('Number of copies', validators=[InputRequired(message='Copies is required'), NumberRange(min=1, message='Copies must be at least 1')])
    submit = SubmitField('Submit')