#!/usr/bin/env python3

def binary_to_text(binary_str):
    """Chuyển chuỗi binary thành text ASCII"""
    try:
        bytes_list = [binary_str[i:i+8] for i in range(0, len(binary_str), 8)]
        
        text = ''.join([chr(int(byte, 2)) for byte in bytes_list])
        return text
    except:
        return "Loi: Chuoi binary khong hop le!"

def main():
    print("=== CONG CU CHUYEN BIT THANH VAN BAN ===")
    print("Huong dan:")
    print("- Nhap chuoi bit tu cac goi tin giau tin (100=0, 101=1)")
    print("- Vi du: 010100110100010101000011010100100100010101010100")
    print("- Ket qua se hien thi thong diep duoc giai ma\n")
    
    while True:
        binary_input = input("Nhap chuoi bit (hoac 'q' đe thoat): ").strip()
        
        if binary_input.lower() == 'q':
            break
        
        if not all(c in '01' for c in binary_input):
            print("Loi: Chuoi chi duoc chua ky tu 0 va 1!")
            continue
        
        message = binary_to_text(binary_input)
        print(f"\nKet qua giai ma: {message}\n")

if __name__ == "__main__":
    main()

