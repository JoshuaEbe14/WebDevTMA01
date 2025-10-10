from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectMultipleField, SelectField, TextAreaField, IntegerField, FieldList, FormField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, URL

class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5)])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

class AuthorForm(FlaskForm):
    name = StringField('Author Name')
    is_illustrator = BooleanField('Illustrator')

class AddBookForm(FlaskForm):
    genres = SelectMultipleField('Choose multiple Genres', coerce=str, validators=[DataRequired()])
    title = StringField('Title', validators=[DataRequired()])
    category = SelectField('Choose a category', choices=[('Children', 'Children'), ('Teens', 'Teens'), ('Adult', 'Adult')], validators=[DataRequired()])
    url = StringField('URL for Cover', validators=[DataRequired(), URL()])
    description = TextAreaField('Description', validators=[DataRequired()])

    authors = FieldList(FormField(AuthorForm), min_entries=5, max_entries=5)
    
    pages = IntegerField('Number of pages', validators=[DataRequired()])
    copies = IntegerField('Number of copies', validators=[DataRequired()])
    submit = SubmitField('Submit')