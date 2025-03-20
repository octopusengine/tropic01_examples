from time import sleep_ms
import uhashlib, ubinascii
from tropic_upy_lib import ts, pkey_index_0, sh0priv, sh0pub

DEBUG_LOG = False

print("=" * 30)
print("Signing SHA256 hash with TROPIC01 (SECP256R1)...")

print("=" * 32)
print("Starting secure session...\n")
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))

sleep_ms(300)
print("pkey_index_0:",pkey_index_0)
try:
    print("FW Bank: {}".format(ts.fw_bank))
except Exception as e:
    print("Exception: {}".format(e))

def print_ecc_key0(slot):
    print("-"*32)
    print("[slot]", slot)
    ecc_tuple = ts.ecc_key_read(slot)
    print(ecc_tuple)
    ecc_key = ecc_tuple[2]
    print("ecc_key",slot,":",ecc_key.hex())

def print_ecc_key(slot):
    print("-" * 32)
    print("[Slot]", slot)
    
    try:
        # Attempt to read the ECC key from the specified slot.
        ecc_tuple = ts.ecc_key_read(slot)
    except Exception as e:
        # If an error occurs (e.g., key not present), print the error message.
        print("Error reading ECC key from slot", slot, ":", e)
        print("Generating new ECC key in slot", slot)
        try:
            # Generate a new ECC key in the given slot using P256 (curve value 1).
            ts.ecc_key_generate(slot, 1)
        except Exception as gen_err:
            print("Error generating ECC key in slot", slot, ":", gen_err)
            return
        
        try:
            # Try reading the key again after generation.
            ecc_tuple = ts.ecc_key_read(slot)
        except Exception as e2:
            print("Error reading ECC key after generation from slot", slot, ":", e2)
            return
    
    # Print the tuple returned from ecc_key_read.
    if DEBUG_LOG:
        print(ecc_tuple)
    # The third element of the tuple contains the public ECC key.
    ecc_key = ecc_tuple[2]
    print("ecc_key:", ecc_key.hex())


message = b"abc"
sha256 = uhashlib.sha256()
sha256.update(message)
hashed_message = sha256.digest()  # hashed_message má délku 32 bajtů
print("hashed_message:",hashed_message.hex())

print_ecc_key(1)
rs = ts.ecdsa_sign(1, hashed_message) # slot: int, hash: bytes
print("R:",rs[0].hex())
print("S:",rs[1].hex())

"""
print_ecc_key(2)
rs = ts.ecdsa_sign(2, hashed_message)
print("R:",rs[0].hex())
print("S:",rs[1].hex())
"""

if DEBUG_LOG:
    print("-"*30)
    print("[ Log ]")
    print(ts.get_log())
    
    
"""
Starting secure session...

len(ecc_key) 128
--------------------------------
[Slot] 1
ecc_key: 90cf272a6b284f33f20a5e3506b0ebf29b5259db4323f9e21036961eba98e09c678ab1db7ea681f07a09b5e09072c4d4f97003da6937da695440ed43aefa52f9
R: 4cc9f47d24b6cb2d8edc82b71a62a0e0e354fa9027805385cd4e73778ecbf757
S: be798b2122cd9313055e245a81ed80f5060ba83903c7ff31b090de3a4a07f99d

...
--------------------------------
[Slot] 2
Error reading ECC key from slot 2 : Command failed with result: 0x12
Generating new ECC key in slot 2
(1, 1, b'\x84G\t\xbb\x85\xb7\x16\xc3*\xbd\xcb\x1b\xd8`\xad\xff$"]\xe1\xdfv;\xe6$\xb6\xd3\xe8\xa9Ai\xbe\xae\xaa(\xcc\xd0~\xactB[\xe4\xda\xb2\x86\xae\xceu\x9b\xf1d8\xa9\xb2\x03\xd4\x84\x0b0\xea\xd4\xe9\xad')
ecc_key 2 : 844709bb85b716c32abdcb1bd860adff24225de1df763be624b6d3e8a94169beaeaa28ccd07eac74425be4dab286aece759bf16438a9b203d4840b30ead4e9ad
R: ca8c9f633ac9ac247a77775b2752a94b06f007190753fdcf9c06ee19ad2badc1
S: 54280decbbf13f79534911a507ffec726e8ca9ca674ee3b2755a37ad950fcd65
"""

    
     





