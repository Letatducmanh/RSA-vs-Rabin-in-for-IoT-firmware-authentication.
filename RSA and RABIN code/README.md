# CryptoSim: Phân tích RSA vs Rabin cho xác thực firmware IoT

Đây là một dự án mô phỏng so sánh **chữ ký số RSA** và **chữ ký số Rabin** trong bài toán xác thực bản cập nhật phần mềm (Firmware Update) cho thiết bị IoT. Ứng dụng dùng **Python + FastAPI** cho backend và **HTML/CSS/JavaScript** cho frontend, hiển thị kết quả bằng biểu đồ và bảng thống kê.

## Mục tiêu dự án

- Mô phỏng quá trình ký số và xác thực của RSA và Rabin.
- Đo và so sánh thời gian ký, thời gian xác thực, độ ổn định và kích thước chữ ký.
- Minh họa trực quan bằng giao diện web để dễ trình bày trong báo cáo/thực nghiệm.

## Cấu trúc dự án

```text
code ck/
├── PLAN.md
├── requirements.txt
└── project_root/
    ├── main.py
    ├── simulation.py
    ├── core/
    │   ├── rsa_crypto.py
    │   ├── rabin_crypto.py
    │   └── utils.py
    └── static/
        ├── index.html
        ├── style.css
        └── script.js
```

### Vai trò các file chính

- `project_root/main.py`: Khởi tạo FastAPI, phục vụ giao diện tĩnh và cung cấp API chạy mô phỏng.
- `project_root/simulation.py`: Sinh gói tin giả lập và đo thời gian ký/xác thực cho RSA và Rabin.
- `project_root/core/rsa_crypto.py`: Cài đặt lớp chữ ký số RSA.
- `project_root/core/rabin_crypto.py`: Cài đặt lớp chữ ký số Rabin.
- `project_root/core/utils.py`: Các hàm hỗ trợ như sinh số nguyên tố và băm SHA-256.
- `project_root/static/index.html`: Giao diện web chính.
- `project_root/static/style.css`: Giao diện và hiệu ứng hiển thị.
- `project_root/static/script.js`: Gọi API backend và vẽ biểu đồ bằng Chart.js.

## Công nghệ sử dụng

- Python
- FastAPI
- Uvicorn
- gmpy2
- cryptography
- HTML / CSS / JavaScript
- Chart.js

## Cài đặt

Khuyến nghị dùng môi trường ảo Python trước khi cài đặt.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Cách chạy dự án

1. Mở terminal tại thư mục gốc của dự án.
2. Nếu chưa làm ở bước cài đặt, hãy kích hoạt môi trường ảo Python.
3. Di chuyển vào thư mục `project_root` và chạy backend:

```bash
uvicorn main:app --reload
```

4. Mở trình duyệt và truy cập:

```text
http://127.0.0.1:8000
```

## API chính

- `GET /`: Trả về giao diện web.
- `GET /api/run-simulation?num_packets=100&key_bits=2048`: Chạy mô phỏng so sánh RSA và Rabin.

### Tham số mô phỏng

- `num_packets`: Số lượng gói tin firmware giả lập.
- `key_bits`: Độ dài khóa, mặc định là `2048`.

## Luồng hoạt động

1. Frontend gửi yêu cầu chạy mô phỏng tới backend.
2. Backend tạo khóa RSA và Rabin theo độ dài bit đã chọn.
3. Hệ thống sinh các gói tin ngẫu nhiên đại diện cho firmware.
4. Đo thời gian ký và xác thực của từng thuật toán.
5. Trả kết quả về frontend để vẽ biểu đồ và cập nhật bảng so sánh.

## Lưu ý

- Ứng dụng hiện phục vụ giao diện trực tiếp từ backend FastAPI, nên chỉ cần chạy một lệnh `uvicorn` là đủ.
- Dự án tập trung vào mục đích mô phỏng và so sánh hiệu năng, không phải một hệ thống chữ ký số triển khai sản xuất.
