import sqlite3
import bcrypt

DB_NAME = "data.db"

def connect():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

def create_tables():
    conn = connect()
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password BLOB,
        role TEXT
    )
    """)

    c.execute("""
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        age INTEGER,
        income INTEGER,
        loan INTEGER,
        credit INTEGER,
        probability REAL,
        result TEXT
    )
    """)

    conn.commit()
    conn.close()

# AUTH
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def add_user(username, password, role):
    conn = connect()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username,password,role) VALUES (?,?,?)",
                  (username, hash_password(password), role))
        conn.commit()
        return True
    except:
        return False

def get_user(username):
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone()

def get_users():
    conn = connect()
    return conn.execute("SELECT id,username,role FROM users").fetchall()

# DATA
def save_history(age, income, loan, credit, prob, result):
    conn = connect()
    c = conn.cursor()
    c.execute("""
    INSERT INTO history (age,income,loan,credit,probability,result)
    VALUES (?,?,?,?,?,?)
    """, (age,income,loan,credit,prob,result))
    conn.commit()

def get_history():
    conn = connect()
    return conn.execute("SELECT * FROM history").fetchall()