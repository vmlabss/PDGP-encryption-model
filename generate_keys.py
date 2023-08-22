from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

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

private_key, public_key = generate_key_pair()
print("Generated keys are saved in private_key.pem and public_key.pem files.")
