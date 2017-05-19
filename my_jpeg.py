from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import socket
import pickle

def send_jpeg(sock, addr):
    img = Image.open("in.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("sans-serif.ttf", 16)
    draw.text((0, 0), "JPEG TEXT TEST", (0,0,0), font=font)
    img.save('buff.jpg')

    with open('buff.jpg', 'rb') as f:
        encoded_data = bytearray(f.read())

    data_dict = {
        'alg_type' : 'jpeg',
        'cdata' : encoded_data
    }

    serialized_data = pickle.dumps(data_dict)
    sock.sendto(serialized_data, addr)

def decode_jpeg(received_dict):
    encoded_data = received_dict['cdata']

    with open('received_jpeg.jpeg', 'wb') as f:
        f.write(encoded_data)

if __name__ == '__main__':
    send_jpeg()