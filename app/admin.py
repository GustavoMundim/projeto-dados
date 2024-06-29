from django.contrib import admin
from .models import PlataformaJogos


@admin.register(PlataformaJogos)
class PlataformaView(admin.ModelAdmin):
    list_display = ('cartao_jogo', 'nome_jogo', 'preco_jogo')
    list_editable = ('preco_jogo',)


