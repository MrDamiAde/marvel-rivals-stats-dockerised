from flask import Flask, render_template, abort
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    return psycopg2.connect(
        host=os.environ['POSTGRES_HOST'],
        database=os.environ['POSTGRES_DB'],
        user=os.environ['POSTGRES_USER'],
        password=os.environ['POSTGRES_PASSWORD']
    )

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, health, speed, ability FROM characters;')
    characters = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', characters=characters)

@app.route('/character/<name>')
def character_detail(name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT name, health, speed, ability FROM characters WHERE name = %s;', (name,))
    character = cur.fetchone()
    cur.close()
    conn.close()
    if character:
        return render_template('character.html', character=character)
    else:
        abort(404)

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

