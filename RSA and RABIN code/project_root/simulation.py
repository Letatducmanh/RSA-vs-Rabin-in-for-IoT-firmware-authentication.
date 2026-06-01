import time
import random
import string
from core.rsa_crypto import RSASignature
from core.rabin_crypto import RabinSignature

def generate_mock_firmware_packets(num_packets=1000, packet_size=256):
    """Sinh ra mảng chứa các chuỗi dữ liệu ngẫu nhiên đại diện cho các gói tin Firmware."""
    packets = []
    for _ in range(num_packets):
        # Tạo chuỗi ngẫu nhiên gồm chữ và số
        packet = ''.join(random.choices(string.ascii_letters + string.digits, k=packet_size))
        packets.append(packet)
    return packets

def run_simulation(num_packets=1000, key_bits=2048):
    """
    Kịch bản chạy mô phỏng đo lường:
    1. Máy chủ (Server) thực hiện Ký số.
    2. Thiết bị IoT thực hiện Xác thực.
    """
    print(f"[*] Đang khởi tạo khóa {key_bits}-bit cho RSA và Rabin (Sẽ mất vài giây)...")
    rsa = RSASignature(bits=key_bits)
    rabin = RabinSignature(bits=key_bits)
    
    print(f"[*] Đang sinh {num_packets} gói tin cập nhật Firmware...")
    packets = generate_mock_firmware_packets(num_packets)
    
    # ---------------------------------------------------------
    # GIAI ĐOẠN 1: MÁY CHỦ KÝ SỐ (SERVER SIDE)
    # Đo lường thời gian Ký từng gói tin để vẽ biểu đồ Line Chart
    # ---------------------------------------------------------
    rsa_sign_times = []
    rsa_signatures = []
    
    rabin_sign_times = []
    rabin_signatures = []
    
    print("[*] Máy chủ đang tiến hành ký số (RSA)...")
    for msg in packets:
        start_time = time.perf_counter_ns()
        sig = rsa.sign(msg)
        end_time = time.perf_counter_ns()
        
        # Chuyển đổi từ nano-giây sang mili-giây và lưu lại
        rsa_sign_times.append((end_time - start_time) / 1_000_000)
        rsa_signatures.append(sig)

    print("[*] Máy chủ đang tiến hành ký số (Rabin)...")
    for msg in packets:
        start_time = time.perf_counter_ns()
        sig, salt = rabin.sign(msg)
        end_time = time.perf_counter_ns()
        
        rabin_sign_times.append((end_time - start_time) / 1_000_000)
        rabin_signatures.append((sig, salt))

    # ---------------------------------------------------------
    # GIAI ĐOẠN 2: THIẾT BỊ IOT XÁC THỰC (EDGE/CLIENT SIDE)
    # Đo lường tổng thời gian và tính trung bình để vẽ Bar Chart
    # ---------------------------------------------------------
    print("[*] Thiết bị IoT đang xác thực chữ ký (RSA)...")
    start_rsa_verify = time.perf_counter_ns()
    for i in range(num_packets):
        is_valid = rsa.verify(rsa_signatures[i], packets[i])
        assert is_valid == True, "Lỗi: Xác thực RSA thất bại!"
    end_rsa_verify = time.perf_counter_ns()
    rsa_verify_total_ms = (end_rsa_verify - start_rsa_verify) / 1_000_000

    print("[*] Thiết bị IoT đang xác thực chữ ký (Rabin)...")
    start_rabin_verify = time.perf_counter_ns()
    for i in range(num_packets):
        sig, salt = rabin_signatures[i]
        is_valid = rabin.verify(sig, packets[i], salt)
        assert is_valid == True, "Lỗi: Xác thực Rabin thất bại!"
    end_rabin_verify = time.perf_counter_ns()
    rabin_verify_total_ms = (end_rabin_verify - start_rabin_verify) / 1_000_000

    # ---------------------------------------------------------
    # ĐÓNG GÓI KẾT QUẢ VÀO DICTIONARY
    # ---------------------------------------------------------
    results = {
        "simulation_info": {
            "num_packets": num_packets,
            "key_bits": key_bits
        },
        "signing_metrics": {
            "rsa_times_ms": rsa_sign_times,
            "rabin_times_ms": rabin_sign_times,
            "rsa_avg_ms": sum(rsa_sign_times) / num_packets,
            "rabin_avg_ms": sum(rabin_sign_times) / num_packets
        },
        "verification_metrics": {
            "rsa_total_ms": rsa_verify_total_ms,
            "rabin_total_ms": rabin_verify_total_ms,
            "rsa_avg_ms": rsa_verify_total_ms / num_packets,
            "rabin_avg_ms": rabin_verify_total_ms / num_packets
        }
    }
    
    # Tính toán kích thước thực tế của chữ ký bằng Byte
    # Ép kiểu int() để gmpy2 có thể đếm được số bit
    rsa_size_bytes = (int(rsa.n).bit_length() + 7) // 8
    
    # Kích thước Rabin = Kích thước chữ ký + kích thước của tham số Salt ngẫu nhiên
    rabin_sig_size = (int(rabin.n).bit_length() + 7) // 8
    first_salt = rabin_signatures[0][1]
    salt_bytes = (int(first_salt).bit_length() + 7) // 8 if first_salt > 0 else 1
    rabin_total_bytes = rabin_sig_size + salt_bytes

    # ---------------------------------------------------------
    # ĐÓNG GÓI KẾT QUẢ VÀO DICTIONARY
    # ---------------------------------------------------------
    results = {
        "simulation_info": {
            "num_packets": num_packets,
            "key_bits": key_bits
        },
        "signing_metrics": {
            "rsa_times_ms": rsa_sign_times,
            "rabin_times_ms": rabin_sign_times,
            "rsa_avg_ms": sum(rsa_sign_times) / num_packets,
            "rabin_avg_ms": sum(rabin_sign_times) / num_packets
        },
        "verification_metrics": {
            "rsa_total_ms": rsa_verify_total_ms,
            "rabin_total_ms": rabin_verify_total_ms,
            "rsa_avg_ms": rsa_verify_total_ms / num_packets,
            "rabin_avg_ms": rabin_verify_total_ms / num_packets
        },
        # THÊM KHỐI DỮ LIỆU ĐO KÍCH THƯỚC NÀY
        "storage_metrics": {
            "rsa_bytes": rsa_size_bytes,
            "rabin_bytes": rabin_total_bytes,
            "salt_bytes": salt_bytes
        }
    }
    
    print("[*] Hoàn tất mô phỏng!")
    return results

# Cú pháp này giúp bạn có thể chạy thử trực tiếp file này trên terminal để test code
if __name__ == "__main__":
    test_results = run_simulation(num_packets=100) # Chạy thử 100 gói tin cho nhanh
    print(f"Tổng thời gian IoT xác thực RSA: {test_results['verification_metrics']['rsa_total_ms']:.2f} ms")
    print(f"Tổng thời gian IoT xác thực Rabin: {test_results['verification_metrics']['rabin_total_ms']:.2f} ms")