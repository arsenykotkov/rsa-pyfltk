import os
import re
from datetime import datetime
from random import randrange, getrandbits


def is_prime(n, k=128):
    """ Test if a number is prime
        Args:
            n -- int -- the number to test
            k -- int -- the number of tests to do
        return True if n is prime
    """
    # Test if n is not even.
    # But care, 2 is prime !
    if n == 2 or n == 3:
        return True
    if n <= 1 or n % 2 == 0:
        return False
    # find r and s
    s = 0
    r = n - 1
    while r & 1 == 0:
        s += 1
        r //= 2
    # do k tests
    for _ in range(k):
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            j = 1
            while j < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                j += 1
            if x != n - 1:
                return False
    return True


def generate_prime_candidate(length):
    """ Generate an odd integer randomly
        Args:
            length -- int -- the length of the number to generate, in bits
        return a integer
    """
    # generate random bits
    p = getrandbits(length)
    # apply a mask to set MSB and LSB to 1
    p |= (1 << length - 1) | 1
    return p


def generate_prime_number(length=512):
    """ Generate a prime
        Args:
            length -- int -- length of the prime to generate, in bits
        return a prime
    """
    p = 4
    # keep generating while the primality test fail
    while not is_prime(p, 128):
        p = generate_prime_candidate(length)
    return p


# function for extended Euclidean Algorithm
def gcdExtended(a, b):
    # Base Case
    if a == 0:
        return b, 0, 1

    gcd, x1, y1 = gcdExtended(b % a, a)

    # Update x and y using results of recursive
    # call
    x = y1 - (b // a) * x1
    y = x1

    return gcd, x, y


# open_exps = [3, 5, 17, 257, 65537]


def key_name_from_datetime():
    return re.sub("[-\s:.]", "", str(datetime.now()))


def gen_keys(bit_length, open_exponent, path):
    bit_length = bit_length
    e = open_exponent
    m = 0
    d = -1
    n = 0
    while True:
        p, q = generate_prime_number(bit_length), generate_prime_number(bit_length)
        n = p * q
        phi = (p - 1) * (q - 1)
        m, a, b = gcdExtended(phi, e)
        if m == 1 and b > 0:
            break

    # Export keys
    with open('{}_public.txt'.format(path), 'w', encoding='utf-8') as public:
        public.write('RSAPublicKey ::= SEQUENCE {\n')
        public.write('             modulus            {},   -- n\n'.format(n))
        public.write('             publicExponent     {},   -- e\n'.format(e))
        public.write('         }')
    with open('{}_private.txt'.format(path), 'w', encoding='utf-8') as private:
        private.write('RSAPrivateKey ::= SEQUENCE {\n')
        private.write('             modulus            {},   -- n\n'.format(n))
        private.write('             publicExponent     {},   -- e\n'.format(e))
        private.write('             privateExponent    {},   -- d\n'.format(b))
        private.write('             prime1             {},   -- p\n'.format(p))
        private.write('             prime2             {},   -- q\n'.format(q))
        private.write('         }')
    print('Ключи сгенерированы.')


def encrypt(filename, public_key):
    with open(filename, 'r', encoding='utf-8') as file:
        message = file.read()
    with open(public_key, 'r', encoding='utf-8') as file:
        public_key = file.read()
    n = int(re.findall('.*-- n$', public_key, re.MULTILINE)[0].split()[1].rstrip(','))
    e = int(re.findall('.*-- e$', public_key, re.MULTILINE)[0].split()[1].rstrip(','))
    padding = len(str(n))
    encryptedContent = ''.join([str(pow(ord(char), e, n)).zfill(padding) for char in message])
    with open(filename + '.encrypted', 'w', encoding='utf-8') as encrypted:
        encrypted.write('EncryptedData :: = SEQUENCE {\n')
        encrypted.write('             contentType                               text\n')
        encrypted.write('             contentEncryptionAlgorithmIdentifier      rsaEncryption\n')
        encrypted.write('             encryptedContent                          {}\n'.format(encryptedContent))
        encrypted.write('         }')
    print('Файл зашифрован.')


def decrypt(filename, secret_key):
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    with open(secret_key, 'r', encoding='utf-8') as file:
        secret_key = file.read()
    n = int(re.findall('.*-- n$', secret_key, re.MULTILINE)[0].split()[1].rstrip(','))
    e = int(re.findall('.*-- e$', secret_key, re.MULTILINE)[0].split()[1].rstrip(','))
    d = int(re.findall('.*-- d$', secret_key, re.MULTILINE)[0].split()[1].rstrip(','))
    p = int(re.findall('.*-- p$', secret_key, re.MULTILINE)[0].split()[1].rstrip(','))
    q = int(re.findall('.*-- q$', secret_key, re.MULTILINE)[0].split()[1].rstrip(','))
    encryptedContent = re.findall('.*encryptedContent.*', content, re.MULTILINE)[0].split()[1]
    encryptedContent = re.findall('.{' + str(len(str(n))) + '}', encryptedContent)
    with open(re.sub('\.encrypted', '', filename) + '.decrypted', 'w', encoding='utf-8') as decrypted:
        decrypted.write(''.join([chr(pow(int(char), d, n)) for char in encryptedContent]))
    print('Файл расшифрован.')


"""
CLI

while True:
    # Генерация ключей
    command = int(input('1. Сгенерировать ключ\n2. Зашифровать файл\n3. Расшифровать файл\n'))
    if command == 1:
        gen_key(key_name_from_datetime())
    # Шифрование
    elif command == 2:
        print('Имеющиеся публичные ключи:')
        [print(file) for file in os.listdir() if re.match('^public_.*', file)]
        public_key = input('Выберите открытый ключ: ')
        filename = input('Файл, который нужно зашифровать: ')
        encrypt(filename, public_key)
    # Расшифрование
    elif command == 3:
        print('Имеющиеся закрытые ключи:')
        [print(file) for file in os.listdir() if re.match('^private_.*', file)]
        secret_key = input('Выберите закрытый ключ: ')
        filename = input('Файл, который нужно расшифровать: ')
        decrypt(filename, secret_key)
"""