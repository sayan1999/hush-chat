from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from log import log

private_key=""

def gen_key(username):
	global private_key
	pem=""
	public_key=""
	try:
		with open(username+"private_key.pem", "rb") as key_file:
		    private_key = serialization.load_pem_private_key(
		        key_file.read(),
		        password=None,
		        backend=default_backend()
		    )
	except FileNotFoundError:
   		raise BaseException(username+"private_key.pem is missing")

	try:
		with open(username+"public_key.pem", "rb") as key_file:
		    public_key = serialization.load_pem_public_key(
		        key_file.read(),
		        backend=default_backend()
		    )	
	except FileNotFoundError:
   		raise BaseException(username+"public_key.pem is missing")

	pem=public_key.public_bytes(
	    encoding=serialization.Encoding.PEM,
	    format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return pem

def get_priv_key():
	return	private_key

def decrypt(messageBytes):
	original_message =  ''
	try:
		original_message=private_key.decrypt(
	    messageBytes,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )
	)
	
	except ValueError as e:
		log.error(e)
		log.error("Could not decrypt message")
		return str(messageBytes)

	return original_message

def encrypt(message, pem):
	
	messageBytes=message.encode('ascii')
	try:
		public_key = serialization.load_pem_public_key(
	        pem,
	        backend=default_backend()
	    )
	except TypeError:
		log.error("Encryption Error: Couldn't load public key")
		log.debug(pem)
		return message

	encrypted = public_key.encrypt(
	    messageBytes,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )
	) 
	return encrypted