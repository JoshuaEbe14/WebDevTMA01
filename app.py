from flask import Flask, render_template
from books import all_books # Correctly import the 'all_books' list

app = Flask(__name__)

@app.route('/')
def home():
    # Sort the list of book dictionaries directly by the 'title' key
    sorted_books = sorted(all_books, key=lambda book: book['title'])

    # Process the description for each book
    for book in sorted_books:
        # The 'description' is a list of strings (paragraphs)
        description_paragraphs = book['description']
        
        # Check if there is more than one paragraph
        if len(description_paragraphs) > 1:
            # Create a new key with the first and last paragraphs
            book['display_description'] = f"{description_paragraphs[0]} ... {description_paragraphs[-1]}"
        else:
            # If there's only one paragraph, just use that one
            book['display_description'] = description_paragraphs[0]

    # Pass the processed and sorted list to the template
    return render_template('home.html', books=sorted_books)