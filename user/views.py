from django.shortcuts import redirect
from django.http import HttpResponseRedirect
import os
from django.shortcuts import render
from django.conf import settings
from user.models import User, Log
from django.core.files.storage import FileSystemStorage
from lib.convert import detect_convert
from lib.trainPictures import retrain_data
from camera.models import Camera
from setting.models import ProjectSetting


def all_users(request):
    users = User.objects.all()
    return render(request, 'user/list.html', {'users': users})


def show(request, id):
    user = User.objects.get(id=id)
    user_pictures = get_user_pictures(id)
    return render(request, 'user/show.html', {'user': user, 'images': user_pictures})


def new_user(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        user = User()
        user.name = name
        user.save()
        return redirect('/')
    return render(request, 'user/new.html', {})


def get_user_pictures(user_id):
    media = settings.MEDIA_URL
    images = os.listdir(media)
    user_pictures = []
    for image in images:
        file_id = (os.path.split(image)[-1].split('.')[0])
        if file_id == user_id:
            user_pictures.append(image)
    return user_pictures


def simple_upload(request):
    user_id = request.POST.get('user_id')
    if request.method == 'POST' and  'image' in request.FILES:
        image = request.FILES['image']
        user = User.objects.get(id=user_id)
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        detect_convert(uploaded_file_url, user)
        fs.delete(filename)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def retrain(request):
    setting = ProjectSetting.objects.first()
    r = retrain_data(setting)

    if r == 0:
        return render(request, 'user/retrain.html', {'message': False})
    else:
        return render(request, 'user/retrain.html', {'message': True})


def delete_user(request, id):
    user = User.objects.get(id=id)
    remove_user_pictures(id)
    user.delete()
    return redirect('/')


def remove_user_pictures(user_id):
    user_picture = get_user_pictures(user_id)
    fs = FileSystemStorage()
    for picture in user_picture:
        fs.delete(picture)


def user_logs(request, user_id):
    user = User.objects.get(id=user_id)
    logs = Log.objects.filter(user=user)
    return render(request, 'user/log.html', {'user': user, 'logs': logs})

def create_dummy_users(request):
    user1 = User()
    user1.username = 'vahidstar'
    user1.name = 'Vahid Mahdiun'
    user1.save()
    user1 = User()
    user1.username = 'mahdi'
    user1.name = 'Mahdi Mahdiun'
    user1.save()
    user1 = User()
    user1.username = 'alireza'
    user1.name = 'Alireza Mahdiun'
    user1.save()
    user1 = User()
    user1.username = 'mohammad'
    user1.name = 'Mohammad Mahdiun'
    user1.save()
    user1.username = 'barak'
    user1.name = 'Barak Ubama'
    user1.save()


    camera1 = Camera()
    camera1.url = 0
    camera1.active = True
    camera1.camera_type = 'enter'
    camera1.name = 'Camera 1'
    camera1.save()

    camera1 = Camera()
    camera1.url = 0
    camera1.active = True
    camera1.camera_type = 'exit'
    camera1.name = 'Camera 1'
    camera1.save()

    users = User.objects.all()
    return render(request, 'user/list.html', {'users': users})