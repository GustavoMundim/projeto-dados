from typing import Any
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .models import PlataformaJogos
from django.urls import reverse
from django.http import HttpRequest, HttpResponse
# Create your views here.


class HomePage(TemplateView):
    template_name = 'homepage.html'
    
    
    def get(self, request, **kwargs):
        MeuCarrinho(request)
        context = self.get_context_data(**kwargs)
        context['active_page'] = 'homepage'
        self.consultar_id(request=request)
        context['carrinho'] = len(self.request.session['carrinho'])
        return self.render_to_response(context)
    
    def consultar_id(self, request):
        if 'None' in request.session['carrinho']:
            request.session['carrinho'].remove('None')
        else:
            pass
        

    def limpar_acesso(self):
        jogos = PlataformaJogos.objects.all()
        for game in jogos:
            game.acesso = 0
            game.save()
    
    


class MeuCarrinho:
    def __init__(self, request):
        self.session = request.session
        if not self.session.get('carrinho'):
            self.session['carrinho'] = []
            self.session.save()
    def add_carrinho(self, id):
        if id not in self.session['carrinho']:
            self.session['carrinho'].append(id) 
            self.session.save()   
        else:
            pass

    



class Shop(TemplateView):
    template_name = 'carrinho.html'

    @staticmethod
    def get_pagamentos():
        return ['Dinheiro', 'Boleto Bancário', 'Cartão de Crédito 💳', 'Cartão de Débito 💳', 'PIX ❖']
    


    def contexts(self, request, context, id):
            context['carrinho'] = len(request.session['carrinho'])
            context['pagamentos'] = self.get_pagamentos()
            context['id_do_jogo'] = PlataformaJogos.objects.get(id=id)
            return context

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        id = self.kwargs.get('id')
        meu_carrinho = MeuCarrinho(request)
        meu_carrinho.add_carrinho(id)
        context = self.contexts(request, context , id)
        context['carrinho_jogo'] = PlataformaJogos.objects.filter(id__in=request.session['carrinho'])
        context['preco_total_carrinho'] = sum(self.consultar_preco_total(request=request))
        return self.render_to_response(context)
    
   
    @staticmethod
    def consultar_preco_total(request):
        preco_total = []
        for id in request.session['carrinho']:
            consulta_preco = int(PlataformaJogos.objects.filter(id=id).values('preco_jogo').first()['preco_jogo'])
            preco_total.append(consulta_preco)
        return preco_total
    




        
    

    def metodo_pagamento(self, request):
        nome_usuario = request.POST.get('nome')
        sobrenome_usuario = request.POST.get('sobrenome')
        return nome_usuario, sobrenome_usuario

                 
    @staticmethod
    def contagem_acessos(jogos_carrinho):
         for jogo in jogos_carrinho:
            jogo.acesso +=1 
            jogo.save()
        
    


    def post(self, request, id):
        jogos_carrinho = PlataformaJogos.objects.filter(id__in=request.session['carrinho'])
        self.contagem_acessos(jogos_carrinho)
        request.session['carrinho'] = []
        request.session.save()
        return redirect('jogo:homepage')
    

class Games(TemplateView):
    template_name = 'jogos.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        MeuCarrinho(request)
        context['carrinho'] = len(request.session['carrinho'])
        context['all_games'] = PlataformaJogos.objects.all()
        context['active_page'] = 'jogos'
        return self.render_to_response(context)


class ShopPage(Shop, TemplateView):
    template_name = 'carrinho.html'

    def contexts(self, request, context):
            context['carrinho'] = len(request.session['carrinho'])
            context['pagamentos'] = self.get_pagamentos()
            return context


    def get(self, request, **kwargs):
       return super().get()
    
    def post(self, request):
         return super().post(request, id=None)
    

