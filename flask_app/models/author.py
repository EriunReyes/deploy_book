from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.book import Book
db = 'books'

class Author:
    def __init__(self, data):
        
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.books = []

    @classmethod
    def save(self, data):
        query = 'INSERT INTO authors(name, created_at, updated_at) VALUES (%(name)s, NOW(), NOW());'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM authors;'
        result = connectToMySQL(db).query_db(query)
        results = []
        for row in result:
            results.append(cls(row))
        return results

    @classmethod 
    def get_one(cls, data):
        query = 'SELECT * FROM authors LEFT JOIN favorites ON authors.id = favorites.author_id LEFT JOIN books ON books.id = favorites.book_id WHERE authors.id = %(id)s;'
        result = connectToMySQL(db).query_db(query, data)
        print(result)
        author = cls(result[0])
        for row_books in result:
            if row_books['book_id'] == None:
                break
            book_data = {
                'id': row_books['books.id'],
                'title': row_books['title'], 
                'num_of_pages': row_books['num_of_pages'], 
                'created_at': row_books['books.created_at'], 
                'updated_at': row_books['books.updated_at']
            }
            author.books.append(Book(book_data))
        return author

    @classmethod
    def update(cls, data):
        query = 'UPDATE authors SET title = %(title)s, num_of_pages = %(num_of_pages)s, updated_at = NOW() WHERE id = %(id)s; '
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroy(cls, data):
        query = 'DELETE FROM authors WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def favorite(cls, data):
        query ='INSERT INTO favorites (author_id, book_id)'\
        'VALUES (%(author_id)s, %(book_id)s)'
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def authors_not_in_book(cls, data):
        query = 'SELECT * FROM authors WHERE authors.id NOT IN (SELECT author_id FROM favorites WHERE book_id = %(id)s )'
        result = connectToMySQL(db).query_db(query, data)
        results = []
        for row in result:
            results.append(cls(row))
        return results
        