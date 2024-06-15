import sqlite3

DATABASE = 'database.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL 
        )
    ''')


    cursor.execute('''
        CREATE TABLE IF NOT EXISTS songs ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            genre TEXT NOT NULL,
            date INTEGER NOT NULL 
        )
    ''')





    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()