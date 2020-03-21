from _thread import start_new_thread
from client_class import Client
import socket
import pdb
from credential import verifyClient

def client_gen():
	'''accepts and returns client connection'''

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	print("Successfully created socket")
	server.bind(('localhost', 8080)) 
	server.listen(5)
	print("Listening at localhost:8080")
	while True:
		yield server.accept()

def startchat(client, name):
	'''start sending msg to clients'''
	
	state=client.recvStatus()

	if state=='1000':
		name=client.recv()
		if not client.isalive(name):
			client.send('1100')
			return startchat(client, name)
		else:
			client.send('1000')
			client.send(client.client_map[name].get_key(), False)
			return startchat(client, name)
			
	if state=='1101':
		msg=client.recv(False)
		if client.client_map[name].send('1111') and client.client_map[name].send(msg, False):
			client.send('1101')
			return startchat(client, name)
		else:
			client.send('1110')
			return startchat(client, name)


def client_thread(client):
	'''working thread for  a client'''
	
	user, status= '', 0
	
	while status != '0010':
		state=client.recvStatus()
		user, status = verifyClient(client.conn, client)
		client.send(status)
	
	client.client_list.append(user)
	client.client_map[user]=client
	client.set_name(user)
	client.set_key(client.recv(False))
	client.send('0111')

	startchat(client, "")


if __name__=='__main__':
	'''main function'''

	client=Client()
	start_new_thread(pdb.set_trace, ())
	for connaddr in client_gen():		
		client=Client(connaddr[0], connaddr[1])
		print("One connection was received: ", client.addr)
		start_new_thread(client_thread, (client, ))