# Importações necessárias do Django e outras bibliotecas
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, View
from django.http import HttpRequest, HttpResponse
from django.utils.decorators import method_decorator
from .api_yahoo import yahoo_finance_api  # Importa função de API externa
from django.urls import reverse
from django.contrib import auth
from django.contrib import messages  # Importa módulo de mensagens do Django
from django.contrib.messages import constants
from django.contrib.auth.decorators import login_required
from .models import Usuario as User  # Importa o modelo de usuário personalizado
from .models import CriarAnotacao  # Importa o modelo de anotação personalizado
import pandas as pd  # Importa Pandas para manipulação de dados

# Classe de visualização para a página inicial
class Home(TemplateView):
    template_name = 'dados.html'  # Define o template a ser renderizado

    # Método GET para a página inicial
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)  # Obtém o contexto da página

        # Chama a função da API externa para obter dados financeiros
        dados, estrutura, estrutura_original, data = yahoo_finance_api()

        # Personaliza os dados obtidos para exibir apenas o último dia de cada ativo
        dados_customizado = self.pegar_dados(estrutura_original, dados)

        # Adiciona as anotações existentes ao contexto
        context['anotacoes'] = CriarAnotacao.objects.all()
        context['estruturas'] = dados_customizado  # Adiciona os dados personalizados ao contexto

        return self.render_to_response(context)  # Renderiza a página com o contexto fornecido
    
    # Método estático para personalizar os dados obtidos da API
    @staticmethod
    def pegar_dados(estrutura_original, dados):
        adicionar_ativo = {}  # Dicionário para armazenar dados personalizados

        # Itera sobre os ativos originais e os dados obtidos da API
        for ativo in estrutura_original:
            for dado in dados:
                if dado['Ativos'] == ativo:  # Verifica correspondência do ativo
                    # Adiciona dados relevantes ao dicionário personalizado
                    adicionar_ativo[ativo] = {
                        'Data': dado['Data'],
                        'Abertura': dado['Abertura'],
                        'Alta': dado['Alta'],
                        'Baixa': dado['Baixa'],
                        'Fechamento': dado['Fechamento']
                    }
        return adicionar_ativo  # Retorna o dicionário personalizado de dados


# Classe de visualização para o cadastro de usuários
class CadastroUsuario(TemplateView):
    template_name = 'login.html'  # Define o template a ser renderizado

    # Método GET para a página de cadastro de usuários
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)  # Obtém o contexto da página
        context['login_requirement'] = 'cadastro'  # Define o requisito de login para 'cadastro'
        return self.render_to_response(context)  # Renderiza a página com o contexto fornecido

    # Método POST para processar o cadastro de usuários
    def post(self, request):
        # Obtém os dados do formulário de cadastro de usuário
        self.usuario = request.POST.get('usuario')
        self.senha = request.POST.get('senha')
        self.email = request.POST.get('email_usuario')
        return self.cadastro_usuario()  # Chama o método para processar o cadastro de usuário

    # Método para realizar o cadastro de usuário
    def cadastro_usuario(self):
        # Verifica se algum campo necessário está em branco
        if len(self.usuario.strip()) == 0 or len(self.senha.strip()) == 0 or len(self.email.strip()) == 0:
            messages.add_message(self.request, constants.WARNING, 'Você não pode deixar campos em branco')
            return redirect('projeto:cadastro')  # Redireciona de volta para a página de cadastro

        # Verifica se a senha fornecida tem pelo menos 8 caracteres
        if len(self.senha) < 8:
            messages.add_message(self.request, constants.WARNING, 'A sua senha deve ter no mínimo 8 caracteres')
            return redirect('projeto:cadastro')  # Redireciona de volta para a página de cadastro

        # Verifica se o email fornecido é válido 
        if len(self.email) < 7:
            messages.add_message(self.request, constants.WARNING, 'Digite um email válido')
            return redirect('projeto:cadastro')  # Redireciona de volta para a página de cadastro

        # Verifica se já existe um usuário com o mesmo nome de usuário
        if User.objects.filter(username=self.usuario).exists():
            messages.add_message(self.request, constants.ERROR, 'Já existe um usuário cadastrado com esse nome!')
            return redirect('projeto:cadastro')  # Redireciona de volta para a página de cadastro

        try:
            # Cria um novo usuário no sistema
            self.user = User.objects.create_user(username=self.usuario, password=self.senha, email=self.email)
            self.user.save()
            messages.add_message(self.request, constants.SUCCESS, 'Cadastro realizado com sucesso!')
            return redirect('projeto:login')  # Redireciona para a página de login após o cadastro

        except:
            return HttpResponse('Erro interno')  # Retorna uma resposta de erro interno se houver falha


# Classe de visualização para a página de login
class Login(TemplateView):
    template_name = 'login.html'  # Define o template a ser renderizado

    # Método GET para a página de login
    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)  # Obtém o contexto da página
        context['login_requirement'] = 'login'  # Define o requisito de login para 'login'
        return self.render_to_response(context)  # Renderiza a página com o contexto fornecido

    # Método POST para processar a tentativa de login
    def post(self, request):
        # Verifica se o usuário já está autenticado, redireciona para a página do usuário
        if request.user.is_authenticated:
            return redirect('projeto:usuario')

        # Obtém os dados do formulário de login
        self.usuario = request.POST.get('usuario')
        self.senha = request.POST.get('senha')
        self.email = request.POST.get('email_usuario')

        # Autentica o usuário com os dados fornecidos
        self.user = auth.authenticate(request, username=self.usuario, password=self.senha, email=self.email)
        return self.verificar_login(self.usuario)  # Chama o método para verificar o login

    # Método para verificar e processar o login do usuário
    def verificar_login(self, usuario):
        # Se o usuário não estiver autenticado, exibe uma mensagem de erro e redireciona para a página de login
        if not self.user:
            messages.add_message(self.request, constants.ERROR, 'O nome de usuário está incorreto ou a senha está incorreta')
            return redirect('projeto:login')

        auth.login(self.request, self.user)  # Realiza o login do usuário
        return redirect('projeto:usuario')  # Redireciona para a página do usuário após o login


# Classe de visualização para exibir gráficos financeiros
class Grafico(Home, TemplateView):
    template_name = 'grafico.html'  # Define o template a ser renderizado

    # Método para filtrar dados financeiros para um gráfico específico
    def filtro(self, data, estrutura, id):
        nome_empresa = estrutura[id - 1]  # Obtém o nome da empresa com base no ID
        dados_filtrados = data[data['Ativos'] == nome_empresa]  # Filtra os dados para a empresa específica
        datas = dados_filtrados['Data'].values
        aberturas = dados_filtrados['Abertura'].values
        altas = dados_filtrados['Alta'].values
        baixas = dados_filtrados['Baixa'].values
        fechamentos = dados_filtrados['Fechamento'].values
        # Retorna um dicionário com os dados filtrados para renderização no template
        return {'Data': datas, 'Aberturas': aberturas, 'Altas': altas, 'Baixas': baixas, 'Fechamento': fechamentos, 'Empresa': nome_empresa}

    # Método GET para renderizar a página do gráfico
    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)  # Obtém o contexto da página
        pegar_id = kwargs.get('id_grafico')
        
        # Obtém a anotação para o ID do gráfico
        anotacao = self.receber_anotacao(pegar_id)
        
        # Obtém os dados da Yahoo Finance API
        dados, estrutura, estrutura_original, data = yahoo_finance_api()
        
        # Filtra os dados conforme necessário
        valores_filtrados = self.filtro(data, estrutura_original, pegar_id)
        
        # Personaliza os dados conforme necessário
        dados_customizado = self.pegar_dados(estrutura_original, dados)
        context = {
            'ativos': estrutura,
            'estrutura': dados_customizado,
            'dados_ativos': ['Abertura', 'Baixa', 'Alta', 'Fechamento'],
            'dados_filtrados': valores_filtrados,
            'anotacao': anotacao,
            'id_anotacao': pegar_id
        }
        return self.render_to_response(context)


    def receber_anotacao(self, id):
            return CriarAnotacao.objects.filter(id_card=id)

def anotacao_do_usuario(request, counter):
    try:
        pegar_anotacao = request.POST.get('anotacao-usuario')
        if request.POST.get('anotacao-usuario-grafico'):
            pegar_anotacao = request.POST.get('anotacao-usuario-grafico')
            print(pegar_anotacao, counter)
        criar_anotacao = CriarAnotacao(anotacao=pegar_anotacao, usuario=request.user.username, id_card=counter)
        criar_anotacao.save()
    except:
        pass
    return redirect('projeto:home')


def deletar_anotacao(request, comentario_id):
    try:
        pegar_anotacao = get_object_or_404(CriarAnotacao, id=comentario_id)
        pegar_anotacao.delete()
        return redirect('projeto:home')
    except:
        return redirect('projeto:home')




def logout(request):
    auth.logout(request)
    return redirect('projeto:login')



@method_decorator(login_required(login_url='projeto:login'), name='dispatch')
class PlataformaUsuario(TemplateView):
    template_name = 'plataforma.html'

    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        #  VERIFICAR SE EXISTE UMA SESSION
        if 'alterar_imagem' in request.session:
            context['alterar_imagem'] = request.session['alterar_imagem']
        return self.render_to_response(context)
    
    def post(self, request, **kwargs):
        request.session['alterar_imagem'] = True
        return redirect('projeto:usuario')



class AlterarImagem(View):
    pass


    def get(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def post(self, request, **kwargs):
        request.session['alterar_imagem'] = False
        usuario = request.user
        try:
            usuario.foto_usuario = request.FILES['imagem_alterada_usuario']
            usuario.save()
            return redirect('projeto:usuario')
        except:
            return redirect('projeto:usuario')




            



def back_plataforma(request):
    if 'alterar_imagem' in request.session:
        del request.session['alterar_imagem']
    return redirect('projeto:usuario')

    # return render(request, 'plataforma.html')


