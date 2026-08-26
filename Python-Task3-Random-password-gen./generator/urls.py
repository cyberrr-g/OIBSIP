from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('generate/', views.generate_password_view, name='generate_password'),
]
