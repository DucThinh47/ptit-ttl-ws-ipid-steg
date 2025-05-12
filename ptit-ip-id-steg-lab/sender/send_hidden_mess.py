from scapy.all import *
import time
import sys

# Che giấu thông điệp bằng mã hóa Caesar đơn giản
def _hidden_encoder():
    encoded = [80, 84, 73, 84]  # 'PTIT' dạng ASCII decimal
    return ''.join(chr(c) for c in encoded)

def _calculate_checksum(msg):
    return sum(ord(c) for c in msg) & 0xFFFF

def _send_hidden_message(dst_ip, interval=0.5):
    hidden_msg = _hidden_encoder()  # Lấy thông điệp đã mã hóa
    
    # Mã hóa thành binary + checksum
    binary_str = ''.join(format(ord(c), '08b') for c in hidden_msg)
    binary_str += format(_calculate_checksum(hidden_msg), '016b')
    
    print("[+] Initiating network packet transmission...")
    print("[*] Sending crafted TCP packets to", dst_ip)
    
    for bit in binary_str:
        pkt = IP(dst=dst_ip, id=20000 if bit == '0' else 20001)/TCP(dport=80)
        send(pkt, verbose=False)
        time.sleep(interval)
    
    print("[+] Transmission sequence completed")
    print("[*] Total packets injected:", len(binary_str))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 send_stego.py <receiver_ip>")
        print("Example: python3 send_stego.py 192.168.1.100")
        sys.exit(1)

    _send_hidden_message(sys.argv[1])
