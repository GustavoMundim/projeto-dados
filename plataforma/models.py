from django.db import models
from django.contrib.auth.models import AbstractUser





class CriarAnotacao(models.Model):
    anotacao = models.TextField(max_length=900, verbose_name='Anotação')
    usuario = models.CharField(max_length=50, verbose_name='Nome do Usuário')
    id_card = models.IntegerField(blank=True, verbose_name='ID Anotação', default=0)

    class Meta:
        verbose_name = 'Anotação de Usuário'

    def __str__(self):
        return self.usuario

class Usuario(AbstractUser):
    foto_usuario = models.ImageField(upload_to='perfil', verbose_name='Foto do Usuário', blank=True)
    nivel = models.IntegerField(default=0)
    