import socket
import numpy as np
import cv2
import signdetect
from matplotlib import pyplot as plt
import threading
import time

width = 416
height = 304

pic = []
lock = threading.Lock()
event = threading.Event()


class ClientThread(threading.Thread):
    def run(self):
        global pic
        # Connect a client socket to my_server:8000 (change my_server to the
        # hostname of your server)
        client_socket = socket.socket()
        client_socket.connect(('192.168.2.3', 8000))
        connection = client_socket.makefile('rb')

        client_socket.send(b'0')
        raw_arr = np.frombuffer(connection.read(width * height), dtype=np.uint8)
        local_pic = np.reshape(raw_arr, (height, width))
        lock.acquire()
        pic = local_pic
        lock.release()
        event.set()

        while True:
            client_socket.send(b'0')
            raw_arr = np.frombuffer(connection.read(width * height), dtype=np.uint8)
            local_pic = np.reshape(raw_arr, (height, width))
            lock.acquire()
            pic = local_pic
            lock.release()


if __name__ == "__main__":
    ClientThread().start()
    event.wait()
    while True:
        signdetect.detect_haar("stopsign_classifier.xml", pic, True)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        time.sleep(0.1)
