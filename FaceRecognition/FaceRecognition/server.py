from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
# ap.add_argument('-p,', '--prototxt', required=True,
#     help="path to Caffe 'deploy' prototxt file")
# ap.add_argument('-m', '--model', required=True,
#     help="path to Caffe pre-trained model")
# ap.add_argument('-c', '--confidence', type=float, default=0.2,
#     help="minimum probability to filter weak detections")
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

# start looping over all the frames

print('Server started')
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
    (h, w) = frame.shape[:2]
    # blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 
    #     0.007843, (300, 300), 127.5)

    # update the new frame in the frame dictionary
    frameDict[JetsonName] = frame

    # build a montage using images in the frame dictionary
    montages = build_montages(frameDict.values(), (w, h), (mW, mH))

    # display the montage(s) on the screen
    for (i, montage) in enumerate(montages):
        cv2.imshow('My house monitor: ({})'.format(i), montage)
    
    # detect any keypresses
    key = cv2.waitKey(1) & 0xFF

    # if current time minus last time when the active device check 
    # was made is greater than the threshold set then do a check
    if (datetime.now() - lastActiveCheck).seconds > ACTIVE_CHECK_SECONDS:
        # loop over all previously active devices
        for(JetsonName, ts) in list(lastActive.items()):
            # remove the Jetson from the last active and frame
            # dictionaries if the device hasn't been active recently
            if (datetime.now() - ts).seconds > ACTIVE_CHECK_SECONDS:
                print('[INFO] lost connection to {}'.format(JetsonName))
                lastActive.pop(JetsonName)
                frameDict.pop(JetsonName)

        # set the last active check time as current time
        lastActiveCheck = datetime.now()
    
    # if the 'q' was pressed, break from the loop
    if key == ord('q'):
        break
# do a bit of cleanup
cv2.destroyAllWindows()