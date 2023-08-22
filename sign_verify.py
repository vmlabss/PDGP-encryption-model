from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key

class MessageVerifier:
    @staticmethod
    def verify_signature(public_key_pem, message, signature):
        public_key = load_pem_public_key(public_key_pem)
        
        try:
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
