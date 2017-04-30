import cv2

from lib.convert import resize_image


face_cascade = cv2.CascadeClassifier('../cascade/frontalFace.xml')
def face_recognition():
    recognizer = cv2.face.createLBPHFaceRecognizer()
    recognizer.load('../data/trainData.ext')
    img = cv2.imread('../public/test.jpg')
    faces = face_cascade.detectMultiScale(img, 1.2, 5)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    resize = resize_image(gray, 180, 180)
    id, conf = recognizer.predict(resize)
    print(conf)


face_recognition()