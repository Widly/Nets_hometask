from collections import Counter
import socket
import pickle
from utils import int_to_bytes, int_from_bytes

text = (b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
          b'sed do eiusmod tempor incididunt ut labore et dolore magn'
          b'a aliqua. Ut enim ad minim veniam, quis nostrud exercitat'
          b'ion ullamco laboris nisi ut aliquip ex ea commodo consequ'
          b'at. Duis aute irure dolor in reprehenderit in voluptate v'
          b'elit esse cillum dolore eu fugiat nulla pariatur. Excepte'
          b'ur sint occaecat cupidatat non proident, sunt in culpa qu'
          b'i officia deserunt mollit anim id est laborum.')


def split_two(arr, i):
    if len(arr) <= 1:
        return arr, []

    left, right = arr[:i], arr[i:]

    if left and right:
        return left, right
    else:
        return left or right, []


def build_dict(text):
    counter = Counter(text)
    arr = counter.most_common()

    result = {}

    def _build_dict(part, suffix):
        # print(part, suffix)
        if len(part) == 1:
            result[part[0][0]] = suffix
            return
        elif len(part) == 0:
            return

        i = 0
        acc = 0
        limit = sum(weight for code, weight in part) // 2
        for i, (code, weight) in enumerate(part):
            acc += weight
            if acc >= limit:
                break

        l, r = split_two(part, i+1)
        _build_dict(l, suffix+'0')
        _build_dict(r, suffix+'1')

    _build_dict(arr, '')
    return result


def shannonfano_encode(text, codedict=None):
    if codedict is None:
        codedict = build_dict(text)
    return int_to_bytes(int(''.join(codedict[c] for c in text), 2)), pack_dict(codedict)


def shannonfano_decode(text, codedict):
    codedict = unpack_dict(codedict)
    text = '{:b}'.format(int_from_bytes(text)).encode()

    codedict = {v: k for k, v in codedict.items()}
    res = b''
    word = b''
    for c in text:
        word += bytes((c,))
        try:
            char = codedict[word.decode()]
        except KeyError:
            pass
        else:
            res += bytes((char,))
            word = b''
    assert word == b''
    return res


def pack_dict(codedict):
    return int_to_bytes(int('1'+''.join(
        '{:03b}'.format(len(code)-1) + '{:08b}'.format(orig) + '{}'.format(code)
        for orig, code
        in codedict.items()
    ), 2))


def unpack_dict(coded):
    res = {}
    coded = '{:b}'.format(int_from_bytes(coded))[1:]

    while coded:
        try:
            length = int(coded[:3], 2)+1
            res[int(coded[3:11], 2)] = coded[11:11+length]
        except ValueError:
            pass
        finally:
            coded = coded[11 + length:]

    return res

def send_shannon_fano(sock, addr):
    print('raw data len = ', len(text))
    encoded_text, cdict = shannonfano_encode(text)
    print('encoded data len = ', (len(encoded_text) + len(cdict)))
    data_dict = {
        'alg_type' : 'shannon_fano',
        'ctext' : encoded_text,
        'cdict' : cdict
    }

    serialized_data = pickle.dumps(data_dict)
    sock.sendto(serialized_data, addr)

def decode_shannon_fano(received_dict):
    decoded_text = shannonfano_decode(received_dict['ctext'], received_dict['cdict'])
    print(decoded_text)

if __name__ == '__main__':
    encoded_text, cdict = shannonfano_encode(text)
    shannonfano_decode(encoded_text, cdict)