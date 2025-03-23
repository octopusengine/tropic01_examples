from time import sleep_ms
import uhashlib, ubinascii
from upy_esp32_tropic01.tropic_upy_lib import  SW, print_head, ts, pkey_index_0, sh0priv, sh0pub

DEBUG_LOG = False

print_head("upy_03mcounter | Monotonic Counter",True)

print("Starting secure session...\n")
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))

sleep_ms(300)

"""
mcounter_init(self, index : int, value : int) -> bool:
mcounter_update(self, index : int) -> bool:
mcounter_get(self, index : int) -> int:
"""

print("ts.mcounter_init()",ts.mcounter_init(3,123))
print(ts.mcounter_get(3))
print("ts.mcounter_update()", ts.mcounter_update(3))
print(ts.mcounter_get(3))

if DEBUG_LOG:
    print("-"*30)
    print("[ Log ]")
    print(ts.get_log())


"""
MPY: soft reboot
--------------------------------------------------
Lib. TropicSquareMicroPython | version: 0.0.1
upy_03mcounter | Monotonic Counter
--------------------------------------------------
Starting secure session...

ts.mcounter_init() True
123
ts.mcounter_update() True
122
"""
