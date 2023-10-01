from key_generator import KeyGenerator
from message_encryptor import MessageEncryptor
from message_verifier import MessageVerifier
import base64

def main():
    # Generate and save the private and public keys
    private_key, public_key = KeyGenerator.generate_key_pair()
    print("Generated keys are saved in private_key.pem and public_key.pem files.")

    message = "Hello, this is a secret message!"
    
    # Encrypt the message
    encrypted_symmetric_key, encrypted_message = MessageEncryptor.encrypt_message(public_key, message)
    print("Encrypted Symmetric Key:", encrypted_symmetric_key)
    print("Encrypted Message:", encrypted_message)
    
    signature = "..."  # Replace with your actual signature
    
    # Verify the signature
    verifier = MessageVerifier()
    signature_valid = verifier.verify_signature(public_key, message, base64.b64decode(signature))
    
    if signature_valid:
        print("Signature is valid: The message is authentic.")
    else:
        print("Signature verification failed: The message may be tampered with.")

if __name__ == "__main__":
    main()
