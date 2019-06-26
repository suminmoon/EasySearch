from django.urls import path
from . import views

app_name ='pages'

urlpatterns= [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('detail/', views.detail, name='detail'),
    path('result/<str:serial_no>/', views.result, name='result'),
    path('telegram/', views.telegram, name='telegram'),
    path('telegram_bot/', views.telegram_bot, name='telegram_bot'),
    # path('result/', views.result, name='result'),


]