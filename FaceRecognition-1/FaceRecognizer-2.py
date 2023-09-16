import face_recognition as fc
import cv2

Donface = fc.load_image_file('./demoImages/known/Donald Trump.jpg')
DonfaceEncode = fc.face_encodings(Donface)[0]

Nancyface = fc.load_image_file('./demoImages/known/Nancy Pelosi.jpg')
NancyfaceEncode = fc.face_encodings(Nancyface)[0]

Encodings = [DonfaceEncode, NancyfaceEncode]
Names = ['Donal Trump', 'Nancy Pelosi']

font = cv2.FONT_HERSHEY_SIMPLEX

testImage = fc.load_image_file('./demoImages/unknown/u11.jpg')
facePositions = fc.face_locations(testImage)

allEncoding = fc.face_encodings(testImage, facePositions)

# openCV work with image as BGR, so we need to convert RGB to BGR
# hmmm, openCV is weird =((
testImage = cv2.cvtColor(testImage, cv2.COLOR_RGB2BGR)

for (top, right, bottom, left), face_encoding in zip(facePositions,  allEncoding):
    name = 'Stranger'
    matches = fc.compare_faces(Encodings, face_encoding)
    if True in matches:
        first_match_index = matches.index(True)
        name = Names[first_match_index]
    cv2.rectangle(testImage, (left, top), (right, bottom), (0, 0, 255), 2)
    cv2.putText(testImage, name, (left, top-6), font, .75, (0, 255, 255), 2)
cv2.imshow('image', testImage)
cv2.moveWindow('image', 0, 0)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows