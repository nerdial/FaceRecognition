import os, cv2
import numpy as np
from PIL import Image
from lib.faceRecognition import get_recognizer


def retrain_data(setting):
    recognizer = get_recognizer(setting)
    path = 'public/images/'
    def getImagesAndIds(path):
        imagePaths= [os.path.join(path,f) for f in os.listdir(path)]
        faces = []
        ids = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg,'uint8')
            id = int(os.path.split(imagePath)[-1].split('.')[0])
            faces.append(faceNp)
            ids.append(id)

        return ids, faces
    ids, faces = getImagesAndIds(path)
    if len(faces) == 0:
        return 0
    else:
        ids = (np.array(ids))
        recognizer.train(faces, ids)
        recognizer.save('data/trainData.ext')
