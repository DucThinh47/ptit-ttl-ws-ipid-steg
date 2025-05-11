from scapy.all import *
import time
import random

message = ""

def text_to_bits(text):
    return ''.join(format(ord(c), '08b') for c in text)

def build_steg_packets(bits):
    packets = []
    for i in range(0, len(bits), 2):
        bit1 = bits[i]
        bit2 = bits[i+1] if i+1 < len(bits) else '0'

        ttl = 100 if bit1 == '0' else 101
        win = 2048 if bit2 == '0' else 2049

        ip = IP(dst="172.20.0.11", ttl=ttl)
        tcp = TCP(sport=40000+i, dport=80, flags="PA", window=win)
        pkt = ip / tcp / Raw(load="GET / HTTP/1.1\r\nHost: steg.example.com\r\n\r\n")
        packets.append(pkt)
    return packets

def build_noise_packet(index):
    ttl = random.choice([110, 120, 128, 64])
    win = random.choice([3000, 5000, 6000, 4096])
    ip = IP(dst="172.20.0.11", ttl=ttl)
    tcp = TCP(sport=50000+index, dport=80, flags="PA", window=win)
    pkt = ip / tcp / Raw(load="GET /noise HTTP/1.1\r\nHost: noise.site\r\n\r\n")
    return pkt

def send_all():
    bits = text_to_bits(message)
    steg_pkts = build_steg_packets(bits)

    all_pkts = steg_pkts.copy()
    for i in range(14):
        all_pkts.insert(random.randint(0, len(all_pkts)), build_noise_packet(i))

    print(f"[+] Sending {len(all_pkts)} packets (including steg + noise)...")
    for idx, pkt in enumerate(all_pkts):
        send(pkt, verbose=0)
        print(f"Sent packet #{idx+1}")
        time.sleep(0.5)

send_all()
print("[+] Done.")

