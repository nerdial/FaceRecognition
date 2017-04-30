import cv2
import random
def detect_convert(image, user):
    img = cv2.imread(image)
    face_cascade = cv2.CascadeClassifier('cascade/frontalFace.xml')
    number = random.randrange(1,100)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    user.last_id += 1
    for (x, y, w, h) in faces:
        gray = gray[y:y+h, x:x+w]
        gray = resize_image(gray, 180,180)
        if gray is None:
            break
        cv2.imwrite('public/images/'+ str(user.id)+ '.' + str(user.last_id) +'.jpg', gray)
    user.save()

def resize_image(image, w, h):

    height, width = image.shape[:2]
    if height == 0 or width == 0:
        return None
    if height > h and width > w:
        image = cv2.resize(image, (w, h))
    elif height == h and width == w:
         image = cv2.resize(image, (w, h))
    else:
        image = cv2.resize(image,(width+(w - width), height+(h - height)), interpolation = cv2.INTER_CUBIC)
    return image