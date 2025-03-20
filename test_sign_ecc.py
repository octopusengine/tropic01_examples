import hashlib
from ecdsa import VerifyingKey, NIST256p, util

message = b"abc"
pubkey_hex = "90cf272a6b284f33f20a5e3506b0ebf29b5259db4323f9e21036961eba98e09c678ab1db7ea681f07a09b5e09072c4d4f97003da6937da695440ed43aefa52f9"
R = "4cc9f47d24b6cb2d8edc82b71a62a0e0e354fa9027805385cd4e73778ecbf757"
S = "be798b2122cd9313055e245a81ed80f5060ba83903c7ff31b090de3a4a07f99d" 

# ========================================

pubkey_bytes = bytes.fromhex(pubkey_hex)
vk = VerifyingKey.from_string(pubkey_bytes, curve=NIST256p)

hashed_message = hashlib.sha256(message).digest()
print("hashed_message",hashed_message.hex())
print("R:",R)
print("S:",S)
# Concatenate raw R and S bytes
r_bytes = bytes.fromhex(R)
s_bytes = bytes.fromhex(S)
rs_raw = r_bytes + s_bytes  # 64 bytes total

try:
    # Specify that the signature is raw (concatenated R||S)
    valid = vk.verify_digest(rs_raw, hashed_message, sigdecode=util.sigdecode_string)
    print("Signature is valid:", valid)
except Exception as e:
    print("Signature verification failed:", e)

"""
ESP32 MicroPython
hashed_message: ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
--------------------------------
[Slot] 1
ecc_key: 90cf272a6b284f33f20a5e3506b0ebf29b5259db4323f9e21036961eba98e09c678ab1db7ea681f07a09b5e09072c4d4f97003da6937da695440ed43aefa52f9
R: 4cc9f47d24b6cb2d8edc82b71a62a0e0e354fa9027805385cd4e73778ecbf757
S: be798b2122cd9313055e245a81ed80f5060ba83903c7ff31b090de3a4a07f99d

-->
Python Validation
hashed_message ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad
R: 4cc9f47d24b6cb2d8edc82b71a62a0e0e354fa9027805385cd4e73778ecbf757
S: be798b2122cd9313055e245a81ed80f5060ba83903c7ff31b090de3a4a07f99d
Signature is valid: True
"""