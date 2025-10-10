from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Book, Loan, User
import datetime
import random

loan_bp = Blueprint('loan_bp', __name__)

@loan_bp.route("/loan/<book_id>", methods=['POST'])
@login_required
def loan_book(book_id):
    if not isinstance(current_user._get_current_object(), User):
        flash("Please login or register first to get an account", "warning")
        return redirect(url_for('auth_bp.login'))

    book = Book.objects(id=book_id).first()
    if not book:
        flash("Book not found.", "danger")
        return redirect(url_for('book_bp.home'))

    # The application randomly generates a borrow date 10 to 20 days before today’s date
    borrow_date = datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(10, 20))

    loan = Loan.create_loan(user=current_user._get_current_object(), book=book, borrow_date=borrow_date)

    if loan:
        flash(f"You have successfully borrowed '{book.title}'.", "success")
    else:
        if book.available == 0:
            flash(f"Sorry, '{book.title}' is currently unavailable.", "danger")
        else:
            flash(f"You already have an unreturned loan for '{book.title}'.", "warning")

    # Redirect back to the page the user was on
    return redirect(request.referrer or url_for('book_bp.home'))

@loan_bp.route('/loans')
@login_required
def view_loans():
    user_loans = Loan.get_user_loans(current_user._get_current_object())
    today = datetime.datetime.utcnow()
    return render_template('loans.html', loans=user_loans, today=today, timedelta=datetime.timedelta)

@loan_bp.route('/loan/renew/<loan_id>', methods=['POST'])
@login_required
def renew_loan(loan_id):
    loan = Loan.get_loan_by_id(loan_id)
    if loan and loan.user_id.id == current_user.id:
        if loan.renew():
            flash(f"Successfully renewed '{loan.book_id.title}'.", "success")
        else:
            flash("This loan cannot be renewed.", "danger")
    else:
        flash("Loan not found or you do not have permission to renew it.", "danger")
    return redirect(url_for('loan_bp.view_loans'))

@loan_bp.route('/loan/return/<loan_id>', methods=['POST'])
@login_required
def return_loan(loan_id):
    loan = Loan.get_loan_by_id(loan_id)
    if loan and loan.user_id.id == current_user.id:
        if loan.return_loan():
            flash(f"Successfully returned '{loan.book_id.title}'.", "success")
        else:
            flash("This loan could not be returned.", "danger")
    else:
        flash("Loan not found or you do not have permission to return it.", "danger")
    return redirect(url_for('loan_bp.view_loans'))

@loan_bp.route('/loan/delete/<loan_id>', methods=['POST'])
@login_required
def delete_loan(loan_id):
    loan = Loan.get_loan_by_id(loan_id)
    if loan and loan.user_id.id == current_user.id:
        if loan.delete_loan():
            flash("Loan record successfully deleted.", "success")
        else:
            flash("This loan cannot be deleted as it has not been returned yet.", "danger")
    else:
        flash("Loan not found or you do not have permission to delete it.", "danger")
    return redirect(url_for('loan_bp.view_loans'))
