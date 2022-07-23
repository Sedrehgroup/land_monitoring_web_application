from django.urls import path
from .views import ChangeDetectionStatics, ChangeDetectionPolygon, ClassStaticsGeom, ClassStatics, ClassIndiv, ManualRun

ManualRun
urlpatterns = [
    path('statics', ChangeDetectionStatics.as_view()),
    path('polygon', ChangeDetectionPolygon.as_view()),
    path('index', ClassStatics.as_view()),
    path('index-geom', ClassStaticsGeom.as_view()),
    path('indiv', ClassIndiv.as_view()),
    path('manual-run', ManualRun.as_view()),
]