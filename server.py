import io
import socket
import picamera
import bluepy.btle as btle

# Initialize bluetooth
print("Connecting to Bluetooth LE...")
p = btle.Peripheral("34:15:13:1C:68:DD")
s = p.getServiceByUUID("0000ffe0-0000-1000-8000-00805f9b34fb")
c = s.getCharacteristics()[0]
print("Connected")

width = 416
height = 304

# Initialize camera
camera = picamera.PiCamera(sensor_mode=4, resolution='416x304', framerate=40)
#camera.resolution = (width, height)
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
        if data == b'1':
            c.write(b'1')
            continue
        print("Capture")
        camera.capture(stream, 'yuv')
        print("Capture ends")
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream.read(width * height))
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
        print("Sent")


finally:
    connection.close()
    server_socket.close()
    camera.stop_preview()
    p.disconnect()
