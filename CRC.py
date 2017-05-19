from zlib import crc32
import random
import pickle

def send_crc32(sock, addr):
	data = input('Enter the data\n')
	if (len(data) == 0):
		print('Entered data is empty')
		return

	data = bytearray(data, encoding = 'utf-8')
	checksum = crc32(data)

	data[random.randint(0, len(data) - 1)] += 1
	print(hex(checksum))

	data_dict = {
		'alg_type' : 'crc32',
		'data' : data,
		'checksum' : checksum
	}

	serialized_data = pickle.dumps(data_dict)
	sock.sendto(serialized_data, addr)

def decode_crc32(received_dict):
	checksum = crc32(received_dict['data'])
	if (checksum - received_dict['checksum'] != 0):
		print('An error occurred!')
	else:
		print('OK!')

	print(received_dict['data'].decode('utf-8'), hex(checksum))