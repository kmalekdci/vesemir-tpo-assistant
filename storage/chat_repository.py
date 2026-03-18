import sqlite3
import uuid
from datetime import datetime

DB_FILE = "db/chats.db"


def conn():
    return sqlite3.connect(DB_FILE)


def init_db():

    c = conn()
    cur = c.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS chats(
        id TEXT PRIMARY KEY,
        title TEXT,
        created_at TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        role TEXT,
        content TEXT,
        tokens INTEGER,
        created_at TEXT
    )
    """)

    c.commit()
    c.close()


def create_chat():

    chat_id = str(uuid.uuid4())

    c = conn()
    cur = c.cursor()

    cur.execute(
        "INSERT INTO chats VALUES (?,?,?)",
        (chat_id, "New Chat", datetime.utcnow().isoformat())
    )

    c.commit()
    c.close()

    return chat_id


def set_title(chat_id, title):

    c = conn()
    cur = c.cursor()

    cur.execute(
        "UPDATE chats SET title=? WHERE id=?",
        (title, chat_id)
    )

    c.commit()
    c.close()


def list_chats():

    c = conn()
    cur = c.cursor()

    cur.execute(
        "SELECT id, title FROM chats ORDER BY created_at DESC"
    )

    rows = cur.fetchall()
    c.close()

    return rows


def delete_chat(chat_id):

    c = conn()
    cur = c.cursor()

    cur.execute("DELETE FROM chats WHERE id=?", (chat_id,))
    cur.execute("DELETE FROM messages WHERE chat_id=?", (chat_id,))

    c.commit()
    c.close()


def save_message(chat_id, role, content, tokens):

    c = conn()
    cur = c.cursor()

    cur.execute(
        """INSERT INTO messages(chat_id,role,content,tokens,created_at)
        VALUES (?,?,?,?,?)""",
        (chat_id, role, content, tokens, datetime.utcnow().isoformat())
    )

    c.commit()
    c.close()


def load_messages(chat_id):

    c = conn()
    cur = c.cursor()

    cur.execute(
        "SELECT role, content FROM messages WHERE chat_id=? ORDER BY id",
        (chat_id,)
    )

    rows = cur.fetchall()
    c.close()

    return [
        {"role": role, "content": content}
        for role, content in rows
    ]
