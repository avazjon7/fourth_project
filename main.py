import psycopg2

db_params = {
    'host': 'localhost',
    'port': 5432,
    'database': 'lesson_1',
    'user': 'postgres',
    'password': '1234',
}

class BookManager:
    def __init__(self, db_params):
        self.db_params = db_params

    def __enter__(self):
        self.conn = psycopg2.connect(**self.db_params)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id SERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                author VARCHAR(300) NOT NULL
            )
        ''')
        self.conn.commit()
        print(f"Connected'{self.db_params['database']}'")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()
        print(f"Disconnected'{self.db_params['database']}'")

    def create_book(self, book):
        self.cursor.execute(
            'INSERT INTO books (name, author) VALUES (%s, %s) RETURNING id',
            (book['name'], book['author'])
        )
        book_id = self.cursor.fetchone()[0]
        self.conn.commit()
        print(f"Added book: {book} with id {book_id}")

    def read_books(self):
        self.cursor.execute('SELECT * FROM books')
        books = self.cursor.fetchall()
        return books

    def update_book(self, book_id, updated_book):
        self.cursor.execute(
            'UPDATE books '
            '      SET name = %s, '
            '      author = %s '
            '      WHERE id = %s',
            (updated_book['name'], updated_book['author'], book_id)
        )
        self.conn.commit()
        print(f"Updated book with id {book_id}: {updated_book}")

    def delete_book(self, book_id):
        self.cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
        self.conn.commit()
        print(f"Deleted book with id {book_id}")


with BookManager(db_params) as manager:

    manager.create_book({'name': '1984', 'author': 'Lev Tolstoy'})
    manager.create_book({'name': 'Inferno', 'author': 'Victor Soy'})


    books = manager.read_books()
    print("Current books:", books)


    manager.update_book(1, {'name': 'Nineteen Eighty-Four', 'author': 'George Orwell'})
    manager.delete_book(2)

    books = manager.read_books()
    print("Remaked version:", books)
