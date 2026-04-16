from binascii import crc32
import itertools

target_crc = 0xEC40CA13

for char_codes in itertools.product(range(128), repeat=3):
    candidate = ''.join(chr(code) for code in char_codes)
    if crc32(candidate.encode()) == target_crc:
        print("匹配的字符串：", candidate)
        break 