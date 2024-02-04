from django.urls import path

from catalog import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contacts/', views.contact, name='contacts'),
    path('index', views.index, name='index'),
]