from scapy.all import sniff
import argparse

bits = []

# ======= PARSE ARGS =======
parser = argparse.ArgumentParser(description="Stegano UDP TTL Receiver")
parser.add_argument('--chars', type=int, required=True, help='So ky tu can thu (moi ky tu = 8 bit)')
args = parser.parse_args()
bit_target = args.chars * 8

# ======= PACKET PROCESSING =======
def process_packet(packet):
    if packet.haslayer('IP') and packet.haslayer('UDP'):
        src = packet['IP'].src
        ttl = packet['IP'].ttl
        lsb = ttl & 1
        bits.append(str(lsb))
        print(f"From {src} → TTL={ttl}, LSB={lsb}, Bits={''.join(bits)}")

print(f"[*] Listening for {bit_target} bits ({args.chars} characters)...")
sniff(filter="udp and port 5555", prn=process_packet, count=bit_target, store=0)

print(f"\n[+] All bits received: {''.join(bits)}")

# ======= DECODE MESSAGE =======
message = ''
for i in range(0, bit_target, 8):
    byte = ''.join(bits[i:i+8])
    char = chr(int(byte, 2))
    message += char
print(f"[+] Decoded Message: {message}")

