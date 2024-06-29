
from .models import PlataformaJogos

def jogo_adicionado_recente(request):
    lista_jogos = PlataformaJogos.objects.all().order_by('-data_criacao')[0:10]
    return {"lista_jogos_adicionados_recentes": lista_jogos}


def jogos_mais_acessados(request):
    lista_jogos = PlataformaJogos.objects.all().order_by('-acesso')[0:10]
    return {'lista_jogos_acessados': lista_jogos}
