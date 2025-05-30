from django.urls import path
from . import views

urlpatterns = [
    path('', views.gerenciador, name='gerenciador'),
    path('pelada/criar/', views.cadastra_pelada, name='cadastra_pelada'),
    path('pelada/<int:pelada_id>/editar/', views.editar_pelada, name='editar_pelada'),
    path('pelada/<int:pelada_id>/excluir/', views.excluir_pelada, name='excluir_pelada'),
    path('pelada/<int:pelada_id>/salva/', views.salva_pelada, name='salva_pelada'),
]
