import configparser
from log import log

def registration(username, password):

	cfg = configparser.ConfigParser()
	credentials=cfg.read('credentials.ini')

	pd=cfg.get('users', username, fallback='No such things as monsters.')	
	if pd != 'No such things as monsters.':
		log.info('User already registered')
		return '0000'

	cfg.set('users', username, password)	
	with open('credentials.ini', 'w') as configfile:
		cfg.write(configfile)
	return "1111"


def verify(username, password, list_of_clients):

	if username in list_of_clients:
		log.info("User already logged in.")
		return "0001"
	
	cfg = configparser.ConfigParser()
	credentials=cfg.read('credentials.ini')

	pd=cfg.get('users', username, fallback='No such things as monsters.')	
	if pd=='No such things as monsters.':
		log.info('User not registered')
		return "0010"

	if pd!=password:
		log.info('Incorrect password')
		return "0011"

	log.info("Logged in successfully")
	return "1111"


def verifyClient(conn, list_of_clients):

	signup=conn.recv(1024).decode('utf-8').strip()
	username=conn.recv(1024).decode('utf-8').strip()
	password=conn.recv(1024).decode('utf-8').strip()

	if int(signup):
		s=registration(username, password)
		if s != "1111":
			return (username, "", e)
	else:
		s = verify(username, password, list_of_clients)
		if s != "1111":
			return (username, "", e)

	pub_key=conn.recv(4096).decode('ascii').strip().encode('ascii')
	return username, pub_key, "1111"