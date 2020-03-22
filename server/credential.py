import configparser
from log import log
from os.path import exists as fileexist
from client_class import Client

def registration(username, password):

	cfg = configparser.ConfigParser()
	if not fileexist('credentials.ini'):
		with open('credentials.ini', 'w+') as f:
			f.write('[users]')
			f.close()
			
	credentials=cfg.read('credentials.ini')

	pd=cfg.get('users', username, fallback='No such things as monsters.')	
	if pd != 'No such things as monsters.':
		log.info('User already registered')
		return '0011'

	cfg.set('users', username, password)	
	with open('credentials.ini', 'w') as configfile:
		cfg.write(configfile)
	return "0010"


def verify(username, password, client):

	if client.isalive(username):
		log.info("User already logged in.")
		return "1001"
	
	cfg = configparser.ConfigParser()
	credentials=cfg.read('credentials.ini')

	pd=cfg.get('users', username, fallback='No such things as monsters.')	
	if pd=='No such things as monsters.':
		log.info('User not registered')
		return "0100"

	if pd!=password:
		log.info('Incorrect password')
		return "0101"

	log.info("Logged in successfully")
	return "0010"


def verifyClient(conn, client):

	signup=conn.recv(1024).decode('utf-8').strip()
	username=conn.recv(1024).decode('utf-8').strip()
	password=conn.recv(1024).decode('utf-8').strip()
	log.debug("signup: " + signup)
	log.debug("username: " + username)
	log.debug("password: " + password)
	Client.kill_inactive()
	if int(signup):
		s=registration(username, password)
		if s != "0010":
			return (username, s)
	else:
		s = verify(username, password, client)
		if s != "0010":
			return (username, s)

	return username, "0010"