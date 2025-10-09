from flask import Flask, render_template, request
from models import db, Book  
from flask_login import LoginManager
from models import User
from auth_controller import auth

app = Flask(__name__)

app.config['SECRET_KEY'] = 'a-very-secret-and-secure-key'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login' 
login_manager.login_message = "Please login or register first to get an account"

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

app.register_blueprint(auth)

app.config['MONGODB_SETTINGS'] = {
    'db': 'elibrary',       
    'host': 'localhost',    
    'port': 27017           
}

db.init_app(app)

Book.init_db()

@app.route('/')
def home():
    # selected category (default: All)
    selected = (request.args.get('category') or 'All').title()

    # categories for dropdown
    categories = ['All'] + sorted(Book.objects.distinct('category'))

    # filter by category
    if selected != 'All':
        books = Book.objects(category=selected).order_by('title')
    else:
        books = Book.objects().order_by('title')

    return render_template(
        'home.html',
        books=books,
        count=len(books),
        categories=categories,
        selected_category=selected
    )

@app.route('/book/<string:book_id>')
def book_details(book_id):
    # Find the single book document that matches the ID
    book = Book.objects(id=book_id).first()

    if book:
        # Renders the book_details.html template
        return render_template('book_details.html', book=book)
    
    # If no book with that title exists, return a 404 error
    return "Book not found", 404