from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


urlpatterns = [ 
    path('api/', include('users.urls')),
    path('api/', include('crops.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)