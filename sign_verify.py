from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key

def sign_message(private_key_pem, message):
    # Load the private key from its PEM format
    private_key = load_pem_private_key(private_key_pem, password=None)
    
    # Sign the message using the private key
    signature = private_key.sign(
        message.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_signature(public_key_pem, message, signature):
    # Load the public key from its PEM format
    public_key = load_pem_public_key(public_key_pem)
    
    try:
        # Verify the signature using the public key
        public_key.verify(
            signature,
            message.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except:
        return False
