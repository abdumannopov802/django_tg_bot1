from django.urls import path
from . import views

urlpatterns = [
    path('getpost/', views.index, name='telegram_bot'),
    path('setwebhook/', views.setwebhook, name='setwebhook'),
]