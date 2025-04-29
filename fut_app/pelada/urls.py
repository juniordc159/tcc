from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerenciador, name='gerenciador'),
]
