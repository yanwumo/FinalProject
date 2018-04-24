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
        client_socket.send(b'0')
        lock.acquire()
        pic = local_pic
        lock.release()
        event.set()

        while True:
            raw_arr = np.frombuffer(connection.read(width * height), dtype=np.uint8)
            local_pic = np.reshape(raw_arr, (height, width))
            client_socket.send(b'0')
            lock.acquire()
            pic = local_pic
            lock.release()


if __name__ == "__main__":
    # Initialize classifier
    classifier = cv2.CascadeClassifier("stopsig n_classifier.xml")

    ClientThread().start()
    event.wait()
    while True:
        stop_signs = signdetect.detect_haar(classifier, pic, True)
        time.sleep(0.5)
