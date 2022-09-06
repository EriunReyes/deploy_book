from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import author

db = 'books'
class Book:   
    def __init__(self, data): #Class that helps to bring the attributes from our table Book
        self.id = data['id']
        self.title = data['title']
        self.num_of_pages = data['num_of_pages']
        self.price = data['price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.authors = []

    @classmethod
    def save(self, data): # method that helps to insert our information tables and save it in our database
        query = 'INSERT INTO books(title, num_of_pages,price, created_at, updated_at) VALUES (%(title)s, %(num_of_pages)s, %(price)s, NOW(), NOW())'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = 'SELECT * FROM books;'
        result = connectToMySQL(db).query_db(query)
        results = []
        for row in result:
            results.append(cls(row))
        return results

    @classmethod 
    def get_one(cls, data):
        query ='SELECT * FROM books LEFT JOIN '\
        'favorites ON books.id = favorites.book_id LEFT JOIN '\
        'authors ON authors.id = favorites.author_id WHERE books.id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        book = cls(results[0])
        for row_author in results:
            if row_author['author_id'] == None:
                break
            author_data = {
                'id': row_author['authors.id'],
                'name': row_author['name'], 
                'created_at': row_author['authors.created_at'], 
                'updated_at': row_author['authors.updated_at']
            }
            book.authors.append(author.Author(author_data))
        return book

    @classmethod
    def update(cls, data):
        query = 'UPDATE books SET title = %(title)s, num_of_pages = %(num_of_pages)s, updated_at = NOW() WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def destroyBooks(cls, data):
        query = 'DELETE FROM books WHERE id = %(id)s;' #this method delete the specific id
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def books_not_in_author(cls, data): # this method allows to only add one book one time
        query = 'SELECT * FROM books WHERE books.id NOT IN (SELECT book_id FROM favorites WHERE author_id = %(id)s )' 
        result = connectToMySQL(db).query_db(query, data)
        results = []
        for row in result:
            results.append(cls(row))
        return results
        