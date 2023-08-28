from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

class MessageVerifier:
    @staticmethod
    def verify_signature(public_key_pem, message, signature):
        # Load the public key from PEM format
        public_key = load_pem_public_key(public_key_pem)
        
        try:
            # Verify the signature using PSS padding and SHA-256 hashing
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

def main():
    # Example usage
    public_key_pem = ...  # Load the public key PEM
    message = "Hello, this is the message to verify."
    signature = ...  # Load the signature

    verifier = MessageVerifier()
    is_verified = verifier.verify_signature(public_key_pem, message, signature)

    if is_verified:
        print("Signature verified: The message is authentic.")
    else:
        print("Signature verification failed: The message may be tampered with.")

if __name__ == "__main__":
    main()
