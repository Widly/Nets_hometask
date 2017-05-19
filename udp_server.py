import socket
import pickle
from zlib import crc32
from hamming import decode_hamming
from CRC import decode_crc32
from shannon_fano import decode_shannon_fano
from my_lzw import decode_lzw
from my_jpeg import decode_jpeg

if __name__ == '__main__':
	UDP_IP = "127.0.0.1"
	UDP_PORT = 8080

	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	sock.bind((UDP_IP, UDP_PORT))

	decoder_dict = {
		'crc32' : decode_crc32,
		'hamming' : decode_hamming,
		'shannon_fano' : decode_shannon_fano,
		'lzw' : decode_lzw,
		'jpeg' : decode_jpeg
	}

	while True:
		data = sock.recv(16384)

		received_dict = pickle.loads(data)
		decoder_dict[received_dict['alg_type']](received_dict)