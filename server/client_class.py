import socket
from log import log
from _thread import exit_thread as stop_current_thread

class Client:
	''' A conn class to directly interact with conn '''

	client_list=list()
	client_map=dict()
	conn_list=list()

	def __init__(self, conn=None, addr=None):
		'''Constructor'''
		self.addr=addr
		self.conn=conn
		if conn!=None:
			Client.conn_list.append(self)

	@staticmethod
	def kill_inactive():
		'''Detect inactive connections and kill them'''

		for cli in Client.conn_list:
			c=cli.conn
			try:
				c.sendall(b'1010')
			except (BrokenPipeError, OSError):
				c.close()
				if cli in Client.conn_list:
					Client.conn_list.remove(cli)
				if cli.name in Client.client_list:
					Client.client_list.remove(cli.name)
				if cli.name in Client.client_map.keys():
					Client.client_map.pop(cli.name)
				log.debug("Current connection list :" + str(Client.conn_list))	

	@staticmethod
	def isalive(user):
		'''Check if a particular user is logged in'''

		userconn=Client.client_map.get(user, None)
		if userconn==None:
			return False
		return True

	def leave_list(self):
		self.conn.close()
		if self in self.conn_list:
			self.conn_list.remove(self)
		if self.name in self.client_list:
			self.client_list.remove(self.name)
		if self.name in self.client_map.keys():
			self.client_map.pop(self.name)


	def send(self, message, encoding='utf-8'):
		'''send method to send to conn'''

		if encoding!=False:
			try:
				message=message.encode(encoding)

			except ValueError as e:
				log.error(e)
				return False
		
		try:
			log.debug("Message to send " + str(message))
			self.conn.sendall(message)
			log.debug("Message sent to conn " + str(message))
			return True
		except (BrokenPipeError, OSError):
			log.error("Unable to send; " + self.name + " is not responding")
			return False

	
	def recv(self, size = 4096, encoding='utf-8'):
		'''recv response from conn'''

		datatype = "message" if size == 4096 else "status"
		data = ''
		
		try:
			data=self.conn.recv(size)
			if data==b'':
				self.leave_list()
				log.error("Unable to receive; " + self.name + " is not responding")
				print("Exiting Thread")
				stop_current_thread()
		except (OSError, BrokenPipeError) as e:
			log.error(e)
			self.leave_list()
			print("Exiting Thread")
			stop_current_thread()

		if encoding!=False:
			try:
				data=data.decode(encoding)

			except ValueError as e:
				log.error(e)

		log.debug("Received " + datatype + " from conn: " + str(data))
		return data

	def set_name(self, name):
		self.name=name

	def get_name(self):
		return self.name

	def show(self):
		'''Print all variables'''
		print(self.__dict__)