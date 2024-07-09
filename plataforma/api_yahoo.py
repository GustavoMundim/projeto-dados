import json
import yfinance as yf
import pandas as pd


# ESTRUTURA DE ATIVOS A SEREM ANALISADOS
def yahoo_finance_api():
    estrutura_ativos = {'Ativo': [
    'PETR3.SA',
    'GOLL4.SA',
    'AZUL4.SA',
    'LREN3.SA',
    'BBAS3.SA',
    'MGLU3.SA',
    'AMZN',
    'CIEL3.SA'
]}

    ativos = {}

    # LOOP PARA OBTER DADOS HISTÓRICOS DE CADA ATIVO
    for estrutura in estrutura_ativos['Ativo']:
        
        # CRIANDO UM OBJETO TICKER PARA CADA ATIVO 
        ativo_yf = yf.Ticker(estrutura)
        # OBTENDO O HISTÓRICO DE PREÇOS DOS ULTIMOS 5 DIAS
        historico_yf = ativo_yf.history(period='5d')
        
        # SELECIONADO AS COLUNAS OPEN (ABERTURA), HIGH (ALTA), LOW (BAIXA), CLOSE (FECHAMENTO)
        historico_personalizado = historico_yf[['Open', 'High', 'Low', 'Close']]
        
        # ARMAZENANDO OS DADOS A ESTRUTURA
        ativos[estrutura] = historico_personalizado
        
        
    #  CONCATENANDO OS VALORES DE TODOS OS ATIVOS EM UM UNICO DATAFRAME
    df_yf = pd.concat(ativos)
    df_yf.reset_index(inplace=True)


    # RENOMEANDO COLUNAS PARA PORTUGUES
    df_yf = df_yf.rename(columns={'level_0': 'Ativos','Date': 'Data', 'Open': 'Abertura', 'High': 'Alta', 'Low': 'Baixa', 'Close': 'Fechamento'})
    pegar_data = df_yf['Data']
    df_yf['Data'] = pd.to_datetime(df_yf['Data'], utc=True).dt.tz_localize(None).dt.floor('d').dt.strftime('%d/%m/%Y')
    # ativos_formatados = df_yf['Ativos'].str.replace('.', '0').str.replace('^','').str.strip()
    database_nova = df_yf.groupby(['Ativos', 'Data'], as_index=False).sum(numeric_only=True)    
    database_nova = database_nova.round(4)
    estruturas_formatadas = database_nova.index.values
    api = database_nova.to_json(orient='records')
    dados = json.loads(api)
    ativos = database_nova['Ativos'].unique()

    return dados, ativos, estrutura_ativos['Ativo'], database_nova
 



