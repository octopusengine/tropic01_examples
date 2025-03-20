from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import hashes, serialization

print("[ ed25519 ]")


# Key generation
private_key = ed25519.Ed25519PrivateKey.generate()

# Retrieve the public key
public_key = private_key.public_key()

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
)

# Convert to hexadecimal format
print("Public Key (Hex):", public_bytes.hex())


# Sign the message
message = b"Test message"
signature = private_key.sign(message)

# Verify the signature
try:
    public_key.verify(signature, message)
    print("Signature is valid.")
except:
    print("Signature is invalid.")

"""
[ ed25519 ]
Public Key (Hex): 05dca5eec85ac7eb03e76161f25120e28b045be8b3353d26c0eb4bd1b6e2fef6
Signature is valid.
"""
