import sqlite3 as sql
from os.path import exists as fileexist
from log import log

class db:

	def __init__(self):
	
		conn=sql.connect('hush.db')
		cursor=conn.cursor()
		
		try:
			cursor.execute('CREATE TABLE texts (id integer primary key AUTOINCREMENT, recipient, message)')
		except sql.OperationalError:
			log.info("Table already exists")
		
		conn=sql.connect('keys.db')
		cursor=conn.cursor()
		try:
			cursor.execute('CREATE TABLE keys (recipient primary key, key)')
		except sql.OperationalError:
			log.info("Table already exists")

		conn.commit()

	def get_res(self, name):
		conn=sql.connect('hush.db')
		cursor=conn.cursor()
		cursor.execute('''SELECT * FROM texts WHERE recipient = ?''', (name, ))
		rows = cursor.fetchall()
		return rows

	def push_res(self, row):
		conn=sql.connect('hush.db')
		cursor=conn.cursor()
		cursor.execute('''INSERT INTO texts(recipient, message) VALUES(?, ?)''', row)
		conn.commit()
		return True

	def delete_res(self, row_id):
		conn=sql.connect('hush.db')
		cursor=conn.cursor()
		cursor.execute('DELETE FROM texts WHERE id=?', (row_id, ))
		conn.commit()

	def get_key(self, name):
		conn=sql.connect('keys.db')
		cursor=conn.cursor()
		cursor.execute('''SELECT key FROM keys WHERE recipient = ?''', (name, ))
		key = cursor.fetchone()
		if key==None:
			return None
		return key[0].encode('ascii')

	def set_key(self, name, key):
		key=key.decode('ascii')
		conn=sql.connect('keys.db')
		cursor=conn.cursor()
		cursor.execute('''SELECT * FROM keys WHERE recipient = ?''', (name, ))
		res = cursor.fetchone()
		if res==None:
			cursor.execute('''INSERT INTO keys(recipient, key) VALUES(?, ?)''', (name, key))
		else:
			cursor.execute('''UPDATE keys set key=? WHERE recipient = ?''', (key, name))
		conn.commit()

instance=db()