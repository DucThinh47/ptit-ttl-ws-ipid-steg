from scapy.all import IP, UDP, send
import time
import random

def send_mixed_packets(dest_ip, message="HELLO"):
    """Gửi xen kẽ gói tin thường và gói tin giấu tin"""
    binary_msg = ''.join(format(ord(c), '08b') for c in message)
    print(f"Encoding message: {message} -> Binary: {binary_msg}")
    
    for i in range(len(binary_msg)*2):
        if i % 2 == 0:
            ttl = random.choice([64, 65, 127, 128])
            note = "NOISE"
        else:
            bit = binary_msg[i//2]
            ttl = 100 if bit == '0' else 101
            note = f"DATA (bit={bit})"
        
        pkt = IP(dst=dest_ip, ttl=ttl)/UDP(dport=5555, sport=4444)
        send(pkt, verbose=False)
        print(f"Sent packet {i+1}: TTL={ttl} ({note})")
        time.sleep(0.5)

if __name__ == "__main__":
    send_mixed_packets("192.168.2.11")
    print("Finished sending mixed packets")
