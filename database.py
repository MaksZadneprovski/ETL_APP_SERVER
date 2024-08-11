import json
import sqlite3
from contextlib import closing

DB_PATH = 'app.db'


def init_db():
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            db.execute('CREATE TABLE IF NOT EXISTS reports (report_id TEXT PRIMARY KEY, report_json TEXT)')
            db.execute('CREATE TABLE IF NOT EXISTS structures (engineer_id TEXT PRIMARY KEY, structure_json TEXT)')
            db.execute(
                'CREATE TABLE IF NOT EXISTS users (login TEXT PRIMARY KEY, password TEXT, is_admin INTEGER DEFAULT 0)')


def save_report(report_id, report_json):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            db.execute('REPLACE INTO reports (report_id, report_json) VALUES (?, ?)', (report_id, report_json))


def get_report(report_id):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            result = db.execute('SELECT report_json FROM reports WHERE report_id = ?', (report_id,)).fetchone()
            return result[0] if result else None


def save_structure(engineer_id, structure_json):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            db.execute('REPLACE INTO structures (engineer_id, structure_json) VALUES (?, ?)',
                       (engineer_id, structure_json))


def get_structure(engineer_id):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            result = db.execute('SELECT structure_json FROM structures WHERE engineer_id = ?',
                                (engineer_id,)).fetchone()
            return result[0] if result else None


def get_all_structures():
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            result = db.execute('SELECT structure_json FROM structures').fetchall()
            # Десериализация каждой JSON-строки в Python объект
            structures = [json.loads(row[0]) for row in result]
            return structures


def validate_credentials_db(login, password):
    with closing(sqlite3.connect(DB_PATH)) as db:
        result = db.execute('SELECT is_admin FROM users WHERE login = ? AND password = ?', (login, password)).fetchone()
        return {"is_valid": bool(result), "is_admin": bool(result[0])} if result else {"is_valid": False,
                                                                                       "is_admin": False}


def create_user(login, password, is_admin=False):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            db.execute('INSERT INTO users (login, password, is_admin) VALUES (?, ?, ?)',
                       (login, password, int(is_admin)))


def delete_user(login):
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            db.execute('DELETE FROM users WHERE login = ?', (login,))


def get_all_users():
    with closing(sqlite3.connect(DB_PATH)) as db:
        with db:
            result = db.execute('SELECT login FROM users').fetchall()
            return [row[0] for row in result]
