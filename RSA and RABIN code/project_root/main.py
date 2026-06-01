import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# =====================================================================
# BƯỚC ĐIỀU CHỈNH ĐƯỜNG DẪN (QUAN TRỌNG CHO DEPLOY)
# =====================================================================

# 1. Tự động lấy đường dẫn tuyệt đối của thư mục chứa file main.py này (project_root)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 2. Thêm thư mục project_root vào hệ thống tìm kiếm của Python để tránh lỗi ModuleNotFoundError
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# 3. Xác định chính xác đường dẫn tuyệt đối đến thư mục static
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Bây giờ có thể import an toàn từ các file cùng cấp hoặc thư mục core
from simulation import run_simulation

# =====================================================================
# KHỞI TẠO ỨNG DỤNG FASTAPI
# =====================================================================

app = FastAPI(title="Rabin vs RSA API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Nạp thư mục 'static' bằng đường dẫn tuyệt đối để phục vụ các file CSS, JS
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# KHI TRUY CẬP TRANG CHỦ (/), SẼ HIỂN THỊ GIAO DIỆN HTML QUA ĐƯỜNG DẪN TUYỆT ĐỐI
@app.get("/")
def serve_frontend():
    html_path = os.path.join(STATIC_DIR, "index.html")
    return FileResponse(html_path)

# Cập nhật thêm tham số key_bits, mặc định là 2048
@app.get("/api/run-simulation")
def api_run_simulation(num_packets: int = 100, key_bits: int = 2048):
    print(f"\n[API] Nhận yêu cầu chạy: {num_packets} gói tin | Khóa {key_bits}-bit...")
    # Truyền cả 2 tham số xuống lõi mô phỏng
    results = run_simulation(num_packets=num_packets, key_bits=key_bits)
    return results