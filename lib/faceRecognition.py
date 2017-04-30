import cv2
import numpy as np
from lib.convert import resize_image
from user.models import get_user_by_id, create_new_log
from camera.models import Camera
face_cascade = cv2.CascadeClassifier('cascade/frontalFace.xml')


def get_recognizer(setting):
    if setting.recognition_algorithm == "createEigenFaceRecognizer":
        return cv2.face.createEigenFaceRecognizer()
    elif setting.recognition_algorithm == "createFisherFaceRecognizer":
        return cv2.face.createFisherFaceRecognizer()
    else:
        return cv2.face.createLBPHFaceRecognizer()


def check_force_stop(camera_id):
    camera = Camera.objects.get(id=camera_id)
    if camera.active:
        return False
    else:
        return True


def face_recognition(camera, setting):
    recognizer = get_recognizer(setting)
    recognizer.load('data/trainData.ext')
    if camera.type == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(camera.url)

    font = cv2.FONT_HERSHEY_SIMPLEX
    while True:
        if check_force_stop(camera.id):
            break

        # camera_update = Camera.objects.get(id=camera.id)
        # if camera_update.active == False:
        #     break
        ret, img = cap.read()
        img = cv2.resize(img, (camera.width, camera.height))
        if ret:

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:

                #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                gray = gray[y:y+h, x:x+w]
                text = 'Guest'
                gray = resize_image(gray, 180, 180)
                if gray is None:
                    break
                id, conf = recognizer.predict(gray)
                print(conf)
                if id is None:
                   text = 'Guest'
                else:
                    person = get_user_by_id(id=id)
                    if person is None:
                       text = 'Guest'
                    elif int(conf) <= int(setting.confidence):

                        create_new_log(person, camera.camera_type)
                        text = person.name
                        #cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                        #cv2.putText(img, text, (x, y+h), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


        #cv2.imshow(camera.name, img)
        if cv2.waitKey(1) == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    camera.in_active_mode()
    print(camera.name + " is inactivated")
