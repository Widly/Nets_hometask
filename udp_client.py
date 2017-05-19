import socket
from hamming import send_hamming
from CRC import send_crc32
from shannon_fano import send_shannon_fano
from my_lzw import send_lzw
from my_jpeg import send_jpeg

if __name__ == '__main__':
	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	send_hamming(sock, ('127.0.0.1', 8080))
	#send_crc32(sock, ('127.0.0.1', 8080))
	#send_shannon_fano(sock, ('127.0.0.1', 8080))
	#send_lzw(sock, ('127.0.0.1', 8080))
	#send_jpeg(sock, ('127.0.0.1', 8080))