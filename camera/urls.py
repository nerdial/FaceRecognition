from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.all_cameras, name='index'),
    url(r'takePicture/$', views.take_picture, name='picture'),
]

