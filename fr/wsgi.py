"""
WSGI config for fr project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os
import time
from django.core.wsgi import get_wsgi_application
from setting.models import ProjectSetting
from threading import Thread
from camera.models import Camera
from lib.faceRecognition import face_recognition


def run_active_cameras(camera, setting):
    face_recognition(camera, setting)


def check_for_camera(cameras):

    setting = ProjectSetting.objects.first()
    for camera in cameras:
        print(camera.name + ' is activated')
        camera.in_use_mode()
        t = Thread(target=run_active_cameras, args=(camera, setting))
        t.start()


def start_check_for_camera():
    while True:
        cameras = Camera.objects.filter(in_use=False, active=True)
        check_for_camera(cameras)
        time.sleep(2)

new_t = Thread(target=start_check_for_camera)
new_t.start()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fr.settings")

application = get_wsgi_application()



