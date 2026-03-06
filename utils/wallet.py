from database import conn


def get_balance(username):

    result = conn.execute(
        "SELECT balance FROM users WHERE username=?",
        (username,)
    ).fetchone()

    if result:
        return result[0]

    return 0


def update_balance(username, amount):

    conn.execute(
        "UPDATE users SET balance = balance - ? WHERE username=?",
        (amount, username)
    )

    conn.commit()


def add_money(username, amount):

    conn.execute(
        "UPDATE users SET balance = balance + ? WHERE username=?",
        (amount, username)
    )

    conn.commit()