from login.util import encrypt_pwd



public_key='MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCRNPY55sDnwFARqVkDsuJ9m68KawFK2uWiGI783QtNAb+O3HViGFOG1JieNexIzoN8fCdhg802KDaUUYqzOlxA4i+gkocERxPvuW9LQJVP7DQAYx4hrydcLMZEMSXpBlbzFKiJ4vgtXfqWhZ8YohGhLk0eQnQNEyHRfs0y6FoCBwIDAQAB'

import random
from Crypto.Util.number import bytes_to_long, long_to_bytes


class RSA:
    def __init__(self, n, e):
        self.n = n
        self.e = e

    def encrypt(self, msg):
        def prepare_message(msg, length):
            if length < len(msg) + 11:
                print("Message too long for RSA")
                return None

            n = []
            t = len(msg) - 1
            while t >= 0 and length > 0:
                o = ord(msg[t])
                if o < 128:
                    n.append(o)
                elif o > 127 and o < 2048:
                    n.append(63 & o | 128)
                    n.append(o >> 6 | 192)
                else:
                    n.append(63 & o | 128)
                    n.append(o >> 6 & 63 | 128)
                    n.append(o >> 12 | 224)
                t -= 1

            n.append(0)
            i = 0
            h = []
            while length > 2:
                a = [0]
                while a[0] == 0:
                    a[0] = random.randint(0, 255)
                n.append(a[0])
                length -= 1

            n.append(2)
            n.append(0)
            return bytes(n)

        t = prepare_message(msg, (self.n.bit_length() + 7) // 8)
        if t is None:
            return None

        n = pow(bytes_to_long(t), self.e, self.n)
        r = hex(n)[2:]
        if len(r) & 1:
            r = '0' + r
        return r


# 示例用法
n = 1234567890  # 替换为实际的 RSA 公钥模数
e = 65537  # 替换为实际的 RSA 公钥指数

rsa = RSA(n, e)
message = "Hello, World!"
encrypted = rsa.encrypt(message)
print("Encrypted message:", encrypted)
