from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key=""

def gen_key():
	global private_key
	private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend())

	public_key = private_key.public_key()

	pem = public_key.public_bytes(
	    encoding=serialization.Encoding.PEM,
	    format=serialization.PublicFormat.SubjectPublicKeyInfo
	)
	return pem

def get_priv_key():
	return	private_key

def decrypt(messageBytes):
	original_message = private_key.decrypt(
	    messageBytes,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )
	)
	return original_message

def encrypt(message, pem):
	
	messageBytes=message.encode('ascii')
	public_key = serialization.load_pem_public_key(
        pem,
        backend=default_backend()
    )
	encrypted = public_key.encrypt(
	    messageBytes,
	    padding.OAEP(
	        mgf=padding.MGF1(algorithm=hashes.SHA256()),
	        algorithm=hashes.SHA256(),
	        label=None
	    )
	) 
	return encrypted