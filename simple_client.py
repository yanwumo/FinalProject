import socket
import numpy as np
import cv2
import signdetect
from matplotlib import pyplot as plt

width = 416
height = 304

# Initialize classifier
classifier = cv2.CascadeClassifier("stopsign_classifier.xml")

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.2.3', 8000))
connection = client_socket.makefile('rb')

num_no_qualified_stop_sign = 5

while True:
    client_socket.send(b'0')
    raw_arr = np.frombuffer(connection.read(width * height), dtype=np.uint8)
    pic = np.reshape(raw_arr, (height, width))
    stop_signs = signdetect.detect_haar(classifier, pic, True)
    has_qualified_stop_sign = False
    for (x, y, w, h) in stop_signs:
        if x + w > width - 100 or y + h > height - 100:
            has_qualified_stop_sign = True
    if has_qualified_stop_sign:
        if num_no_qualified_stop_sign >= 5:
            client_socket.send(b'1')
            print("STOP")
        num_no_qualified_stop_sign = 0
    else:
        num_no_qualified_stop_sign += 1
