from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.fernet import Fernet
import base64

def encrypt_message(public_key_pem, message):
    # Load the public key from its PEM format
    public_key = load_pem_public_key(public_key_pem)
    
    # Generate a symmetric key for encrypting the message
    symmetric_key = Fernet.generate_key()
    
    # Encrypt the message using the symmetric key
    f = Fernet(symmetric_key)
    encrypted_message = f.encrypt(message.encode())
    
    # Encrypt the symmetric key using the public key
    encrypted_symmetric_key = public_key.encrypt(
        symmetric_key,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    return base64.b64encode(encrypted_symmetric_key).decode(), encrypted_message.decode()

def decrypt_message(private_key_pem, encrypted_symmetric_key, encrypted_message):
    # Load the private key from its PEM format
    private_key = load_pem_private_key(private_key_pem, password=None)
    
    # Decrypt the symmetric key using the private key
    decrypted_symmetric_key = private_key.decrypt(
        base64.b64decode(encrypted_symmetric_key),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    # Decrypt the message using the decrypted symmetric key
    f = Fernet(decrypted_symmetric_key)
    decrypted_message = f.decrypt(encrypted_message.encode()).decode()
    
    return decrypted_message
