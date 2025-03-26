# upy_01conn.py - basic connection, secure session, ping

from time import sleep_ms
from upy_esp32_tropic01.tropic_upy_lib import  SW, print_head, ts, pkey_index_0, sh0priv, sh0pub

DEBUG_LOG = True
TEST_PING = True

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

print("=" * SW)
print("Starting secure session...\n")
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))

if TEST_PING:
    print("[ test ping ]")
    try:
        resp = ts.ping(b"Hello Tropic Square From MicroPython!")
        print("Ping: {}".format(resp))
    except Exception as e:
        print("Exception: {}".format(e))

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
[ chipID ] 0...01000000054400000000ffffffffffff01f00f000544545354303103001f
00110b54524f50494330312d4553ffffffff0001000f...f71030300
==================================================
Starting secure session...

[ test ping ]
Ping: b'Hello Tropic Square From MicroPython!'
--------------------------------------------------
[ Log ]
# 465122 D(UI): RX: cmd=0x1
# 465127 D(UI): RX: cmd=0x1
# 465132 D(UI): RX: cmd=0x1
# 465137 D(UI): RX: cmd=0x1
# 465550 D(UI): RX: cmd=0x2
# 465581 X(TLS) pub: 4a 27 ee ee 8a b1 2b 1c c0 1a 5c 02 06 8b b8 df
c9 de c1 3e 67 ea e7 02 05 fb 0b 1a a3 30 2b 41

# 465696 D(UI): RX: cmd=0x1
# 465735 D(UI): RX: cmd=0x1
# 465773 D(UI): RX: cmd=0x1
# 465811 D(UI): RX: cmd=0x1
# 467049 D(UI): RX: cmd=0x4
# 467049 D(CMD3): len 54/54
# 467053 D(SECCHNL): N: 0
# 467053 D(CPB): ST: 101
# 467053 D(CMD3): L3 cmd 4: 1, len: 38
# 467053 D(L3): ping, l=38
# 467076 I(CMD3): TX: 0/54, l=54
# 467076 I(CMD3): sent
"""
