def bits_to_text_with_checksum(bits):
    if len(bits) < 16:
        return "Khong du bit de kiem tra checksum"
    
    # Tách message (32 bit đầu) và checksum (16 bit cuối)
    message_bits = bits[:-16]
    checksum = int(bits[-16:], 2)
    
    # Giải mã message
    message = ''.join(chr(int(message_bits[i:i+8], 2)) for i in range(0, len(message_bits), 8))
    
    # Kiểm tra checksum
    calc_checksum = sum(ord(c) for c in message) & 0xFFFF
    if calc_checksum == checksum:
        return f"Thong diep giai ma: '{message}'"
    else:
        return f"Checksum khong khop! Giai ma duoc: '{message}' (Checksum thuc te: {calc_checksum}, Nhan duoc: {checksum})"

student_bits = input("Nhap chuoi bit tim duoc (included checksum): ").strip()
print(bits_to_text_with_checksum(student_bits))
