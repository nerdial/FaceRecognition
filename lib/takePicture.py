import cv2
from lib.convert import resize_image
from lib.trainPictures import retrain_data


def take_user_picture(user, number, camera, setting):
    camera.in_use_mode()
    print(camera.name + " is inuse")
    number = int(number)
    face_cascade = cv2.CascadeClassifier('cascade/frontalFace.xml')
    if camera.type == "Webcam":
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(camera.url)
    name = user.id
    last_id = user.last_id
    image_counter = 0
    while True:
        ret, img = cap.read()
        if ret:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                last_id += 1
                image_counter += 1
                gray = gray[y:y+h, x:x+w]
                gray = resize_image(gray, 180, 180)
                if gray is None:
                    break
                cv2.imwrite('public/images/'+str(name)+'.'+str(last_id)+'.jpg',gray )
                cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)
                cv2.waitKey(100)
            cv2.imshow('img', img)
            k = cv2.waitKey(1)
            if image_counter > number:
                break




    user.last_id = last_id
    user.save()
    cap.release()
    cv2.destroyAllWindows()
    retrain_data(setting)
    camera.in_active_mode()
    print(camera.name + " is inactivated")


