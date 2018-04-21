import io
import socket
import struct
import time
import numpy as np
import cv2
import signdetect
from matplotlib import pyplot as plt

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('192.168.1.3', 8000))
connection = client_socket.makefile('rb')

while True:
    client_socket.send(b'k')

    raw_arr = np.frombuffer(connection.read(320 * 240), dtype=np.uint8)
    pic = np.reshape(raw_arr, (240, 320))
    #pic = cv2.resize(pic, (0, 0), fx=0.4, fy=0.4)

    #cv2.imshow("frame", pic)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    signdetect.detect_haar("stopsign_classifier.xml", pic, True)
