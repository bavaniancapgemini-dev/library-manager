import sqlite3

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS users(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT UNIQUE,

password TEXT,

role TEXT

)

""")

connection.commit()

connection.close()

def register(username,password,role):

    conn=sqlite3.connect("users.db")

    cursor=conn.cursor()

    cursor.execute(

        "INSERT INTO users(username,password,role) VALUES(?,?,?)",

        (username,password,role)

    )

    conn.commit()

    conn.close()

def login(username,password):

    conn=sqlite3.connect("users.db")

    cursor=conn.cursor()

    cursor.execute(

        """

        SELECT role

        FROM users

        WHERE username=? AND password=?

        """,

        (

            username,

            password

        )

    )

    user=cursor.fetchone()
    
    if user:

        from datetime import datetime

        cursor.execute(

        """

        INSERT INTO login_history(

        username,

        login_time

        )

        VALUES(?,?)

        """,

        (

            username,

            datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        )

    )

    conn.commit()

    conn.close()

    return user

connection = sqlite3.connect("users.db")

cursor = connection.cursor()

cursor.execute("""

CREATE TABLE IF NOT EXISTS login_history(

id INTEGER PRIMARY KEY AUTOINCREMENT,

username TEXT,

login_time TEXT

)

""")

connection.commit()

connection.close()