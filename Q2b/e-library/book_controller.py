from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import Book
from forms import AddBookForm

book_bp = Blueprint('book', __name__)

GENRE_CHOICES = [
    "Animals", "Business", "Comics", "Communication", "Dark Academia",
    "Emotion", "Fantasy", "Fiction", "Friendship", "Graphic Novels", "Grief",
    "Historical Fiction", "Indigenous", "Inspirational", "Magic", "Mental Health",
    "Nonfiction", "Personal Development", "Philosophy", "Picture Books", "Poetry",
    "Productivity", "Psychology", "Romance", "School", "Self Help"
]

@book_bp.route('/add_book', methods=['GET', 'POST'])
@login_required
def add_book():
    if current_user.email != 'admin@lib.sg':
        flash('You do not have permission to access this page.', 'danger')
        return redirect(url_for('home'))

    form = AddBookForm()
    form.genres.choices = [(genre, genre) for genre in GENRE_CHOICES]

    if request.method == 'POST':
        # Always bind incoming data to the form on POST
        form.process(request.form)

        # 1) Add author row
        if 'add_author' in request.form:
            form.authors.append_entry()
            return render_template('add_book.html', form=form)

        # 2) Remove specific author row
        if 'remove_author' in request.form:
            idx = int(request.form['remove_author'])
            if len(form.authors.entries) > 1 and 0 <= idx < len(form.authors.entries):
                # rebuild list without the removed index
                data = form.authors.data
                data.pop(idx)
                while form.authors.entries:
                    form.authors.pop_entry()
                for row in data:
                    form.authors.append_entry(row)
            return render_template('add_book.html', form=form)

        # 3) Otherwise it's a real submit
        if form.validate():
            authors_list = []
            has_author = False
            for author_entry in form.authors.data:
                name = (author_entry.get('author_name') or '').strip()
                if name:
                    has_author = True
                    authors_list.append(
                        f"{name} (Illustrator)" if author_entry.get('is_illustrator') else name
                    )
            if not has_author:
                flash('At least one author is required.', 'danger')
                return render_template('add_book.html', form=form)

            description_list = [p.strip() for p in form.description.data.split('\n') if p.strip()]

            Book(
                title=form.title.data,
                genres=form.genres.data,
                category=form.category.data,
                url=form.url.data,
                description=description_list,
                authors=authors_list,
                pages=form.pages.data,
                copies=form.copies.data,
                available=form.copies.data,
            ).save()

            flash(f'Book "{form.title.data}" has been successfully added!', 'success')
            return redirect(url_for('book.add_book'))
        else:
            # Show validation errors
            for field, errors in form.errors.items():
                for err in errors:
                    flash(f"{field}: {err}", 'danger')
            return render_template('add_book.html', form=form)

    # GET request: ensure at least one author row
    if not form.authors.entries:
        form.authors.append_entry()

    return render_template('add_book.html', form=form)