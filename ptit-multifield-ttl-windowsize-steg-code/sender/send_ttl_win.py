from scapy.all import *
import time
import base64

chunks = ["UF", "RJ", "VA", "A="]

message = base64.b64decode(''.join(chunks)).decode()
def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_packets(bits):
    packets = []
    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i+1] if i+1 < len(bits) else '0'

        ttl = 100 if bit1 == '0' else 101

        win = 2048 if bit2 == '0' else 2049

        ip = IP(dst="172.20.0.11", ttl=ttl)
        tcp = TCP(sport=12345+i, dport=80, flags="PA", window=win)

        pkt = ip / tcp / Raw(load="GET / HTTP/1.1\r\nHost: example.com\r\n\r\n")
        packets.append(pkt)

        print(f"[{i//2}] Sending...")
    return packets

bits = text_to_bits(message)
print(f"[+] Sending message: '****'...")

packets = bits_to_packets(bits)
for pkt in packets:
    send(pkt, verbose=0)
    time.sleep(0.3)

print("[+] Done sending.")

