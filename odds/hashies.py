import hashlib


def big_end_int_64(data: bytes) -> int:
    return int.from_bytes(hashlib.sha256(data).digest()[:8], 'little')


def big_end_bytes_64(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()[:8]


def big_end_str_64(d: bytes) -> str:
    return hashlib.sha256(d).hexdigest()[:16]


def big_end_hex_64(d: bytes) -> str:
    return hex(int.from_bytes(hashlib.sha256(d).digest()[:8], 'little'))


def main():
    s = b"baby, let's cruise"

    print(big_end_int_64(s))

    print(big_end_bytes_64(s))

    print(big_end_str_64(s))

    print(big_end_hex_64(s))


if __name__ == "__main__":
    main()
