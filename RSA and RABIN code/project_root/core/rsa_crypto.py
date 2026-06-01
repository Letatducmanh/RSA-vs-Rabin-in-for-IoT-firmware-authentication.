import gmpy2
from core.utils import generate_prime, hash_message

class RSASignature:
    def __init__(self, bits=2048):
        """Khởi tạo cặp khóa RSA"""
        prime_bits = bits // 2
        self.p = generate_prime(prime_bits)
        self.q = generate_prime(prime_bits)
        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        
        # Số mũ công khai tiêu chuẩn
        self.e = gmpy2.mpz(65537)
        # Số mũ bí mật (Nghịch đảo modulo)
        self.d = gmpy2.invert(self.e, self.phi)

    def sign(self, message):
        """Ký số: s = m^d (mod n)"""
        m_hash = hash_message(message)
        # Hàm powmod của gmpy2 tối ưu hóa tính toán số lớn cực tốt
        signature = gmpy2.powmod(m_hash, self.d, self.n)
        return signature

    def verify(self, signature, message):
        """Xác thực: m' = s^e (mod n)"""
        expected_hash = hash_message(message)
        m_prime = gmpy2.powmod(signature, self.e, self.n)
        return m_prime == expected_hash