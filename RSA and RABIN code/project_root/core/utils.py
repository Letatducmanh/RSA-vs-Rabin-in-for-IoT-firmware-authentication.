import os
import hashlib
import gmpy2

def generate_prime(bits):
    """Sinh một số nguyên tố ngẫu nhiên có độ dài bit chỉ định."""
    # Khởi tạo trạng thái ngẫu nhiên từ hệ điều hành
    rand_state = gmpy2.random_state(int.from_bytes(os.urandom(8), 'big'))
    # Sinh một số ngẫu nhiên làm điểm bắt đầu
    start = gmpy2.mpz(2)**(bits-1) + gmpy2.mpz_urandomb(rand_state, bits-1)
    # Tìm số nguyên tố tiếp theo từ điểm bắt đầu
    return gmpy2.next_prime(start)

def generate_blum_prime(bits):
    """Sinh số nguyên tố Blum thỏa mãn p ≡ 3 (mod 4)."""
    while True:
        p = generate_prime(bits)
        if p % 4 == 3:
            return p

def hash_message(message, salt=b""):
    """Băm thông điệp thành một số nguyên lớn bằng SHA-256."""
    if isinstance(message, str):
        message = message.encode('utf-8')
    if isinstance(salt, int):
        salt = str(salt).encode('utf-8')
        
    digest = hashlib.sha256(message + salt).digest()
    # Chuyển chuỗi byte băm thành số nguyên mpz của gmpy2
    return gmpy2.mpz(int.from_bytes(digest, byteorder='big'))