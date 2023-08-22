from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.fernet import Fernet
import base64

class KeyGenerator:
    @staticmethod
    def generate_key_pair():
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        private_key_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                    format=serialization.PrivateFormat.PKCS8,
                                                    encryption_algorithm=serialization.NoEncryption())
        public_key = private_key.public_key()
        public_key_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                  format=serialization.PublicFormat.SubjectPublicKeyInfo)
        
        with open('private_key.pem', 'wb') as private_key_file, open('public_key.pem', 'wb') as public_key_file:
            private_key_file.write(private_key_pem)
            public_key_file.write(public_key_pem)
        
        return private_key_pem, public_key_pem

class MessageEncryptor:
    @staticmethod
    def encrypt_message(public_key_pem, message):
        public_key = load_pem_public_key(public_key_pem)
        symmetric_key = Fernet.generate_key()
        f = Fernet(symmetric_key)
        encrypted_message = f.encrypt(message.encode())
        
        encrypted_symmetric_key = public_key.encrypt(
            symmetric_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        return base64.b64encode(encrypted_symmetric_key).decode(), encrypted_message.decode()

class MessageDecryptor:
    @staticmethod
    def decrypt_message(private_key_pem, encrypted_symmetric_key, encrypted_message):
        private_key = load_pem_private_key(private_key_pem, password=None)
        decrypted_symmetric_key = private_key.decrypt(
            base64.b64decode(encrypted_symmetric_key),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        f = Fernet(decrypted_symmetric_key)
        decrypted_message = f.decrypt(encrypted_message.encode()).decode()
        
        return decrypted_message

private_key, public_key = KeyGenerator.generate_key_pair()
print("Generated keys are saved in private_key.pem and public_key.pem files.")

message = "Hello, this is a secret message!"
encrypted_symmetric_key, encrypted_message = MessageEncryptor.encrypt_message(public_key, message)
print("Encrypted Symmetric Key:", encrypted_symmetric_key)
print("Encrypted Message:", encrypted_message)

decrypted_message = MessageDecryptor.decrypt_message(private_key, encrypted_symmetric_key, encrypted_message)
print("Decrypted Message:", decrypted_message)
