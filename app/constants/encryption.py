from cryptography.fernet import Fernet

CIPHER_KEY = Fernet.generate_key()
CIPHER = Fernet(CIPHER_KEY)
