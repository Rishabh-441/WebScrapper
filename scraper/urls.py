from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_product, name='search_product'),
    path('download_csv/', views.download_csv, name='download_csv'),  # Add this line
]
