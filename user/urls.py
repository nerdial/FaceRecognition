from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.all_users, name='index'),
    url(r'import/$', views.create_dummy_users, name='create'),
    url(r'new/$', views.new_user, name='new'),
    url(r'show/(\d+)/$', views.show, name="show"),
    url(r'delete/(\d+)/$', views.delete_user, name="delete"),
    url(r'upload/$', views.simple_upload, name='simple_upload'),
    url(r'create/$', views.create_dummy_users, name='create'),
    url(r'log/(\d+)/$', views.user_logs, name='log'),
]

