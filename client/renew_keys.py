from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import serialization
from os.path import exists as fileexist

NAME=input("Enter username: ").strip()

if fileexist(NAME+'private_key.pem'):
    prompt=input("Are you sure you want to proceed, you won't be able to read the unread messages sent to you till before your next login? y or n: ")
    if prompt=="n":
    	exit()

	
private_key = rsa.generate_private_key(
	public_exponent=65537,
	key_size=2048,
	backend=default_backend())

public_key = private_key.public_key()

pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open(NAME+'public_key.pem', 'wb') as f:
    f.write(pem)

pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

with open(NAME+'private_key.pem', 'wb') as f:
    f.write(pem)