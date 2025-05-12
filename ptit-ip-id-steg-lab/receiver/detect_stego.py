from scapy.all import *
import sys

def verify_checksum(binary_str):
    """Xác thực checksum từ chuỗi bit"""
    if len(binary_str) < 16:
        return False, ""
    
    data_bits = binary_str[:-16]
    received_checksum = int(binary_str[-16:], 2)
    
    # Tính checksum từ data
    calculated_checksum = 0
    message = ""
    for i in range(0, len(data_bits), 8):
        if i+8 > len(data_bits):
            break
        byte = data_bits[i:i+8]
        char = chr(int(byte, 2))
        calculated_checksum += ord(char)
        message += char
    
    calculated_checksum &= 0xFFFF  # Giới hạn 16-bit
    
    return calculated_checksum == received_checksum, message

def analyze_packets(pcap_file):
    """Phân tích packet và giải mã message"""
    try:
        packets = rdpcap(pcap_file)
    except:
        print(f"[!] Error: Could not read pcap file {pcap_file}")
        return
    
    # Lọc các packet nghi ngờ (ID 20000 hoặc 20001)
    stego_packets = [pkt for pkt in packets if IP in pkt and pkt[IP].id in [20000, 20001]]
    
    if not stego_packets:
        print("[!] No stego packets found (IP ID 20000 or 20001)")
        return
    
    print(f"\n[+] Found {len(stego_packets)} potential stego packets")
    
    # Giải mã các bit
    binary_str = ''.join('0' if pkt[IP].id == 20000 else '1' for pkt in stego_packets)
    
    print(f"[+] Extracted binary: {binary_str}")
    
    # Xác thực checksum
    is_valid, message = verify_checksum(binary_str)
    
    if is_valid:
        print("\n[+] Message successfully decoded!")
        print(f"[+] Checksum verified")
        print(f"[+] Hidden message: '{message}'")
    else:
        print("\n[!] Checksum verification failed")
        print("[!] Possible reasons:")
        print(" - Missing/corrupted packets")
        print(" - Incorrect decoding")
        print(f"[!] Raw message (unverified): '{message[:6]}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <pcap_file>")
        print("Example: python3 detect_stego.py capture.pcap")
        sys.exit(1)
    
    pcap_file = sys.argv[1]
    analyze_packets(pcap_file)
