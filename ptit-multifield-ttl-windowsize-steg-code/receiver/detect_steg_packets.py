from scapy.all import *
import sys

if sys.version_info[0] < 3:
    print("[!] Please run this script with Python 3.")
    sys.exit(1)

print("[*] Listening for TCP packets to port 80...")

observed = 0

def is_steg_packet(pkt):
    if IP in pkt and TCP in pkt:
        ttl = pkt[IP].ttl
        win = pkt[TCP].window
        return ttl in [100, 101] and win in [2048, 2049]
    return False

def process(pkt):
    global observed
    observed += 1
    if IP in pkt and TCP in pkt:
        ttl = pkt[IP].ttl
        win = pkt[TCP].window
        if is_steg_packet(pkt):
            print(f"[+] Packet #{observed} (TTL={ttl}, Win={win})")
        else:
            print(f"[-] Packet #{observed} (TTL={ttl}, Win={win})")

sniff(filter="tcp and dst port 80", prn=process, timeout=60)

print(f"\n[+] Total packets received: {observed}")
print("[+] Done. Please manually record steg packet numbers.")

