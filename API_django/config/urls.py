from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/monitoring/', include('monitoring.urls'), name='monitoring'),
    path('api/identify/', include('identification.urls'), name='identify'),
    path('api/auth/', include('authe.urls')),
    path('api/analysis/', include('analysis.urls')),
    path('api/ordering/', include('ordering.urls')),
]
