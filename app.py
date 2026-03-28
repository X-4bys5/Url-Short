import os
import random
import string
from flask import Flask, render_template, request, redirect, jsonify
from dotenv import load_dotenv
import sqlite3

load_dotenv()
app = Flask(__name__)
DB = "urls.db"

def init_db():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            short_code TEXT NOT NULL UNIQUE,
            long_url TEXT NOT NULL,
            clicks INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(length))
        conn = sqlite3.connect(DB)
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM urls WHERE short_code = ?", (code,))
        exists = cursor.fetchone()
        conn.close()
        if not exists:
            return code


@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT short_code, long_url, clicks FROM urls ORDER BY id DESC")
    urls = cursor.fetchall()
    conn.close()
    return render_template('index.html', urls=urls)


@app.route('/shorten', methods=['POST'])
def shorten():
    long_url = request.form.get('long_url', '').strip()

    if not long_url:
        return jsonify({'error': 'No long url provided.'}), 400

    if not long_url.startswith('http://') and not long_url.startswith('https://'):
        long_url = 'https://' + long_url

    short_code = generate_short_code()

    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO urls (short_code, long_url) VALUES (?, ?)",
                   (short_code, long_url))
    conn.commit()
    conn.close()
    return redirect('/')


@app.route('/<short_code>')
def redirect_url(short_code):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("SELECT long_url FROM urls WHERE short_code = ?", (short_code,))
    result = cursor.fetchone()

    if not result:
        conn.close()
        return render_template('index.html', error="Short link not found"), 404

    cursor.execute("UPDATE urls SET clicks = clicks + 1 WHERE short_code = ?",
                   (short_code,))
    conn.commit()
    conn.close()

    return redirect(result[0])


@app.route('/delete/<short_code>', methods=['POST'])
def delete_url(short_code):
    conn = sqlite3.connect(DB)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM urls WHERE short_code = ?", (short_code,))
    conn.commit()
    conn.close()
    return redirect('/')


init_db()

if __name__ == '__main__':
    app.run(debug=True)
