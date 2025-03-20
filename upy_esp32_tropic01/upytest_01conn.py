import sys
import uhashlib, ubinascii
from time import sleep, sleep_ms

from tropicsquare.ports.micropython import TropicSquareMicroPython
from machine import SPI, Pin

DEBUG_LOG = False


# Default factory pairing keys
pkey_index_0 = 0x00 # Slot 0
sh0priv = [0xd0,0x99,0x92,0xb1,0xf1,0x7a,0xbc,0x4d,0xb9,0x37,0x17,0x68,0xa2,0x7d,0xa0,0x5b,0x18,0xfa,0xb8,0x56,0x13,0xa7,0x84,0x2c,0xa6,0x4c,0x79,0x10,0xf2,0x2e,0x71,0x6b]
sh0pub  = [0xe7,0xf7,0x35,0xba,0x19,0xa3,0x3f,0xd6,0x73,0x23,0xab,0x37,0x26,0x2d,0xe5,0x36,0x08,0xca,0x57,0x85,0x76,0x53,0x43,0x52,0xe1,0x8f,0x64,0xe6,0x13,0xd3,0x8d,0x54]


print("[ SPI init ]")    
spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), miso=Pin(19), mosi=Pin(23))
cs = Pin(5, mode=Pin.OUT, value=1) # DummyNetworkSpiCSPin(spi)

ts = TropicSquareMicroPython(spi, cs)
    
print("Spect FW version: {}".format(ts.spect_fw_version))
print("RISCV FW version: {}".format(ts.riscv_fw_version))
# print("Chip ID: {}".format(ts.chipid))
try:
    print("FW Bank: {}".format(ts.fw_bank))
except Exception as e:
    print("Exception: {}".format(e))
    
chipid_hex = ts.chipid.hex()
print("[ chipID ] {}".format(chipid_hex))
# 1e2d4748b039fa77022c488fecfd9dc534103467dec9a512228a727c1771a201
# sleep(0.1)

sha256 = uhashlib.sha256()
sha256.update(str(chipid_hex).encode())
h=ubinascii.hexlify(sha256.digest()).decode()
print("[ sha256(chipID) ]", h)

print("="*30)
print("Starting secure session...")
print()
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))

sleep_ms(100)


if DEBUG_LOG:
    print("-"*30)
    print("[ Log ]")
    print(ts.get_log())
    
     
