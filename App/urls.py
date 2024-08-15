from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('about/', views.about, name='About'),
    path('recetas/', views.recetas_list, name='recetas_list'),
    path('publicar_receta', views.publicar_receta, name='publicar_receta'),
    path('editar_receta/<int:receta_id>/', views.editar_receta, name='editar_receta'),
    path('pages/<int:receta_id>/', views.receta_detail, name='receta_detail'),
    path('borrar_receta/<int:receta_id>/', views.borrar_receta, name='borrar_receta')
]