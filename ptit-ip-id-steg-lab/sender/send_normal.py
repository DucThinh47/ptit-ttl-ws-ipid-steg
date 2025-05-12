from scapy.all import *
import random
import time

def send_normal_traffic():
    for i in range(20):
        # Gửi packet ngẫu nhiên
        pkt = IP(dst="175.30.0.11", id=random.randint(1000, 20000), ttl=64)/TCP(dport=80)
        send(pkt, verbose=0)
        time.sleep(0.5)

send_normal_traffic()
