#!/usr/bin/python3
# template.py by Bill Weinman [http://bw.org/]
# created for Python 3 Essential Training on lynda.com
# Copyright 2010 The BearHeart Gorup, LLC
import sqlite3

_DBFILE = 'rss.db'

class rssDB:
    def __init__(self):
        self._db = sqlite3.connect(_DBFILE)
        self._db.row_factory = sqlite3.Row
        self._db.execute('''
            CREATE TABLE IF NOT EXISTS feed (
                id INTEGER PRIMARY KEY,
                url TEXT UNIQUE,
                title TEXT,
                description TEXT
            )
        ''')

    def insert(self, rec):
        self._db.execute('''
            INSERT into feed (url, title, description)
                VALUES (:url, :title, :description)
        ''', rec)
        self._db.commit()

    def getByURL(self, url):
        c = self._db.cursor()
        c.execute('SELECT * FROM feed WHERE url = ?', (url,))
        return c.fetchone()

    def getById(self, id):
        c = self._db.cursor()
        c.execute('SELECT * FROM feed WHERE id = ?', (id,))
        return c.fetchone()

    def update(self, rec):
        self._db.execute('''
            UPDATE feed
                SET title = :title, description = :description 
                WHERE url = :url
            ''', rec )
        self._db.commit()

    def delById(self, id):
        self._db.execute('DELETE from feed WHERE id = ?', (id,)) 
        self._db.commit()

    def list(self):
        c = self._db.cursor()
        c.execute('SELECT * FROM feed ORDER BY UPPER(title)')
        for r in c:
            yield r;

def main():
    db = rssDB()
    print('all recs from {}:'.format(_DBFILE))
    for r in db.list():
        print('{title} [{url}] {description}'.format(**r))

if __name__=='__main__': main()
