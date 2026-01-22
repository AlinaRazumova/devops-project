from flask import Flask, jsonify
import psycopg2
import os
import time

app = Flask(__name__)

# Ждём базу данных
time.sleep(5)

def get_connection():
    return psycopg2.connect(os.environ['DATABASE_URL'])

@app.route("/movies")
def movies():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS movies (
            id SERIAL PRIMARY KEY,
            title TEXT,
            year INT
        );
    """)

    # Проверим, есть ли данные
    cur.execute("SELECT COUNT(*) FROM movies;")
    count = cur.fetchone()[0]
    if count == 0:
        cur.execute("""
            INSERT INTO movies (title, year) VALUES
            ('Inception', 2010),
            ('Interstellar', 2014);
        """)
        conn.commit()

    cur.execute("SELECT title, year FROM movies;")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    return jsonify([{"title": row[0], "year": row[1]} for row in rows])

@app.route("/")
def home():
    return "Привет! Перейди на /movies чтобы увидеть список фильмов."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
