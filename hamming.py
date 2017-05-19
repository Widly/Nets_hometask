import socket
import pickle
import random
from numpy import array, dot, empty, append

hamming_code = (7, 4)
msg_size, data_size = hamming_code

parity_bits = [0, 1, 3]
data_bits = [2, 4, 5, 6]

G = array(((1, 1, 0, 1),
           (1, 0, 1, 1),
           (1, 0, 0, 0),
           (0, 1, 1, 1),
           (0, 1, 0, 0),
           (0, 0, 1, 0),
           (0, 0, 0, 1)))

H = array(((0, 0, 0, 1, 1, 1, 1),
           (0, 1, 1, 0, 0, 1, 1),
           (1, 0, 1, 0, 1, 0, 1)))


def encode(B):
    """ Encode data using Hamming(7, 4) code.
    E.g.:
        encode([0, 0, 1, 1])
        encode([[0, 0, 0, 1],
                [0, 1, 0, 1]])
    :param array B: binary data to encode (must be shaped as (4, ) or (-1, 4)).
    """
    B = array(B)

    flatten = False
    if len(B.shape) == 1:
        flatten = True
        B = B.reshape(1, -1)

    if B.shape[1] != data_size:
        raise ValueError('Data must be shaped as (4, ) or (-1, 4)')

    C = dot(G, B.T).T % 2

    if flatten:
        C = C.flatten()

    return C


def decode(C):
    """ Decode data using Hamming(7, 4) code.
    E.g.:
        decode([1, 0, 0, 0, 0, 1, 1])
        decode([[1, 1, 0, 1, 0, 0, 1],
                [0, 1, 0, 0, 1, 0, 1]])
    :param array C: binary data to code (must be shaped as (7, ) or (-1, 7)).
    """
    C = array(C)
    B = empty(0, dtype = int)

    if len(C.shape) == 1:
        C = C.reshape(1, -1)

    if C.shape[1] != msg_size:
        raise ValueError('Data must be shaped as (7, ) or (-1, 7)')

    syndromes = dot(H, C.T).T % 2

    for syndrome, code_vector in zip(syndromes, C):
        error_pos = 0
        for i in range(0, 3):
            if syndrome[i] == 1:
                error_pos += 2**(2 - i)

        if error_pos != 0:
            code_vector[error_pos - 1] = (code_vector[error_pos - 1] + 1) % 2

        B = append(B, code_vector[data_bits])

    return B


def encode_byte(byte):
    mask = 0b10000000
    data_vector = []

    for i in range(0, 8):
        if (byte & mask != 0):
            data_vector.append(1)
        else:
            data_vector.append(0)

        mask = mask >> 1

    data_vector = array(data_vector)
    data_vector = data_vector.reshape(2, 4)
    encoded_vector = encode(data_vector)

    encoded_byte = bytearray(2)
    encoded_byte[0] = int(''.join([str(bit) for bit in encoded_vector[0]]) + '0', 2)
    encoded_byte[1] = int(''.join([str(bit) for bit in encoded_vector[1]]) + '0', 2)

    return encoded_byte


def decode_byte(encoded_byte):
    encoded_vector = []
    decoded_byte = bytearray(1)

    for i in range(0, 2):
        mask = 0b10000000
        for j in range(0, 7):
            if (encoded_byte[i] & mask != 0):
                encoded_vector.append(1)
            else:
                encoded_vector.append(0)

            mask = mask >> 1

    encoded_vector = array(encoded_vector)
    encoded_vector = encoded_vector.reshape(2, 7)
    
    decoded_vector = decode(encoded_vector)
    mask = 0b10000000

    for i in range(0, 8):
        if (decoded_vector[i] == 1):
            decoded_byte[0] |= mask

        mask = mask >> 1

    return decoded_byte


def send_hamming(sock, addr):
    data = input('Enter the data\n')
    if (len(data) == 0):
        print('Entered data is empty')
        return

    data = bytearray(data, encoding = 'utf-8')
    encoded_data = bytearray(0)

    for i in range(0, len(data)):
        encoded_byte = encode_byte(data[i])
        encoded_byte[0] ^= (0b00000001 << random.randint(1, 7))
        encoded_byte[1] ^= (0b00000001 << random.randint(1, 7))
        encoded_data += encoded_byte[0:2]

    data_dict = {
        'alg_type' : 'hamming',
        'data' : encoded_data,
    }

    serialized_data = pickle.dumps(data_dict)
    sock.sendto(serialized_data, addr)


def decode_hamming(received_dict):
    received_data = received_dict['data']
    decoded_data = bytearray(0)

    for i in range(0, len(received_data), 2):
        decoded_data += decode_byte(received_data[i: i+2])

    print(decoded_data.decode('utf-8'))



if __name__ == '__main__':
    enc = encode_byte(0b10100101)
    print(hex(0b10100101))
    enc[0] ^= 0b00100000
    enc[1] ^= 0b00000100
    print(decode_byte(enc))