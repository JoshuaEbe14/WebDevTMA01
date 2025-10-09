from flask_mongoengine import MongoEngine
from books import all_books  
from flask_login import UserMixin

db = MongoEngine()

class User(db.Document, UserMixin):
    meta = {'collection': 'users'}

    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)


class Book(db.Document):

    meta = {'collection': 'books'}  # Explicitly name the collection in the database

    # Map attributes from the class diagram to MongoEngine field types
    genres = db.ListField(db.StringField())
    title = db.StringField(required=True)
    category = db.StringField()
    url = db.StringField()
    description = db.ListField(db.StringField())
    authors = db.ListField(db.StringField())
    pages = db.IntField()
    available = db.IntField()
    copies = db.IntField()

    @staticmethod
    def init_db():
        # Checks if the collection is empty
        if Book.objects.count() == 0:
            print("Database is empty. Populating with initial book data...")
            # If it is, read data from the global 'all_books' variable
            for book_data in all_books:
                # Create a Book document and save it to MongoDB
                book = Book(**book_data)  
                book.save()
            print("Database populated successfully.")