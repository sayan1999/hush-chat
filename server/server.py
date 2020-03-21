from _thread import start_new_thread
from client_class import Client
import socket
import pdb
from credential import verifyClient
from time import sleep
from sys import argv
from termcolor import colored
from db import instance

def debugging():
	client=Client()
	pdb.set_trace()

def client_gen(host, port):
	'''accepts and returns client connection'''

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	print("Successfully created socket")
	server.bind((host, port)) 
	server.listen(5)
	print("Listening at localhost:8080")
	while True:
		yield server.accept()

def startchat(client, name):
	'''start sending msg to clients'''
	
	while True:
		state=client.recvStatus()

		if state=='1000':
			name=client.recv()
			if not client.isalive(name):
				client.send('1100')
				continue
			else:
				client.send('1000')
				client.send(client.client_map[name].get_key(), False)
				continue
				
		if state=='1101':
			msg=client.recv(False)
			if client.client_map[name].send('1111') and client.client_map[name].send(msg, False):
				client.send('1101')
				continue
			else:
				if instance.push_res((name, msg)):
					client.send('1110')
					continue
				else:
					client.send('1011')
					continue

def check_backlog(client):

	rows=instance.get_res(client.get_name())
	
	for row in rows:
		id=row[0]
		if client.send('1111') and client.send(row[2], False):
			instance.delete_res(str(id))

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

	check_backlog(client)

	startchat(client, "")

def debugging():
	client=Client()
	pdb.set_trace()

def check_conn():
	while True:
		sleep(15)
		Client.kill_inactive()

if __name__=='__main__':
	'''main function'''

	if len(argv)!=3:
		print(colored("Correct Usage: script host port", 'red'))
		exit()
	host, port=argv[1], int(argv[2])

	start_new_thread(debugging, ())
	start_new_thread(check_conn, ())
	for connaddr in client_gen(host, port):		
		client=Client(connaddr[0], connaddr[1])
		print("One connection was received: ", client.addr)
		start_new_thread(client_thread, (client, ))