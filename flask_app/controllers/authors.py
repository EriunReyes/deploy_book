from flask_app import app
from flask_app.models.author import Author
from flask_app.models.book import Book
from flask import render_template, redirect, request, session 




@app.route('/')
def create_author():
    author = Author.get_all()
    return render_template('authors.html', author = author)


@app.route('/add_author', methods=['POST']) #form to add information in our columns from the author table.
def add_author():
    author = Author.save(request.form)
    return redirect('/')


@app.route('/show_author/<int:id>', methods=['GET', 'POST']) #This route should show one author
def show_author(id):
    data = {
        'id': id
    }
    if request.method == 'POST':
        favorite_data = {
            'book_id': request.form['book_id'],
            'author_id': id
        }
        Author.favorite(favorite_data)
    author = Author.get_one(data)
    books = Book.books_not_in_author(data)
    return render_template('author_show.html', author = author, books=books)

@app.route('/show_form', methods=['POST'])
def show_form():
    return redirect('/show_author/<int:id>')


# @app.route('/redirect')
# def redirect():
#     return render_template('author_show.html') 


@app.route('/delete/<int:id>')
def destroy(id):
    data = {
        'id': id
    }
    author = Author.destroy(data)
    return redirect('/')

