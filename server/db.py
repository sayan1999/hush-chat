import sqlite3 as sql
from os.path import exists as fileexist
from log import log

class db:

	def __init__(self):
		self.conn=sql.connect('hush.db')
		self.createtable()

	def createtable(self):
		cursor=self.conn.cursor()
		try:
			cursor.execute('CREATE TABLE texts (id integer primary key AUTOINCREMENT, recipient, message)')
		except sql.OperationalError:
			log.info("Table already exists")

		self.conn.commit()

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
		cursor.execute('DELETE FROM texts WHERE id=?', row_id)
		conn.commit()

instance=db()