import socket
from log import log

class Server:
	''' A server class to directly interact with server '''

	def __init__(self, localhost, port):
		'''Constructor'''

		self.state='0000'
		self.addr=(localhost, port)
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.connect(self.addr)
		self.state='0001'
		self.respQ=[]

	
	def store(self, data):
		'''store msges in the Q'''
		self.respQ.append(data)

	def extract(self):
		'''blocking extraction of msg from Q'''

		while True:
			try:
				return self.respQ.pop(0)
			except IndexError:
				continue

	def send(self, message, encoding='utf-8'):
		'''send method to send to server'''

		if encoding==False:
			message=message.strip()
			
		else:
			try:
				message=message.strip().encode(encoding)

			except ValueError as e:
				log.error(e)
				return False
		
		log.debug("Message encoded into: " + str(message))
		self.server.sendall(message)
		log.info("Message sent to server")
		return True

	def recvStatus(self):
		'''receive status bytes for upcoming data'''

		status=self.server.recv(4)
		try:
			status=status.decode('utf-8')

		except ValueError as e:
			log.error(e)
			return None

		log.info("Received status from server: "+status)
		return status


	def recv(self, encoding='utf-8'):
		'''recv response from server'''

		data=self.server.recv(4096)
		if encoding==False:
			return data.strip()

		try:
			data=data.decode(encoding).strip()

		except ValueError as e:
			log.error(e)
			return None

		log.info("Received data from server: " + data)
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
