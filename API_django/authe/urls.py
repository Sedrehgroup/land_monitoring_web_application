from django.urls import path, include
from .views import Geometry, SetActive, SetGeometry, UserGeometry, Users

urlpatterns = [
    path('geom', Geometry.as_view()),
    path('dj-rest-auth/', include('dj_rest_auth.urls')),
    path('dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
    path('activate', SetActive.as_view()),
    path('set-geom', SetGeometry.as_view()),
    path('users', Users.as_view()),
    path('user-geom', UserGeometry.as_view()),
]