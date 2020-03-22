import socket
from log import log
from _thread import exit_thread as stop_current_thread

class Server:
	''' A server class to directly interact with server '''

	def __init__(self, localhost, port):
		'''Constructor'''

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
		
		if encoding!=False:
			try:
				message=message.strip().encode(encoding)

			except ValueError as e:
				log.error(e)
				return False
		
		try:
			log.debug("Message to send " + str(message))
			if message==b'' or message == '':
				return 
			self.server.sendall(message)
			log.debug("Message sent to server " + str(message))
			return True
		except (BrokenPipeError, OSError):
			log.error("Unable to send; Server is unreachable")
			stop_current_thread()

	
	def recv(self, size = 4096, encoding='utf-8'):
		'''recv response from server'''

		datatype = "message" if size == 4096 else "status"
		data = ''
		
		try:
			data=self.server.recv(size)
			if data==b'':
				log.error("Unable to receive; Server is unreachable")
				stop_current_thread()
		except OSError as e:
			log.error(e)
			stop_current_thread()

		if encoding!=False:
			try:
				data=data.strip().decode(encoding)

			except ValueError as e:
				log.error(e)
				stop_current_thread()

		log.debug("Received " + datatype + " from server: " + str(data))
		return data

	def show(self):
		'''Print all variables'''
		print(self.__dict__)

	def close(self):
		self.server.close()
