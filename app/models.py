from django.db import models
from django.utils.safestring import mark_safe
from django.utils import timezone

class PlataformaJogos(models.Model):
    cartao_imagem = models.ImageField(upload_to='jogos')
    nome_jogo = models.CharField(max_length=120)
    preco_jogo = models.FloatField()
    acesso = models.IntegerField(default=0)
    data_criacao = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return self.nome_jogo
    
    class Meta:
         verbose_name = 'Configuração Jogos Ajuste'
    
    @mark_safe
    def cartao_jogo(self):
          return f'<img width="80px" src="/media/{self.cartao_imagem}">'
