from flask import Flask, request, redirect
import psycopg2
import os
import string
import random
from dotenv import load_dotenv
import werkzeug

load_dotenv()
app = Flask(__name__)

"""
DB connection
"""
def connect_to_db():
    print("starting connection to DB")
    try:
        DB_URI = os.getenv("DB_URI")
        conn = psycopg2.connect(DB_URI)
        print("connected to DB")
        return conn
    except psycopg2.Error as e:
        print("Error connecting to PostgreSQL:", e)

conn = connect_to_db()


"""
Queries
"""
CREATE_LINKS_TABLE = """
CREATE TABLE IF NOT EXISTS links (
    id SERIAL PRIMARY KEY,
    original_link VARCHAR(255),
    shortened_link VARCHAR(255),
    no_of_clicks INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""

CREATE_CLICKS_TABLE = """
CREATE TABLE IF NOT EXISTS clicks (
    id SERIAL PRIMARY KEY,
    original_link VARCHAR(255),
    shortened_link VARCHAR(255),
    ip_address VARCHAR(45),
    device_type VARCHAR(255),
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
"""



"""
Running Queries at the start
"""
def create_tables():
    cur = conn.cursor()
    try:
        cur.execute(CREATE_LINKS_TABLE)
        cur.execute(CREATE_CLICKS_TABLE)
    except:
        print("error creating tables")
    conn.commit()
    cur.close()

create_tables()

"""
Routes mapping 
"""
@app.route('/', methods=['GET'])
def hello_world():
    return "Hello, World!"


@app.route('/create', methods=['POST'])
def create_short_link():
    long_link = request.args["link"]
    shortened_link_id = ''.join(random.choices(string.ascii_letters, k=7))
    shortened_link = f'http://127.0.0.1:8080/{shortened_link_id}'
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO links (original_link, shortened_link) VALUES (%s, %s);", (long_link, shortened_link))
    except:
        print("Cant create new link")
        conn.rollback()
    conn.commit()
    return shortened_link


@app.route('/<string:item_id>', methods=["GET"])
def dynamic_endpoint(item_id):
    ip_address = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    shortened_link = f'http://127.0.0.1:8080/{item_id}'
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM links WHERE shortened_link = (%s);", (shortened_link,))
        rows = cur.fetchall()
        if len(rows) == 0:
            return "No Such link found"
        
        original_link = rows[0][1]

        cur.execute("UPDATE links SET no_of_clicks = (%s) WHERE id = (%s)", (rows[0][3]+1, rows[0][0]))
        cur.execute("INSERT INTO clicks (original_link, shortened_link, ip_address, device_type) VALUES ((%s),(%s),(%s),(%s));",(original_link, shortened_link, ip_address, user_agent))
        conn.commit()
    except psycopg2.Error as e:
        print("Cant redirect to original link", e)
        conn.rollback()
        return "Cant redirect to original link"
    
    return redirect(original_link, code = 302)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)