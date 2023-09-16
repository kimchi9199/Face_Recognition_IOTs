import cv2
import os
import pickle
import face_recognition as fr 
Encodings = []
Names = []
j = 0

image_dir = '/home/thainguyen/Study/IoT/KC/FaceRecognition/demoImages/known'

for root, dirs, files in os.walk(image_dir):
    # print(files)
    for file in files:
        path = os.path.join(root, file)
        # print(path)
        name = os.path.splitext(file)[0]
        print(name)
        person = fr.load_image_file(path)
        encoding = fr.face_encodings(person)[0]
        Encodings.append(encoding)
        Names.append(name)
print(Names)

with open('trained_model.pkl', 'wb') as f:
    pickle.dump(Names, f)
    pickle.dump(Encodings, f)