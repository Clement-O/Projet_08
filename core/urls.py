from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('disclaimer/', views.disclaimer, name='disclaimer'),
]
