import gmpy2
from core.utils import generate_blum_prime, hash_message

class RabinSignature:
    def __init__(self, bits=2048):
        """Khởi tạo cặp khóa Rabin (Bắt buộc dùng Blum primes)"""
        prime_bits = bits // 2
        self.p = generate_blum_prime(prime_bits)
        self.q = generate_blum_prime(prime_bits)
        self.n = self.p * self.q
        
        # Tính toán trước các nghịch đảo cho thuật toán CRT (Garner's formula)
        self.q_inv = gmpy2.invert(self.q, self.p)
        self.p_inv = gmpy2.invert(self.p, self.q)

    def sign(self, message):
        """Ký số Rabin bằng cách rút căn bậc 2 kết hợp CRT"""
        salt = 0
        h = 0
        
        # VÒNG LẶP RANDOMIZED PADDING (Giải quyết rào cản 25%)
        while True:
            h = hash_message(message, salt)
            # Kiểm tra Thặng dư bậc 2 bằng ký hiệu Legendre (Jacobi trong gmpy2)
            if gmpy2.jacobi(h, self.p) == 1 and gmpy2.jacobi(h, self.q) == 1:
                break
            salt += 1 # Thay đổi salt nếu không phải thặng dư
            
        # 1. Rút căn trên từng module nguyên tố
        s_p = gmpy2.powmod(h, (self.p + 1) // 4, self.p)
        s_q = gmpy2.powmod(h, (self.q + 1) // 4, self.q)
        
        # 2. Áp dụng CRT để tổng hợp nghiệm modulo n
        # Ta chỉ cần tính ra 1 trong 4 nghiệm để làm chữ ký (Nghiệm 1)
        root1 = (s_p * self.q * self.q_inv + s_q * self.p * self.p_inv) % self.n
        
        signature = root1 
        
        # Trả về cả chữ ký và salt để thiết bị nhận có thể băm lại đúng chuỗi
        return signature, salt

    def verify(self, signature, message, salt):
        """Xác thực Rabin siêu nhẹ: m' = s^2 (mod n)"""
        expected_hash = hash_message(message, salt)
        # Chỉ duy nhất 1 phép bình phương!
        m_prime = gmpy2.powmod(signature, 2, self.n)
        return m_prime == expected_hash