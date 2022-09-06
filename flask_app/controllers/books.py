from flask_app import app
from flask_app.models.book import Book
from flask_app.models.author import Author
from flask import render_template, session, redirect, request

@app.route('/books') #This route render template the html page with the get all books from the database
def books():
    books = Book.get_all()
    return render_template('books.html', books = books)


@app.route('/add_book', methods=['POST']) # this method save our input information form into our database
def add_book():
    book = Book.save(request.form)
    return redirect('/books')


@app.route('/book_show/<int:id>', methods=['POST', 'GET']) # This method is calling the id on the route, requesting information from our foreign_keys,
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


@app.route('/deletes/<int:id>')
def destroy_book(id):
    data = {
        'id': id
    }
    books = Book.destroyBooks(data)
    return redirect('/books')



