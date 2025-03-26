from time import sleep_ms
import uhashlib, ubinascii
from upy_esp32_tropic01.tropic_upy_lib import  SW, print_head, ts, pkey_index_0, sh0priv, sh0pub

DEBUG_LOG = False

print_head("upy_02data | read data | simple XOR test",True)

print("Starting secure session...\n")
ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub))

sleep_ms(100)
print("[ test memory data ]")

# ts.mem_data_write(test_data, 0) # sha256(chip_id)
"""
hex_key = '0c1e24e5917779d297e14d45f14e1a1a' # andreas
byte_array_key = bytes.fromhex(hex_key)
# ts.mem_data_erase(1)
ts.mem_data_write(byte_array_key, 1) # test
# constant/cmd_result/: TropicSquareError: Command failed with result: 0x10 == CMD_RESULT_MEM_WRITE_FAIL
# ---> First, it is necessary to perform mem_data_erase(mem_index)
"""

sleep_ms(100)
data0 =  ts.mem_data_read(0) # slot0
print("  data0:",data0) 	 # empty
data1 =  ts.mem_data_read(1)
print("  data1:",data1)     # andreas
# print("data1hex:",data1.hex())

print("=" * SW)
# ----------XOR-------------
key = data1.hex()
msg_str = 'Test Msg ABC123'  # string
msg = bytearray(msg_str, 'ut 8')

print("    key:",key," | ",len(key))
print("    msg:",msg," | ",len(msg))
mhx = msg.hex()
print("msg_hex:",mhx)

result_hex = hex(int(key, 16) ^ int(mhx, 16))
print("result_hex:",result_hex) # "secret" msg

retrieved_msg_num = int(result_hex, 16) ^ int(key, 16) # "decode"
# print("retrieved_msg_num:",retrieved_msg_num)

retrieved_msg_hex = hex(retrieved_msg_num)[2:]  # Removing '0x' prefix
retrieved_msg = bytearray.fromhex(retrieved_msg_hex).decode('utf-8')

print("Original message (retrieved):", retrieved_msg)

"""
MPY: soft reboot
--------------------------------------------------
Lib. TropicSquareMicroPython | version: 0.0.1
upy_02data | read data | simple XOR test
--------------------------------------------------
Starting secure session...

[ test memory data ]
  data0: b''
  data1: b'\x0c\x1e$\xe5\x91wy\xd2\x97\xe1ME\xf1N\x1a\x1a'
==================================================
    key: 0c1e24e5917779d297e14d45f14e1a1a  |  32
    msg: bytearray(b'Test Msg ABC123')  |  15
msg_hex: 54657374204d736720414243313233
result_hex: 0xc4a4196e55734a1f0c10c07b27f2829
Original message (retrieved): Test Msg ABC123
"""
