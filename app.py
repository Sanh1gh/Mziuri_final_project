from flask import Flask, render_template, redirect, request, session, url_for, flash
from datetime import timedelta
import sqlite3

app = Flask(__name__)

app.secret_key = 'mziuri'

app.permanent_session_lifetime = timedelta(minutes=1)

DATABASE = 'database.db'

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def register(self):
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (self.username, self.password))
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False

    def login(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('SELECT password FROM users WHERE username = ?', (self.username,))
        record = cursor.fetchone()
        conn.close()
        if record and record[0] == self.password:
            return True
        return False

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html', username=session['username'])
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.login():
            session['username'] = username
            return redirect(url_for('home'))
        else:
            flash('womp womp womp')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username, password)
        if user.register():
            flash('now u are registred')
            return redirect(url_for('login'))
        else:
            flash('es useri arsebobs')
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/add_song', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        genre = request.form['genre']
        release_year = request.form['release_year']

        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO songs (title, genre, date) VALUES (?, ?, ?)', (title, genre, release_year))
        conn.commit()
        conn.close()

        flash(' yochag ')
        return redirect(url_for('song_list'))

    return render_template('add_song.html')



@app.route('/song_list')
def song_list():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, title FROM songs')
    songs = cursor.fetchall()
    conn.close()
    return render_template('song_list.html', songs=songs)



if __name__ == '__main__':
    app.run(debug=True)

