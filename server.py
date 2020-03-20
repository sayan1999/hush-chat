# Python program to implement server side of chat room. 
import socket 
import select 
import sys 
import threading
from log import log
from credential import verifyClient

threads=[]
list_of_clients=[]
keymap=dict()
connmap=dict()

def send(name, message):
	try:
		connmap[name].sendall(message)
		return True
	except IOError:
		log.info(name+ " went offline.")
		return False

def sendtoConn(conn, message):
	try:
		conn.sendall(message)
		return True
	except IOError:
		log.info("Target is not reachable.")
		return False

def clientthread(conn, addr): 
	
	user, pub_key, status = verifyClient(conn, list_of_clients)		
	if status != "1111":
		log.info("Client verification failed for client "+user+" conn: "+ addr[0]+ ":" +str(addr[1]))
		sendtoConn(conn, status.encode('utf-8'))
		log.info('Neg ack sent to '+ user)
		return False

	log.info("Client verification successful for client "+user+" conn: "+ addr[0]+ ":" +str(addr[1]))
	sendtoConn(conn, b'1111')
	log.info('Pos ack sent to ' +  user)

	list_of_clients.append(user)
	keymap[user] = pub_key	
	connmap[user] = conn
	log.debug(list_of_clients, keymap, connmap)

	while True:
		name = conn.recv(1024).decode('utf-8').strip()
		log.info(user + " wants to send messages to " + name)
		if name=="":
			if not checkIfAlive(user):
				return
			continue

		if name not in list_of_clients:
			log.info(name + " is offline")
			conn.sendall(b'0000')
			continue
		conn.sendall(b'1111')

		log.info(name + " is online")
		send(user, keymap[name])
		log.info("Pub key of " + name + " is sent to "+user)
		while True:
			message = conn.recv(1024)
			log.info("Received bytes from " + user)
			if message == b'':
				log.info("Received blank bytes from " + user)
				checkIfAlive(user)
				return
			if message == b'exit':
				log.info(user + " has exited from chat")
				send(name, (user + " has exited from chat").encode('utf-8'))
				break
			log.info("Forwarding messages of " + user + " to " + name)
			if not send(name, message):
				log.info(name + " went offline")
				send(user, b'0000')
				break
			send(user, b'1111') 
			log.info("Messages forwarded from " + user + " to " + name)


def checkIfAlive(user): 
	try:
		connmap[user].sendall("Please don't send blank messages".encode('utf-8'))
		return True
	except IOError:
		log.info("Client: "+user+" has disconnected :(")
		if user in list_of_clients: 
			list_of_clients.remove(user)
		connmap.pop(user, None) 
		keymap.pop(user, None) 
		return False


if __name__=='__main__':
	
	if len(sys.argv) != 3: 
		print ("Correct usage: script, IP address, port number")
		exit() 

	IP_address = str(sys.argv[1]) 
	Port = int(sys.argv[2]) 

	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	server.bind((IP_address, Port)) 
	server.listen(5)	

	while True: 

		conn, addr = server.accept()		
		print (addr[0], addr[1], " connected")
 
		t=threading.Thread(target=clientthread,args=(conn,addr))
		t.start()
		threads.append(t)

	for thread in threads:
		thread.join()

	server.close() 
