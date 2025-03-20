from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric.utils import encode_dss_signature, decode_dss_signature
import os

print("[ SECP256R1 ]")

# Key generation
private_key = ec.generate_private_key(ec.SECP256R1())

# Retrieve the public key
public_key = private_key.public_key()

public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.X962,
    format=serialization.PublicFormat.UncompressedPoint
)

# Convert to hexadecimal format
print("Public Key (Hex):", public_bytes.hex())


# Hash the message
message = b"Test message"
digest = hashes.Hash(hashes.SHA256())
digest.update(message)
hashed_message = digest.finalize()

# Sign the hash
signature = private_key.sign(hashed_message, ec.ECDSA(hashes.SHA256()))

# Split the signature into R and S components
r, s = decode_dss_signature(signature)
print(f"Signature (R, S): {r}, {s}")

# Verify the signature
try:
    public_key.verify(signature, hashed_message, ec.ECDSA(hashes.SHA256()))
    print("Signature is valid.")
except:
    print("Signature is invalid.")

"""
[ SECP256R1 ]
Public Key (Hex): 04cde53bfdef39bce05fd05239f31d70c207477ac39aef6fdc34a85a4f05c87d6c8df0507e89baf330e7da96a6496dde09671be8e06d765b7a3dae90f89bb87853
Signature (R, S): 73108869416324655262724221568022940909836222389054364123377279397472346560814, 92219505460915181273363284381229646603053437936899601202657356073817343838703
Signature is valid.
"""
