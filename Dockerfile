# 1. Chọn hệ điều hành và phiên bản Python có sẵn
FROM python:3.10-slim

# 2. Cài đặt các thư viện lõi của hệ thống (bắt buộc phải có để chạy gmpy2)
RUN apt-get update && apt-get install -y \
    gcc \
    libgmp-dev \
    libmpfr-dev \
    libmpc-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Tạo một thư mục tên là /app trên server của Render để chứa code
WORKDIR /app

# 4. Copy file requirements.txt từ máy bạn lên server
COPY requirements.txt .

# 5. Cài đặt các thư viện Python (FastAPI, gmpy2, cryptography...)
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy toàn bộ các file/thư mục còn lại của dự án vào server
COPY . .

# 7. Lệnh cuối cùng để khởi động server FastAPI khi mọi thứ đã cài xong
CMD ["uvicorn", "project_root.main:app", "--host", "0.0.0.0", "--port", "10000"]