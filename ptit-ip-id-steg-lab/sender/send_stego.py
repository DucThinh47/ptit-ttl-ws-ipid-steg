from scapy.all import *
import time
import sys

def calculate_checksum(message):
    """Tính checksum 16-bit cho message"""
    return sum(ord(c) for c in message) & 0xFFFF

def encode_message(message):
    """Mã hóa message thành chuỗi bit với checksum"""
    binary_str = ''.join(format(ord(c), '08b') for c in message)
    checksum = calculate_checksum(message)
    binary_str += format(checksum, '016b')  # Thêm 16-bit checksum
    return binary_str

def send_stego_packets(message, dst_ip, interval=0.5):
    """Gửi các packet chứa tin nhấu giấu"""
    print(f"[+] Encoding message: '{message}'")
    binary_str = encode_message(message)
    print(f"[+] Binary representation with checksum: {binary_str}")
    
    print("\n[+] Sending packets:")
    for i, bit in enumerate(binary_str):
        # Tạo packet với ID chẵn/lẻ tương ứng bit 0/1
        pkt = IP(dst=dst_ip, id=20000 if bit == '0' else 20001)/TCP(dport=80)
        send(pkt, verbose=False)
        print(f"Packet {i+1}: ID={pkt.id} (bit={bit})")
        time.sleep(interval)
    
    print("\n[+] Message sent successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <receiver_ip> <message>")
        print("Example: python3 send_stego.py 192.168.1.2 SECRET")
        sys.exit(1)
    
    dst_ip = sys.argv[1]
    message = sys.argv[2]
    
    if len(message) > 6:
        print("[!] Warning: Message longer than 6 characters may not decode properly")
    
    send_stego_packets(message, dst_ip)
