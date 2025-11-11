# Lab: Giấu tin trong mạng sử dụng kỹ thuật kết hợp nhiều trường và kỹ thuật mã hóa
## Lý thuyết
**1. Lý thuyết "Kênh ẩn Đa trường" (Multi-field Covert Channel)**

Đây là nguyên tắc quan trọng nhất của bài lab này. Thay vì chỉ sử dụng một trường (như IP ID) hoặc luân phiên các trường (như LSB TTL), kỹ thuật này sử dụng đồng thời nhiều trường trong cùng một gói tin để giấu tin.
- `Nguyên tắc`: Mỗi gói tin được gửi đi (`send_combined_steg.py`) được thiết kế để mang thông tin ẩn trong cả ba trường: `TTL`, `IP ID`, và `Window Size`.
- Hệ quả (Tăng Băng thông): Đây là điểm mấu chốt.
    - Các bài lab trước (chỉ dùng IP ID hoặc chỉ dùng TTL) chỉ mang được 1 bit thông tin cho mỗi gói tin ẩn.
    - Bài lab này, mỗi gói tin ẩn hợp lệ mang được 3 bit thông tin (TTL -> IP ID -> Window Size).
    - Điều này làm cho kênh ẩn có băng thông cao hơn gấp 3 lần, cho phép gửi thông điệp ("PTIT") nhanh hơn và với ít gói tin hơn.

**2. Nguyên tắc "Ghép kênh Kỹ thuật Mã hóa" (Multiplexing Encoding Techniques)**

Bài lab này cũng cho thấy rằng các phương pháp mã hóa khác nhau có thể được "ghép" (multiplexed) lại với nhau trong cùng một giao thức ẩn, tùy thuộc vào đặc điểm của từng trường.
- `Mã hóa LSB (Bit cuối)`: Được sử dụng cho các trường có giá trị linh hoạt tự nhiên.
    - `TTL`: {100, 101} (LSB là 0 hoặc 1).
    - `Window Size`: {2048, 2049} (LSB là 0 hoặc 1).
- `Mã hóa Chẵn-Lẻ (Parity)`: Được sử dụng cho trường IP ID để tạo một chữ ký cụ thể.
    - `IP ID`: {20000, 20001} (Chẵn là 0, Lẻ là 1).

Nguyên tắc này cho thấy sự linh hoạt trong việc thiết kế kênh ẩn: chọn kỹ thuật mã hóa phù hợp nhất cho từng trường để tối ưu hóa khả năng lẩn trốn.

**3. Lý thuyết "Giao thức Kênh ẩn" (Covert Protocol) và Thứ tự Bit**

Bài lab này định nghĩa một "giao thức" (protocol) rất rõ ràng cho kênh ẩn.
- `Quy tắc Lọc (Chữ ký)`: Một gói tin chỉ được coi là "hợp lệ" (mang tin ẩn) nếu nó tuân thủ cả ba điều kiện cùng lúc `(TTL ∈ {100, 101} VÀ IP ID ∈ {20000, 20001} VÀ WS ∈ {2048, 2049})`. Bất kỳ gói tin nào khác đều bị coi là nhiễu.
- `Quy tắc Trật tự (Bit Order)`: Thông điệp được giải mã bằng cách trích xuất các bit theo một thứ tự nghiêm ngặt đã được thống nhất trước: Bit từ TTL -> Bit từ IP ID -> Bit từ Window Size.
    - Ví dụ của bài lab (1 1 0) xác nhận điều này: TTL=101 (bit 1), IP ID=20001 (bit 1), WS=2048 (bit 0).

Điều này nhấn mạnh rằng cả hai bên (sender và receiver) phải đồng bộ tuyệt đối về các quy tắc này để kênh ẩn hoạt động.

**4. Phát hiện dựa trên "Chữ ký Phức hợp" (Complex Signature)**

Một hệ quả thú vị của kỹ thuật này là nó vừa khó hơn và vừa dễ hơn để phát hiện.
- `Khó hơn (với công cụ đơn giản)`: Một công cụ chỉ tìm kiếm sự bất thường ở một trường (ví dụ: chỉ theo dõi LSB của TTL) có thể bỏ sót, vì nó phải tìm kiếm sự kết hợp.
- `Dễ hơn (với công cụ nâng cao)`: Việc một gói tin có đồng thời cả 3 trường đều nằm trong các tập giá trị "bất thường" (TTL cố định, IP ID cố định, WS cố định) tạo ra một chữ ký (signature) cực kỳ cụ thể và hiếm gặp. Một bộ lọc Wireshark hoặc một quy tắc IDS (Hệ thống phát hiện xâm nhập) được viết để tìm chính xác sự kết hợp này sẽ có tỷ lệ báo động giả (false positive) cực thấp.
## Thực hành
Trên máy monitor, khởi động Wireshark:
    
    wireshark &

![img](0)

Từ máy sender, kiểm tra kết nối tới máy receiver:

    ping 192.168.50.10

![img](1)

Kiểm tra trên Wireshark xem có bắt được gói tin ICMP không:

![img](2)

Trên máy sender, thực thi file send_combined_steg.py để gửi thông điệp “PTIT”:

    sudo python3 send_combiend_steg.py “PTIT”

![img](3)

Trên Wireshark, dừng bắt gói tin, quan sát lưu lượng mạng. 

Với kỹ thuật giấu tin kết hợp TTL + Window Size + IP ID, sinh viên cần biết cách sử dụng Wireshark để lọc ra các gói tin có khả năng chứa thông điệp, từ đó xác định chuỗi bit đúng. Chỉ lọc và phân tích các gói tin mà:
- TTL ∈ {100, 101}
- Window Size ∈ {2048, 2049}
- IP ID ∈ {20000, 20001}

Cách xác định và ghi lại chuỗi bit. Mỗi gói hợp lệ mang 3 bit theo thứ tự:
- TTL → IP ID → Window Size
- Ghi lại chuỗi bit từng gói
- Ví dụ:
    - TTL = 101 → LSB = 1
    - IP ID = 20001 → lẻ → 1
    - Window Size = 2048 → LSB = 0

-> Gói này mang 3 bit: 1 1 0

![img](4)

Sau khi quan sát và phân tích, tìm được các gói có chứa thông điệp, tiến hành lưu lưu lượng mạng thành file monitor_capture.pcap:

![img](5)

Kiểm tra trên máy monitor xem đã lưu file thành công chưa:

![img](6)

Tiếp theo thực hiện chuyển file monitor_capture.pcap từ máy monitor sang máy receiver.
Trên máy receiver: 

    nc -l -p 8888 > monitor_capture.pcap

![img](7)

Trên máy monitor:

![img](8)

Trên máy receiver, Ctrl+C để dừng netcat. Kiểm tra xem nhận được file chưa:

![img](9)

Trên máy receiver, thực thi script detect_combined_steg.py:

    sudo python3 detect_combined_steg.py monitor_capture.pcap

![img](10)

Từ logs thu được sau khi thực thi script detect_combined_steg.py trên máy receiver, phân tích, tìm ra đâu là gói tin thật, đâu là gói tin chứa thông điệp.
Ghi lại số lượng gói tin có chứa thông điệp vào file answer.txt trên máy monitor:

    nano answer.txt

![img](11)

Từ việc phân tích, tiến hành ghi lại giá trị bits đại diện cho thông điệp “PTIT”.
Thực thi script decode_bits.py trên máy monitor để xác nhận chuỗi bit tìm được là đúng:

    python3 decode_bits.py

![img](12)

Sau khi đã tìm ra được chuỗi bit đúng, ghi kết quả vào file answer.txt trên máy monitor. Lưu file answer.txt.




