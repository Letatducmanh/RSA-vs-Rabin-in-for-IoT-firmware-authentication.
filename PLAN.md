# KẾ HOẠCH TRIỂN KHAI THỰC NGHIỆM (CHƯƠNG 4)
**Đề tài:** Phân tích độ an toàn và hiệu năng của chữ ký số Rabin so với hệ mật RSA.
**Bài toán mô phỏng:** Xác thực bản cập nhật phần mềm (Firmware Update) cho thiết bị IoT.
**Công nghệ sử dụng:** Python (Backend - Lõi mật mã & API) + HTML/CSS/JS (Frontend - Biểu đồ).

---

## GIAI ĐOẠN 1: KHỞI TẠO DỰ ÁN VÀ KIẾN TRÚC (SETUP & ARCHITECTURE)
*Mục tiêu: Xây dựng cấu trúc thư mục chuẩn và cài đặt các thư viện cần thiết.*

- [ ] **1.1. Khởi tạo môi trường ảo (Virtual Environment)**
  - Chạy lệnh: `python -m venv venv`
  - Kích hoạt môi trường: `source venv/bin/activate` (Mac/Linux) hoặc `venv\Scripts\activate` (Windows).
- [ ] **1.2. Cài đặt các thư viện lõi**
  - Chạy lệnh: `pip install fastapi uvicorn gmpy2 cryptography`
  - *(Lưu ý: `fastapi` và `uvicorn` dùng làm Web Server, `gmpy2` để tính toán số lớn tối ưu, `cryptography` để dùng hàm băm SHA-256).*
- [ ] **1.3. Thiết lập cấu trúc thư mục dự án**
  ```text
  project_root/
  ├── backend/
  │   ├── core/
  │   │   ├── rsa_crypto.py      # Chứa Class thực thi RSA
  │   │   ├── rabin_crypto.py    # Chứa Class thực thi Rabin
  │   │   └── utils.py           # Các hàm phụ trợ (sinh số nguyên tố, hash)
  │   ├── simulation.py          # Kịch bản chạy giả lập 1000 gói tin
  │   └── main.py                # Khởi tạo FastAPI Server & Endpoints
  ├── frontend/
  │   ├── index.html             # Giao diện chính
  │   ├── style.css              # File CSS
  │   └── script.js              # Xử lý logic gọi API và vẽ biểu đồ
  ├── requirements.txt           # Lưu danh sách thư viện
  └── PLAN.md                    # File kế hoạch này


lệnh thực thi chạy : uvicorn main:app --reload