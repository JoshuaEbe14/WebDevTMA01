from flask import Flask, render_template, request
from books import all_books

app = Flask(__name__)

def first_last(paras):
    paras = [p.strip() for p in paras if p and p.strip()]
    if not paras:
        return "", ""
    return paras[0], (paras[-1] if len(paras) > 1 else "")

@app.route('/')
def home():
    # selected category (default: All)
    selected = (request.args.get('category') or 'All').title()

    # categories for dropdown
    categories = ['All'] + sorted({(b.get('category') or '').title() for b in all_books if b.get('category')})

    # filter by category
    if selected != 'All':
        data = [b for b in all_books if (b.get('category') or '').title() == selected]
    else:
        data = list(all_books)

    # sort by title
    data.sort(key=lambda book: book['title'])

    # split description into first/last
    books = []
    for b in data:
        first, last = first_last(b.get('description', []))
        # display categories: category first, then genres
        cat = (b.get('category') or '').title()
        genres = [g.title() for g in b.get('genres', [])]
        display_categories = ([cat] if cat else []) + [g for g in genres if g != cat]
        books.append({**b, 'first_paragraph': first, 'last_paragraph': last, 'display_categories': display_categories})

    return render_template(
        'home.html',
        books=books,
        count=len(books),
        categories=categories,
        selected_category=selected
    )

@app.route('/book/<string:title>')
def book_details(title):
    # Find the book from the 'all_books' list that matches the title
    book = next((b for b in all_books if b['title'] == title), None)
    
    if book:
        # Renders the book_details.html template
        return render_template('book_details.html', book=book)
    
    # If no book with that title exists, return a 404 error
    return "Book not found", 404