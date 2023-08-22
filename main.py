from key_generator import KeyGenerator
from message_encryptor import MessageEncryptor
from message_verifier import MessageVerifier
import base64

private_key, public_key = KeyGenerator.generate_key_pair()
print("Generated keys are saved in private_key.pem and public_key.pem files.")

message = "Hello, this is a secret message!"
encrypted_symmetric_key, encrypted_message = MessageEncryptor.encrypt_message(public_key, message)
print("Encrypted Symmetric Key:", encrypted_symmetric_key)
print("Encrypted Message:", encrypted_message)

signature = "..."  # Replace with your signature
signature_valid = MessageVerifier.verify_signature(public_key, message, base64.b64decode(signature))
print("Signature Valid:", signature_valid)
