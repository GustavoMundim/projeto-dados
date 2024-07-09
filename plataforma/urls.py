from django.urls import path
from . import views


app_name = 'projeto'

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('cadastro/', views.CadastroUsuario.as_view(), name='cadastro'),
    path('login/', views.Login.as_view(), name='login'),
    path('usuario/', views.plataforma, name='usuario'),
    path('logout', views.logout, name='logout'),
    path('note/<int:counter>', views.anotacao_do_usuario, name='note'),
    path("delete/<int:comentario_id>", views.deletar_anotacao, name='delete'),
    path('grafico/<int:id_grafico>', views.Grafico.as_view(), name='grafico')
]