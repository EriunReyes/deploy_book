from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author
from flask import render_template, session, redirect, request



@app.route('/books')
def books():

    books = Book.get_all()
    return render_template('books.html', books = books)


@app.route('/add_book', methods=['POST'])
def add_book():

    book = Book.save(request.form)
    return redirect('/books')


@app.route('/book_show/<int:id>', methods=['POST', 'GET'])
def book_show(id):

    data = {
        'id': id
    }
    if request.method == 'POST':
        favorite_data = {
            'author_id': request.form['author_id'],
            'book_id': id
        }
        Author.favorite(favorite_data)
    authors = Author.authors_not_in_book(data)
    book = Book.get_one(data)
    return render_template('/book_show.html', authors = authors, book = book)



