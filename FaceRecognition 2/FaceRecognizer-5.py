import cv2
import face_recognition as fr
import os
import pickle


Encodings = [] # Known encoded faces
Names = [] # Names of each known faces


# load trained model
with open('trained_model.pkl', 'rb') as f:
    Names = pickle.load(f) # load known name of each faces
    Encodings = pickle.load(f) # load know faces


font = cv2.FONT_HERSHEY_COMPLEX # define font
camera = cv2.VideoCapture(0) # define camera 


while True:
    _, frame = camera.read() # capture video from camera
    frameSmall = cv2.resize(frame, (0, 0), fx=.33, fy=.33) # resize each frames to make it process faster

    # openCV work with image in BGR format, so we need to convert it back to RGB
    # hmmm, openCV is weird =((
    frameRGB = cv2.cvtColor(frameSmall, cv2.COLOR_BGR2RGB) 

    facePositions = fr.face_locations(frameRGB, model='cnn') # fine faces location in each frame

    allEncodings = fr.face_encodings(frameRGB, facePositions) # encode each faces in the frame
    
    # loop through each face positions and each encoded faces
    for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
        name = 'Stranger'
        matches = fr.compare_faces(Encodings, face_encoding) # compare encoded face with known faces

        if True in matches:
            first_match_index = matches.index(True)
            name = Names[first_match_index]
        
        # scale the frame back to the original size
        top = top * 3
        right = right * 3
        left = left * 3
        bottom = bottom * 3

        # make a bounding box and put the name above the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.putText(frame, name, (left, top-6), font, .75, (0, 0, 255), 2)

    cv2.imshow('frame', frame)
    cv2.moveWindow('frame', 0, 0)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()