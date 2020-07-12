from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload, name='htmlupload'),
    path('upload2/', views.upload2, name='htmlupload2'),
]
