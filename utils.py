def int_from_bytes(xbytes):
    return int.from_bytes(xbytes, 'big')


def int_to_bytes(x):
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')


def from_str_to_bits(s):
    return [int(c == '1') for c in s]