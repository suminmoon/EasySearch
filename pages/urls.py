from django.urls import path
from . import views

app_name ='pages'

urlpatterns= [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('detail/', views.detail, name='detail'),
    path('pop/', views.pop, name='pop'),



]