import io
import socket
import struct
import picamera

# Initialize camera
camera = picamera.PiCamera()
camera.resolution = (320, 240)
# Start a preview
camera.start_preview()
stream = io.BytesIO()

# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

conn = server_socket.accept()
connection = conn[0].makefile('wb')

try:
    while True:
        data = conn[0].recv(10)
        if not data:
            break
        print("Capture")
        camera.capture(stream, 'yuv')
        print("Capture ends")
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        # connection.write(struct.pack('<L', stream.tell()))
        # connection.write(struct.pack('<L', 640 * 480))
        # connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read(320 * 240))
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        print("Sent")


finally:
    connection.close()
    server_socket.close()
    camera.stop_preview()
