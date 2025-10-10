from flask_mongoengine import MongoEngine
from books import all_books  
from flask_login import UserMixin
import datetime
import random

db = MongoEngine()

class User(db.Document, UserMixin):
    meta = {'collection': 'users'}

    name = db.StringField(required=True)
    email = db.StringField(required=True, unique=True)
    password = db.StringField(required=True)


class Loan(db.Document):
    meta = {'collection': 'loans'}

    borrow_date = db.DateTimeField(required=True)
    return_date = db.DateTimeField()
    user_id = db.ReferenceField('User', required=True)
    book_id = db.ReferenceField('Book', required=True)
    renew_count = db.IntField(default=0)

    @staticmethod
    def create_loan(user, book, borrow_date):
        existing_loan = Loan.objects(user_id=user, book_id=book, return_date=None).first()
        if existing_loan:
            return None

        if book.borrow():
            loan = Loan(user_id=user, book_id=book, borrow_date=borrow_date)
            loan.save()
            return loan
        return None

    @staticmethod
    def get_user_loans(user):
        return Loan.objects(user_id=user).order_by('-borrow_date')

    @staticmethod
    def get_loan_by_id(loan_id):
        return Loan.objects(id=loan_id).first()

    def renew(self):
        """Renews a loan by updating the borrow date and incrementing the renew count."""
        if self.return_date is None and self.renew_count < 2:
            # Generate a new borrow date 10-20 days after the current one, not exceeding today
            today = datetime.datetime.utcnow()
            new_borrow_date = self.borrow_date + datetime.timedelta(days=random.randint(10, 20))
            if new_borrow_date > today:
                new_borrow_date = today
            
            self.borrow_date = new_borrow_date
            self.renew_count += 1
            self.save()
            return self
        return None

    def return_loan(self):
        """Marks a loan as returned and updates the book's availability."""
        if self.return_date is None:
            # Generate a return date 10-20 days after the borrow date, not exceeding today
            today = datetime.datetime.utcnow()
            return_date = self.borrow_date + datetime.timedelta(days=random.randint(10, 20))
            if return_date > today:
                return_date = today

            self.return_date = return_date
            self.book_id.return_copy()
            self.save()
            return True
        return False

    def delete_loan(self):
        """Deletes a loan document only if it has been returned."""
        if self.return_date:
            self.delete()
            return True
        return False


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

    def borrow(self):
        if self.available > 0:
            self.available -= 1
            self.save()
            return True
        return False

    def return_copy(self):
        if self.available < self.copies:
            self.available += 1
            self.save()
            return True
        return False

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