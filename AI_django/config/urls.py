from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/geoserver', include('geoserver.urls')),
    path('ai/change_detection/', include('image_analysis.urls')),
]
