import bcrypt
from database import conn


def create_user(username, password):

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    conn.execute(
        "INSERT INTO users(username,password) VALUES (?,?)",
        (username, hashed)
    )

    conn.commit()


def login_user(username, password):

    user = conn.execute(
        "SELECT password FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if user:

        if bcrypt.checkpw(password.encode(), user[0]):
            return True

    return False