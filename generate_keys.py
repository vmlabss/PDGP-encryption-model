from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

def generate_key_pair():
    # Generate a new RSA private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    
    # Serialize the private key to PEM format
    private_key_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Extract the public key from the private key
    public_key = private_key.public_key()
    
    # Serialize the public key to PEM format
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Save the private and public keys to files
    with open('private_key.pem', 'wb') as private_key_file, open('public_key.pem', 'wb') as public_key_file:
        private_key_file.write(private_key_pem)
        public_key_file.write(public_key_pem)
    
    return private_key_pem, public_key_pem

def main():
    # Generate and save the private and public keys
    private_key, public_key = generate_key_pair()
    print("Generated keys are saved in private_key.pem and public_key.pem files.")

if __name__ == "__main__":
    main()
