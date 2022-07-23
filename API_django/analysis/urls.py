from django.urls import include , path
from .views import ChangeDetectionStatics, ChangeDetectionPolygon, ClassStaticsGeom, ClassStatics, ClassIndiv, ManualRun , ClassLastAreaChanges , ClassYearAreaChanges ,Some



urlpatterns = [
    path('statics', ChangeDetectionStatics.as_view()),
    path('polygon', ChangeDetectionPolygon.as_view()),
    path('index', ClassStatics.as_view()),
    path('index-geom', ClassStaticsGeom.as_view()),
    path('indiv', ClassIndiv.as_view()),
    path('manual-run', ManualRun.as_view()),
    path('class-last-change', ClassLastAreaChanges.as_view()),
    path('class-year-change', ClassYearAreaChanges.as_view()),
    path('test', Some.as_view()),

]