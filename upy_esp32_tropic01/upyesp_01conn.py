# upy_01conn.py - connection

from time import sleep_ms
from tropic_upy_lib import ts, pkey_index_0, sh0priv, sh0pub

# ts = TropicSquareMicroPython(spi, cs)
DEBUG_LOG = True

print("Spect FW version: {}".format(ts.spect_fw_version))
print("RISCV FW version: {}".format(ts.riscv_fw_version))

try:
    print("FW Bank: {}".format(ts.fw_bank))
except Exception as e:
    print("Exception: {}".format(e))

# Read and hash chip ID
chipid_hex = ts.chipid.hex()
print("[ chipID ] {}".format(chipid_hex))

"""
print("=" * 32)
print("Starting secure session...\n")
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))
"""

if DEBUG_LOG:
    print("-" * 32)
    print("[ Log ]")
    print(ts.get_log())
