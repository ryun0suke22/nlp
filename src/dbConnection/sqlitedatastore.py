import json
import sqlite3

conn = None


def connect():
    global conn
    conn = sqlite3.connect('./sample.db')


def close():
    conn.close()


def create_table():
    conn.execute('DROP TABLE IF EXISTS docs')
    conn.execute('''CREATE TABLE docs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            content     TEXT,
            meta_info   BLOB,
            sentence    BLOB,
            chunk       BLOB,
            token       BLOB
        )''')

### be aware of risk of SQL injections. (only hobby use.)
def load(values):
    conn.executemany(
        'INSERT INTO docs (content, meta_info) VALUES (?,?)',
        values)
    conn.commit()


def get(doc_id, fl):
    row_ls = conn.execute(
        'SELECT {} FROM docs WHERE id = ?'.format(','.join(fl)),
        (doc_id,)).fetchone()
    row_dict = {}
    for key, value in zip(fl, row_ls):
        row_dict[key] = value
    return row_dict


def get_all_ids(limit, offset=0):
    return [record[0] for record in
            conn.execute(
        'SELECT id FROM docs LIMIT ? OFFSET ?',
        (limit, offset))]


def set_annotation(doc_id, name, value):
    conn.execute(
        'UPDATE docs SET {0} = ? where id = ?'.format(name),
        (json.dumps(value), doc_id))
    conn.commit()


def get_annotation(doc_id, name):
    row = conn.execute(
        'SELECT {0} FROM docs WHERE id = ?'.format(name),
        (doc_id,)).fetchone()
    if row[0] is not None:
        return json.loads(row[0])
    else:
        return []
