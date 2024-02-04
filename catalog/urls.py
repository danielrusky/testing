from django.urls import path

from catalog import views
from catalog.apps import CatalogConfig
from catalog.views import home, contact, product, create_category, create_product

app_name = CatalogConfig.name

urlpatterns = [
    path('', home, name='home'),
    path('contact/', contact, name='contact'),
    path('product/<int:pk>', product, name='product'),
    path('create_category/', create_category, name='create_category'),
    path('create_product/', create_product, name='create_product'),
    path('index', views.index, name='index'),
]
