import socket
from log import log

class Client:
	''' A conn class to directly interact with conn '''

	client_list=list()
	client_map=dict()

	def __init__(self, conn=None, addr=None):
		'''Constructor'''

		self.state='0001'
		self.addr=addr
		self.conn=conn

	def isalive(self, user):
		userconn=self.client_map.get(user, None)
		if userconn==None:
			return False
		try:
			userconn.conn.sendall(b'1010')
			return True

		except BrokenPipeError:
			if user in self.client_list:
				self.client_list.remove(user)
			if user in self.client_map.keys():
				self.client_map.pop(user)
			return False

	def set_name(self, name):
		self.name=name

	def get_name(self):
		return self.name

	def set_key(self, key):
		self.key=key

	def get_key(self):
		return self.key

	def send(self, message, encoding='utf-8'):
		'''send method to send to conn'''

		if encoding==False:
			message=message.strip()
		else:
			try:
				message=message.strip().encode(encoding)

			except ValueError as e:
				log.error(e)
				return False
		
		try:
			self.conn.sendall(message)
			log.debug("Message sent to conn" + str(message))
			return True
		except BrokenPipeError:
			return False

	def recvStatus(self):
		'''receive status bytes for upcoming data'''

		status=self.conn.recv(4)
		try:
			status=status.decode('utf-8')

		except ValueError as e:
			log.error(e)
			return None

		log.debug("Received status from conn: " + status)
		return status


	def recv(self, encoding='utf-8'):
		'''recv response from conn'''

		data=self.conn.recv(4096)
		if encoding==False:
			return data.strip()
		try:
			data=data.decode(encoding).strip()

		except ValueError as e:
			log.error(e)
			return None

		log.debug("Received data from conn: " + data)
		return data

	def get_state(self):
		'''get current state'''

		return self.state

	def set_state(self, new):
		'''update current state'''

		self.state=new
		return self.state


	def show(self):
		'''Print all variables'''

		print(self.__dict__)