from django.urls import path

from . import views

urlpatterns = [
    path('search/', views.search, name='search'),
    path('save/', views.save, name='save'),
    path('user/', views.user, name='user_product'),
    path('<int:product_id>/', views.detail, name='detail'),
]
