from server_class import Server
from encryption import gen_key, encrypt, decrypt
from threading import Thread
from sys import stdout, stdin, argv
from errors import err
from termcolor import colored
from getpass import getpass as getPasswd

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


def sign(server):
	'''Sign in or sign up to the session'''
	
	while True:
		signup=input(colored("0 for Logging In,  1 for Signing Up: ", "cyan"))
		if signup not in ["0", "1"]:
			continue
		
		server.send('0001')
		server.send(signup)
		
		global MYNAME
		username=input(colored("Enter Username: ", "cyan"))
		MYNAME=username
		server.send(username)
		password=getPasswd()
		server.send(password)

		state=server.extract()

		if state != '0010':
			print(colored(err[state], 'red'))
			continue

		else:
			print(colored("login was successful", "white"))

		print(colored("Generating key for current session", "white"))
		server.send(gen_key(),  False)
		state=server.extract()

		if state != '0111':
			print(colored("Key was not accepted", "red"))
			continue

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

	while True:
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
			if state=='1011':
				print(colored("Message sending to " + friend + " failed", "red"))
				print(colored("Exiting from chat", "red"))
				break
			if state=='1101':
				continue

			if state==False:
				print(colored("You have exited from the chat", "white"))
				break


def recv(server):
	'''recv msg from server'''

	while True:
		state=server.recvStatus()
		if state=='1010':
			continue

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


if __name__ == '__main__':

	if len(argv)!=3:
		print(colored("Correct Usage: script host port", 'red'))
		exit()
	host, port=argv[1], int(argv[2])

	server = Server(host, port)
	t2=Thread(target=recv, args=(server,))
	t2.start()

	while not sign(server):
		continue

	t1=Thread(target=send, args=(server,))	
	t1.start()
	t1.join()
	t2.join()