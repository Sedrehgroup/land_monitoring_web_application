from django.urls import path
from .views import OrderStatistics , OrderObserv , ShowOrder , Index

urlpatterns = [
    path('statistics' , OrderStatistics.as_view()),
    path('observ' , OrderObserv.as_view()),
    path('orders' , ShowOrder.as_view()),
    path('index' , Index.as_view()),
]