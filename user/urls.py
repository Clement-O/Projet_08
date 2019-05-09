from django.urls import path
# Local import
from . import views

app_name = 'user'
urlpatterns = [
    path('', views.user_mail, name='user_mail')
]
