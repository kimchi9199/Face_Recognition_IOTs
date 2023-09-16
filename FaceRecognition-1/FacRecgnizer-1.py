import face_recognition as fc
import cv2
# print(cv2.__version__)

image = fc.load_image_file('/home/thainguyen/Study/IoT/KC/FaceRecognition/demoImages/unknown/u3.jpg')
face_locations = fc.face_locations(image)
print(face_locations)

# openCV work with image as BGR, so we need to convert RGB to BGR
# hmmm, openCV is weird =((
image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

for(row1, col1, row2, col2) in face_locations:
    cv2.rectangle(image, (col1, row1), (col2, row2), (0, 0, 255), 2)

cv2.imshow('image', image)
cv2.moveWindow('image', 0, 0)
if cv2.waitKey(0) == ord('q'):
    cv2.destroyAllWindows()