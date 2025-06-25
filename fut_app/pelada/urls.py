from django.urls import path
from . import views  # Importa o módulo views


urlpatterns = [
    path('', views.gerenciador, name='gerenciador'),
    path('pelada/criar/', views.cadastra_pelada, name='cadastra_pelada'),
    path('pelada/<int:pelada_id>/editar/', views.editar_pelada, name='editar_pelada'),
    path('pelada/<int:pelada_id>/excluir/', views.excluir_pelada, name='excluir_pelada'),
    path('pelada/<int:player_id>/remove_jogador/', views.remove_jogador, name='remove_jogador'),
    path('pelada/<int:pelada_id>/salva/', views.salva_pelada, name='salva_pelada'),
    path('pelada/<int:pelada_id>/sortear/', views.sortear_times, name='sortear_times'),
]
