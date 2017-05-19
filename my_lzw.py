import lzw
import socket
import pickle

text = (b'Lorem ipsum dolor sit amet, consectetur adipiscing elit, '
          b'sed do eiusmod tempor incididunt ut labore et dolore magn'
          b'a aliqua. Ut enim ad minim veniam, quis nostrud exercitat'
          b'ion ullamco laboris nisi ut aliquip ex ea commodo consequ'
          b'at. Duis aute irure dolor in reprehenderit in voluptate v'
          b'elit esse cillum dolore eu fugiat nulla pariatur. Excepte'
          b'ur sint occaecat cupidatat non proident, sunt in culpa qu'
          b'i officia deserunt mollit anim id est laborum.')

def send_lzw(sock, addr):
    print('raw data len = ', len(text))
    encoded_data = lzw.compress(text)
    lzw.writebytes('compressed.lzw', encoded_data)

    encoded_data = None
    with open('compressed.lzw', 'rb') as f:
        encoded_data = bytearray(f.read())

    print('encoded data len = ', len(encoded_data))

    data_dict = {
        'alg_type' : 'lzw',
        'cdata' : encoded_data
    }

    serialized_data = pickle.dumps(data_dict)
    sock.sendto(serialized_data, addr)

def decode_lzw(received_dict):
    encoded_data = received_dict['cdata']

    with open('received_lzw.lzw', 'wb') as f:
        f.write(encoded_data)

    infile = lzw.readbytes("received_lzw.lzw")
    uncompressed = lzw.decompress(infile)

    decoded_data = bytearray(0)
    for byte in uncompressed:
        decoded_data += byte

    print(decoded_data.decode('utf-8'))

if __name__ == '__main__':
    pass