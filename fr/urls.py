from django.conf.urls import include, url

from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from user.views import retrain
urlpatterns = [

    url(r'', include('user.urls'),name='home'),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^retrain/', retrain, name='retrain'),
    url(r'^camera/', include('camera.urls', namespace='camera')),
    url(r'^setting/', include('setting.urls', namespace='setting')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)