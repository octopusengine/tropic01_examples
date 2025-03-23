# upy_01conn.py - connection

from time import sleep_ms
from upy_esp32_tropic01.tropic_upy_lib import  SW, print_head, ts, pkey_index_0, sh0priv, sh0pub

DEBUG_LOG = True

print_head("upy_01conn | Basic Connection",True)
# ts = TropicSquareMicroPython(spi, cs) ## init from lib 

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
    print("-" * SW)
    print("[ Log ]")
    print(ts.get_log())
    
"""
MPY: soft reboot
--------------------------------------------------
Lib. TropicSquareMicroPython | version: 0.0.1
upy_01conn | Basic Connection
--------------------------------------------------
Spect FW version: (0, 3, 1, 0)
RISCV FW version: (0, 1, 2, 0)
Exception: Response status is not OK (status: 0x7f)
[ chipID ] 0...01000000054400000000ffffffffffff01f00f000544545354303103001f00110b54524f50494330312d4553f...f71030300
--------------------------------------------------
[ Log ]
# 3215453 D(UI): RX: cmd=0x1
# 3215453 D(UI): RX: cmd=0x1
...

"""
