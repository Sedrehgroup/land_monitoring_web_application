from django.urls import path
from .views import Monitor


urlpatterns = [
    path('', Monitor.as_view()),
]