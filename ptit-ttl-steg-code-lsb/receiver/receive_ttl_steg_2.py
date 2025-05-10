from scapy.all import sniff
import datetime

def packet_handler(packet):
    """Xử lý và ghi thông tin gói tin vào file log"""
    if packet.haslayer('IP') and packet.haslayer('UDP'):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")
        src_ip = packet['IP'].src
        ttl = packet['IP'].ttl
        length = len(packet)
        
        # Ghi vào file log
        with open("packet_log.txt", "a") as f:
            f.write(f"{timestamp} - SRC: {src_ip} - TTL: {ttl} - Length: {length}\n")

if __name__ == "__main__":
    print("Starting packet capture...")
    print("All packets will be logged to packet_log.txt")
    print("Press Ctrl+C to stop...")
    
    # Xóa file log cũ nếu tồn tại
    open("packet_log.txt", "w").close()
    
    # Bắt gói tin và ghi log
    sniff(filter="udp and port 5555", prn=packet_handler, store=0)

