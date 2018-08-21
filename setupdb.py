import sqlite3


def init_db():
    conn = sqlite3.connect("scores.db")

    cur = conn.cursor()
    cur.execute("drop table if exists highscores")
    cur.execute("create table highscores(name text, score integer)")

    conn.commit()
    conn.close()
