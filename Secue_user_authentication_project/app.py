from flask import Flask, render_template_string, redirect, request, session, send_from_directory
import sqlite3
import bcrypt
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            role TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# Load HTML content from files manually (same folder)
def load_template(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read()

# Serve CSS from the same folder
@app.route('/styles.css')
def serve_css():
    return send_from_directory(os.getcwd(), 'styles.css')

# Serve image from the same folder
@app.route('/security_image.webp')
def serve_image():
    return send_from_directory(os.getcwd(), 'security_image.webp')

@app.route('/')
def home():
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, hashed, 'user'))
            conn.commit()
            return redirect('/login')
        except sqlite3.IntegrityError:
            return "Username already exists!"
        finally:
            conn.close()
    return render_template_string(load_template('register.html'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute("SELECT password, role FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()

        if result and bcrypt.checkpw(password.encode('utf-8'), result[0]):
            session['username'] = username
            session['role'] = result[1]
            return redirect('/dashboard')
        return "Invalid credentials!"
    return render_template_string(load_template('login.html'))

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect('/login')
    html = load_template('dashboard.html')
    return render_template_string(html.replace("{{ username }}", session['username']).replace("{{ role }}", session['role']))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)

