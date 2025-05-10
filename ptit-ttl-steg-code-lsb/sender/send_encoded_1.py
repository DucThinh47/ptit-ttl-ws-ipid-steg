from scapy.all import IP, UDP, send
import time

message = 'B21DCAT181'
binary = ''.join(format(ord(c), '08b') for c in message)
dest_ip = '192.168.2.11'

print(f"[+] Sending binary for message '{message}': {binary}")
for bit in binary:
    ttl = 100 if bit == '0' else 101
    pkt = IP(dst=dest_ip, ttl=ttl)/UDP(dport=5555, sport=4444)
    send(pkt, verbose=False)
    print(f"    Sent packet with TTL={ttl} (bit={bit})")
    time.sleep(0.5)

