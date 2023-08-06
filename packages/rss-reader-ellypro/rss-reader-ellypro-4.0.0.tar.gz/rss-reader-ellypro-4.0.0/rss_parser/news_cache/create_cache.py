import sqlite3
from os.path import isfile, dirname, realpath


def create_cache(entries, date_attr):
    dir_path = dirname(realpath(__file__))
    db_path = dir_path + '/cache.db'
    # Creates database if it is not exists already
    if not isfile(db_path):
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()

        # Creating Table
        cur.execute('''CREATE TABLE RSS
                 (
                 TITLE           TEXT    NOT NULL,
                 LINK            CHAR(250)     NOT NULL,
                 DATE        CHAR(50),
                 SUMMARY         TEXT NOT NULL);''')

        # Inserting data to Table
        entry_list = []
        for e in entries:
            entry_list.append((e.title.text, e.link.get('href'),
                               ''.join(e.updated.text[:10].split('-')), e.summary.text))
        cur.executemany("insert into RSS (TITLE, LINK, DATE, SUMMARY) VALUES(?, ?, ?, ?);", entry_list)
        conn.commit()
        conn.close()

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        filtered_query = cur.execute("""SELECT * FROM RSS WHERE DATE=:date;""", {"date": date_attr})
        conn.commit()
        return filtered_query

