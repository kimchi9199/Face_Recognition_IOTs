from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
import threading
import socket
import base64
import imutils
import time
import queue
import zmq



# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()

ap.add_argument('-mW', '--montageW', required=True, type=int,
    help="montage frame width")
ap.add_argument('-mH', '--montageH', required=True, type=int,
    help="montage frame height")
args = vars(ap.parse_args())

# initialize the ImageHub object
imageHub = imagezmq.ImageHub()

# initialize the dictionary which will contain information regarding
# when a device was last active, then store the last time the check
# was made was now
lastActive = {}
lastActiveCheck = datetime.now()

# initialize a frame dictionary
frameDict = {}

# stores the estimated number of Jetsons, active checking period, 
# and calculates the duration seconds to wait before making a check
# to see if a device was active
ESTIMATED_NUM_JETSONS = 1
ACTIVE_CHECK_PERIOD = 10
ACTIVE_CHECK_SECONDS = ESTIMATED_NUM_JETSONS * ACTIVE_CHECK_PERIOD

# assign montage width and height, so we can view all incoming frames
# in a single dashboard
mW = args['montageW']
mH = args['montageH']

frameDataQueue = queue.Queue()

print('Server started')




# def receive_video_frame_from_jetson_camera():
#     # start looping over all the frames
#     while True:
#
#         # received JetsonName and frame form the Jetson and acknowledge
#         # the receipt
#         (JetsonName, frame) = imageHub.recv_image()
#         imageHub.send_reply(b'OK')
#
#         # if a device is not in the last active dictionary then it means
#         # that it's a newly connected device
#         if JetsonName not in lastActive.keys():
#             print('[INFO] receiving data from {}...'.format(JetsonName))
#
#         # record the last active time for the device from which we just
#         # received a frame
#         lastActive[JetsonName] = datetime.now()
#
#         # resize the frame to have a maximum width of 400 pixels, then
#         # gram the frame dimension and construct a blob
#         frame = imutils.resize(frame, width=400)
#         frameDataQueue.put(frame)
#         (h, w) = frame.shape[:2]
#
#         # update the new frame in the frame dictionary
#         frameDict[JetsonName] = frame
#
#         # build a montage using images in the frame dictionary
#         montages = build_montages(frameDict.values(), (w, h), (mW, mH))
#
#         # display the montage(s) on the screen
#         for (i, montage) in enumerate(montages):
#             cv2.imshow('My house monitor: ({})'.format(i), montage)
#
#         # detect any keypresses
#         key = cv2.waitKey(1) & 0xFF
#
#
#         # if the 'q' was pressed, break from the loop
#         if key == ord('q'):
#             break
#     # do a bit of cleanup
#     cv2.destroyAllWindows()

def send_video_to_android_client():
    BUFF_SIZE = 65536
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
    host_name = socket.gethostname()
    host_ip = socket.gethostbyname(host_name)
    print(host_ip)
    port = 9999
    # socket_address = (host_ip, port)
    # server_socket.bind(socket_address)
    socket_address = ('192.168.234.2', port)
    server_socket.bind(socket_address)
    print('Listening at: ', socket_address)



    while True:
        msg, client_adr = server_socket.recvfrom(BUFF_SIZE)
        print('GOT connection from ', client_adr)
        WIDTH = 400
        while (1):
            frame = frameDataQueue.get()
            frame = imutils.resize(frame, width=WIDTH)
            encoded, buffer = cv2.imencode('.jpg', frame)
            message = base64.b64encode(buffer)
            print(message)
            server_socket.sendto(message, client_adr)
            print(client_adr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                server_socket.close()
                break



# receiveVideoFrameThread = threading.Thread(target=receive_video_frame_from_jetson_camera)
sendVideoFrameThread = threading.Thread(target=send_video_to_android_client)


# receiveVideoFrameThread.start()
sendVideoFrameThread.start()


# start looping over all the frames
while True:

    # received JetsonName and frame form the Jetson and acknowledge
    # the receipt
    (JetsonName, frame) = imageHub.recv_image()
    imageHub.send_reply(b'OK')

    # if a device is not in the last active dictionary then it means
    # that it's a newly connected device
    if JetsonName not in lastActive.keys():
        print('[INFO] receiving data from {}...'.format(JetsonName))

    # record the last active time for the device from which we just
    # received a frame
    lastActive[JetsonName] = datetime.now()

    # resize the frame to have a maximum width of 400 pixels, then
    # gram the frame dimension and construct a blob
    frame = imutils.resize(frame, width=400)
    frameDataQueue.put(frame)
    (h, w) = frame.shape[:2]

    # update the new frame in the frame dictionary
    frameDict[JetsonName] = frame

    # build a montage using images in the frame dictionary
    montages = build_montages(frameDict.values(), (w, h), (mW, mH))

    # display the montage(s) on the screen
    for (i, montage) in enumerate(montages):
        cv2.imshow('My house monitor: ({})'.format(i), montage)

    # detect any keypresses
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' was pressed, break from the loop
    if key == ord('q'):
        break
# do a bit of cleanup
cv2.destroyAllWindows()


# receiveVideoFrameThread.join()
sendVideoFrameThread.join()



