from django.shortcuts import render
from camera.models import Camera
from user.models import User
from lib.takePicture import take_user_picture
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse
from setting.models import ProjectSetting

def all_cameras(request):
    cameras = Camera.objects.all()
    return render(request, 'camera/list.html', {'cameras': cameras})


def take_picture(request):
    cameras = Camera.objects.all()
    users = User.objects.all()

    if request.method == 'POST':
        user_id = request.POST.get('user')
        camera_id = request.POST.get('camera')
        number = request.POST.get('number')
        user = User.objects.filter(id=user_id).first()
        camera = Camera.objects.filter(id=camera_id).first()
        camera.active = False
        camera.in_use = False
        camera.save()
        setting = ProjectSetting.objects.first()
        take_user_picture(user, number, camera, setting)
        return HttpResponseRedirect(reverse('user:show', args=[user.id]))
    return render(request, 'camera/take_picture.html', {'users': users, 'cameras': cameras})
