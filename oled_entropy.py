
import sys
from time import sleep
from components.display_i2c_oled import Oled
from machine import SPI, I2C, Pin
from tropicsquare.ports.micropython import TropicSquareMicroPython

I2C_SCL_PIN = const(22)
I2C_SDA_PIN = const(21)
print("ESP32 | MicroPython | -> SPI | TROPIC01")
print("="*30)
print("[--- init ---] I2C ")
# i2c = I2C(sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN))
i2c = I2C(0, sda=Pin(I2C_SDA_PIN), scl=Pin(I2C_SCL_PIN), freq=400000)

print("[--- init ---] OLED display")
# oled = Oled(i2c, 0x3c, 128, 32)
oled = Oled(i2c, 0x3c, 128, 64)

print("[--- test ---]")
oled.text("octopusLAB", 20, 0)
# oled.pixel(50,50,1)
oled.show()

sleep(3)
# Default factory pairing keys
pkey_index_0 = 0x00 # Slot 0
sh0priv = [0x.....]
sh0pub  = [0x.....]

def draw_line(o,line_hex, y):
    x = 0
    for digit in line_hex:        
        bits = bin(int(digit, 16))[2:] # hex2bin
        # Manually pad with leading zeros so that the string is 4 characters long.
        if len(bits) < 4:
            bits = "0" * (4 - len(bits)) + bits
        for bit in bits:
            if bit == '1':
                o.pixel(x, y, 0)
            x += 1
    o.show()


def main():
    print("[SPI init]")
    spi = SPI(1, baudrate=1000000, polarity=0, phase=0, sck=Pin(18), miso=Pin(19), mosi=Pin(23))
    cs = Pin(5, mode=Pin.OUT, value=1) # DummyNetworkSpiCSPin(spi)

    ts = TropicSquareMicroPython(spi, cs)
    
    print("-"*32, "L2")
    print("RISCV FW version: {}".format(ts.riscv_fw_version))
    print("Spect FW version: {}".format(ts.spect_fw_version))    
     
    ver_bytes = ts.spect_fw_version
    # ver_num = int.from_bytes(ver_bytes, 'big') # 'big' little
        
    fw = ts.spect_fw_version # b'\x00\x02\x01\x00'
    """
    major = fw[0]         # 0
    minor = fw[1]         # 2
    patch = int(f"{fw[2]}{fw[3]}")  # 10

    version_str = "{}.{}.{}".format(major, minor, patch)
    print("? Ver:", version_str)
    """
    print("? Ver:", fw)
    #lcd.move_to(0, 1)
    #lcd.putstr("TROPIC01 " + version_str)
    oled.text("TROPIC01 " + str(fw), 20, 20)
    oled.show()
    
    #def draw_image(self, file="assets/octopus_image.pbm",iw = IMAGE_WIDTH, ih = IMAGE_HEIGHT):
    oled.draw_image("trsq128x64.pbm",128,64)
    #oled.fill(0)
    #oled.draw_image("trsq32x32.pbm",32,32)
    oled.invert(1)
    sleep(2)
    #oled.fill(0)

         
    print("-"*32)
    def extract_printable_sequences(data):
        sequences = []
        current = []
        for b in data:
            if 32 <= b <= 126:  # tisknutelný znak
                current.append(chr(b))
            else:
                if current:
                    sequences.append("".join(current))
                    current = []
        if current:
            sequences.append("".join(current))
        return sequences
        
    
    print("Chip ID: {}".format(ts.chipid))
    
    import re

    chip_id = ts.chipid

    # Find all sequences of printable characters (ASCII 32 through 126).
    printable_parts = extract_printable_sequences(chip_id)
    i = 0
    for part in printable_parts:
        print(i, part)
        i += 1
        
    #lcd.move_to(0, 2)
    #lcd.putstr("> "+printable_parts[1])  
    
    try:
        print("FW Bank: {}".format(ts.fw_bank))
    except Exception as e:
        print("Exception: {}".format(e))

    print("="*32)

    #print("RAW Certificate: {}".format(ts.certificate))
    raw_cert = ts.certificate
    truncated = raw_cert[:50]
    print("RAW Certificate: " +str(truncated) + "...")     
       
    
    print("Cert Public Key: {}".format(ts.public_key))

    print("Starting secure session...")
    print(ts.start_secure_session(pkey_index_0, bytes(sh0priv), bytes(sh0pub)))
    print()

    """
    Maximální hodnota je 4 bity na hex znak (tedy 128 bitů celkem pro 32 znaků). Pokud by náš řetězec měl entropii kolem 3,5 bitů na znak
    (tedy přibližně 112 bitů celkem), může to být ještě považováno za použitelné v některých aplikacích, i když ne ideální
    
    f60ebf74db7751e027dedd95e8426d05 32
    Shannonova entropie na znak: 3.527518 bitů
    Celková entropie: 112.8806 bitů
    
    b6bca325c4a7f442c635a4c7a875b2d8 32
    Shannonova entropie na znak: 3.468139 bitů
    Celková entropie: 110.9804 bitů
    
    5a12168e901fbb77383d74961a5ed5a8 32
    Shannonova entropie na znak: 3.780639 bitů
    Celková entropie: 120.9804 bitů
    """
    
    import math

    def shannon_entropy(s):
        freq = {}
        for c in s:
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
        entropy = 0.0
        length = float(len(s))
        for count in freq.values():
            p = count / length
            entropy -= p * math.log(p, 2)
        return entropy
    
    def entropy():
        rnd32 = ts.get_random(16) # 16*2=32
        print(rnd32.hex(), len(str(rnd32.hex())))        
                
        hex_str = rnd32.hex()
        ent_per_char = shannon_entropy(hex_str)
        total_entropy = ent_per_char * len(hex_str)
        print("Shannonova entropie na znak:", ent_per_char, "bitů")
        print("Celková entropie:", total_entropy, "bitů")   
        
        sleep(0.3)
        
    print("[ sign ]")
    try:
        resp = ts.ping(b"Hello Tropic Square From MicroPython!")
        print("Ping: {}".format(resp))
    except Exception as e:
        print("Exception: {}".format(e))    
    
    print("[ RND ]")
    for y in range(1,63):
        print(y)
        rnd32 = ts.get_random(8) # 16*2=32
        print(rnd32)
        print(y, rnd32.hex())        
        draw_line(oled,str(rnd32.hex()),y)     
    
    """
    757382dfd135dc17b3916961a3804e47
    8c269512ad25774d8f99a2ab3bf53c8d
    091f919c0f4c7443ad902b3da995c719
    e4003035d9c27d93d82b6fb928b7f518
    1de40e3889d2501a2fe275b96ddba9eb
    """
    try:
        resp = ts.ping(b"Hello Tropic Square From MicroPython!")
        print("Ping: {}".format(resp))
    except Exception as e:
        print("Exception: {}".format(e))

    print("Log")
    print(ts.get_log())

if __name__ == "__main__":
    main()

