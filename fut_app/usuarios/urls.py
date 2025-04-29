from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('principal/', views.pagina_principal, name='pagina_principal'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('gerencia/', views.renderizar_pagina_gerenciador, name='gerencia')
]
