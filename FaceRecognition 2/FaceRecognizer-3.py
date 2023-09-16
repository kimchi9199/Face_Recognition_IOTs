import cv2
import os
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

font = cv2.FONT_HERSHEY_SIMPLEX

image_dir_unk = '/home/thainguyen/Study/IoT/KC/FaceRecognition/demoImages/unknown'

for root, dirs, files in os.walk(image_dir_unk):
    for file in files:
        print(root)
        print(file)
        testImagePath = os.path.join(root, file)
        testImage = fr.load_image_file(testImagePath)
        facePositions = fr.face_locations(testImage)
        allEncodings = fr.face_encodings(testImage, facePositions)
        testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)



        for (top, right, bottom, left), face_encoding in zip(facePositions, allEncodings):
            name = 'Stranger'
            matches = fr.compare_faces(Encodings, face_encoding)
            if True in matches:
                first_match_index = matches.index(True)
                name = Names[first_match_index]
            cv2.rectangle(testImage, (left, top), (right, bottom), (0, 0, 255), 2)
            cv2.putText(testImage, name, (left, top-6), font, .75, (0, 255, 255), 2)
        cv2.imshow('image', testImage)
        cv2.moveWindow('image', 0, 0)
        if cv2.waitKey(0) == ord('q'):
            cv2.destroyAllWindows

