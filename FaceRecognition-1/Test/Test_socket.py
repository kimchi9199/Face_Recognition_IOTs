import cv2
import socket
import struct
import sys

HOST = '192.168.1.12'
PORT = 8888

def stream_video():
    camera = cv2.VideoCapture(0)

    # set up socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()

        # Accept incoming connections
        conn, addr = s.accept()
        with conn:
            print('Connected by', addr)

            # Loop to capture and send video frames
            while True:
                # Capture frame
                ret, frame = camera.read()
                if not ret:
                    break
                frame = cv2.resize(frame, (640, 480))
                # Convert frame to byte string
                data = cv2.imencode('.jpg', frame)[1].tobytes()

                # send frame size and frame data over socket
                conn.send(struct.pack('<L', len(data)))
                conn.send(data)

def test_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('socket created')
    try:
        s.bind((HOST, PORT))
    except socket.error as err:
        print('Bind failed, Error code: ' + str(err[0]) + ', Message: ' + err[1])
        sys.exit()
    print('Socket Bind Success!')

    s.listen(10)
    print('Socket is now listening')

    while 1:
        conn, addr = s.accept()
        print('Connect with ' + addr[0] + ':' + str(addr[1]))
        buf = conn.recv(64)
        print(buf)
    s.close()

if __name__ == '__main__':
    stream_video()
    # test_socket()