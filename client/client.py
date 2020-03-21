from server_class import Server
from encryption import gen_key, encrypt, decrypt
from threading import Thread
from sys import stdout, stdin
from errors import err
import time
from termcolor import colored

MYNAME=""
pub_key=""

def read():
	'''read from stdin'''
	return stdin.readline().strip()

def write(data):
	'''write into stdout'''
	if type(data)!=str:
		data=data.decode('ascii')
	print(colored(data, 'green'))

def successprompt():
	print(colored(">>>: ", "magenta"), end=" ")

def sign(server):
	'''Sign in or sign up to the session'''
	
	signup=input("0 for Logging In,  1 for Signing Up: ")
	if signup not in ["0", "1"]:
		return sign(server)
	
	server.send('0001')
	server.send(signup)
	
	global MYNAME
	username=input("Enter Username: ")
	MYNAME=username
	server.send(username)
	password=input("Enter Password: ")
	server.send(password)

	state=server.recvStatus()

	if state != '0010':
		print(colored(err[state], 'red'))
		return sign(server)

	else:
		print(colored("login was successful", "white"))

	print(colored("Generating key for current session", "white"))
	server.send(gen_key(),  False)
	state=server.recvStatus()

	if state != '0111':
		print(colored("Key was not accepted", "red"))
		return sign(server)

	else:
		print(colored("Your session is end-to-end encrypted now", "white"))
	return True


def sendmsg(server):
	'''send messages to current receiver'''

	global MYNAME, pub_key
	msg=read()
	if msg=="exit":
		return False

	server.send('1101')
	msg=MYNAME + ": " + msg
	encrypted=encrypt(msg, pub_key)
	server.send(encrypted, False)
	
	state=server.extract()
	return state


def send(server):
	'''sending to the server'''

	print(colored("New recepient: ", 'cyan'))
	global pub_key
	friend = read() 
	server.send('1000')
	server.send(friend)

	state=server.extract()	
	if state=='1100':
		print(colored(friend + " is not available", "red"))
		return send(server)

	if state=='1000':
		print(colored(friend + " is online", "white"))
		pub_key=server.extract()

	while True:
		state=sendmsg(server)
		if state=='1110':
			print(colored(friend + " went offline", "red"))
			break
		if state=='1101':
			successprompt()

		if state==False:
			print(colored("You have exited from the chat", "white"))
			break

	return send(server)


def recv(server):
	'''recv msg from server'''

	state=server.recvStatus()
	if state=='1010':
		return recv(server)

	if state=='1000':
		# key recv
		server.store(state)
		key=server.recv(False)
		server.store(key)

	else:
		if state=='1111':
			encrypted=server.recv(False)
			decrypted=decrypt(encrypted)
			write(decrypted)

		else: 
			server.store(state)
	recv(server)


if __name__ == '__main__':

	server = Server('localhost', 8080)

	while not sign(server):
		continue

	t1=Thread(target=send, args=(server,))
	t2=Thread(target=recv, args=(server,))
	t1.start()
	t2.start()

	t1.join()
	t2.join()