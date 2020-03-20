import sys
import socket 
import select 
import threading
import encryption
from log import log
from errors import err

# Username of the client made a Global var
MYNAME=""

# A synchronization variable
target_status=0
pub_key=""

def Sign():
	"""Asks whether user wants to sign in or signup"""

	signup=input("0 for Logging In,  1 for Signing Up: ")
	if signup not in ["0", "1"]:
		log.warning("Please enter 0 or 1")
		return signup, False
	return signup, True


def sendtoconn(server, messageBytes):
	

	try:
		server.sendall(messageBytes.encode('utf-8'))
	except IOError:
		log.critical("Can't send messages. Server has disconnected.")
		exit()

def startSession():

	# Chack if user wants a login or signup and send selection to server
	signup, status=Sign()
	if status is False:
		return False

	sendtoconn(server, signup)

	# take input for credentials and send to server
	global MYNAME
	username=input("Enter Username: ")
	MYNAME=username
	server.sendall(username.encode('utf-8'))
	password=input("Enter Password: ")
	server.sendall(password.encode('utf-8'))

	# generate public and private key for current session and import 
	# the public key and send to the server
	pub_key = encryption.gen_key()
	server.sendall(pub_key)
	log.info("Public Key sent to server.")

	# Wait for acknowledgement from server 1111 means successful anything else is failure
	status=server.recv(4)
	if  status == b'1111':
		log.info("Session created successfully.")
		return True
	else:
		error=err.get(status.decode('utf-8').strip(), "Unknown")
		log.warning(error)
		return False

def receive(server):
	message = server.recv(4096)
	
	global target_status
	global pub_key
	if message==b'0000':
		target_status=message
		receive(server)
	if message==b'1111':
		pub_key=server.recv(4096).decode('ascii').strip().encode('ascii')
		target_status=1
		receive(server)
	log.info("Message received from server.") 
	sys.stdout.write(encryption.decrypt(message).decode('ascii')) 
	sys.stdout.flush()
	receive(server)

def ackfromserver(server):
	ack = server.recv(4096)
	if ack==b'1111':
		return True
	else:
		return False

def send(server):
	target = sys.stdin.readline().strip() 
	server.sendall(target.encode('utf-8'))
	log.info("Intended target name: " + target + " sent to server.")
	global target_status
	global pub_key
	
	while(target_status==0):
		continue
	if target_status==b'0000':
		print(target, "is offline :( try someone else.")
		target_status=0
		return

	log.info("Public key of " + target + " for encryption received.")
	target_status=0
	while True:
		messageString = sys.stdin.readline().strip()
		if messageString=="exit":
			message_to_send=messageString.encode('utf-8')
		else:
			message_to_send=encryption.encrypt(("<" + MYNAME + ">: " + messageString).encode('utf-8'), pub_key)

		log.info("Encrypted message sent to server.")
		server.sendall(message_to_send) 
		print("<You> -> "+target+">: " + messageString) 
		if messageString=="exit":
			print("You have exited from chat.")
			continue
		if not ackfromserver(server):
			print("Target went offline.")
			continue


def communicate(server):

	t1=threading.Thread(target=receive,args=(server,))
	t1.start()
	while True:
		send(server)
	t1.join()
	server.close() 


if __name__ == '__main__':


	server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	if len(sys.argv) != 3: 
		log.error("Correct usage: script, IP address, port number.")
		exit() 

	IP_address = str(sys.argv[1]) 
	Port = int(sys.argv[2]) 

	log.debug("IP_address: " + IP_address)
	log.debug("Port: " + str(Port))
	server.connect((IP_address, Port))
	
	while True:
		if startSession():
			communicate(server)