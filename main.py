# =============================================================================
# SCRIPT: main.py
# OBJETIVO: Implementar a API de busca de voos utilizando FastAPI.
#
# CONTEXTO:
# Este script faz parte do projeto final da disciplina Python para IA (PYAI)
# da Especialização em Inteligência Artificial Generativa da UFPR.
# A aplicação recebe informações de origem, destino e data da viagem e
# realiza consultas a uma API externa de voos.
#
# ENTRADAS:
# - Código IATA do aeroporto de origem.
# - Código IATA do aeroporto de destino.
# - Data da viagem.
#
# SAÍDAS:
# - Resposta JSON com informações simplificadas sobre os voos encontrados.
#
# AUTOR: Matheus Rossetto
# DATA DE CRIAÇÃO: 12/08/2026
#
# HISTÓRICO DE ALTERAÇÕES:
# - 12/08/2026: Criação da estrutura inicial da API com FastAPI.
# - 13/08/2026: Integração com a SerpApi e processamento das opções de voo.
# =============================================================================



#------------------------------------------------------------------------------
# Importações de bibliotecas necessárias para o funcionamento da API
#------------------------------------------------------------------------------
import os # Biblioteca para interações com o sistema operacional
import truststore # Biblioteca para gerenciamento de certificados de segurança

truststore.inject_into_ssl() # Faz o Python utilizar os certificados confiáveis do sistema operacional nas conexões SSL

import requests # Biblioteca para realizar requisições HTTP, para interagir com APIs externas

from fastapi import FastAPI # Biblioteca FastAPI para criar a API própria




#------------------------------------------------------------------------------
# Criação da instância da aplicação FastAPI
#------------------------------------------------------------------------------
SERPAPI_URL = "https://serpapi.com/search" # URL base da API externa de busca de voos (SerpApi) que será utilizada para consultas

app = FastAPI(title="Travel API") # Criando a instância da aplicação FastAPI com o nome "Travel API"


# Definindo a rota raiz ("/") da API, que será acessada via método GET
# Retorna uma mensagem de confirmação de que a API está funcionando corretamente
@app.get("/") 
def home():
    return {"mensagem": "Travel API funcionando"} 



# Definindo a rota "/voos" da API, que será acessada via método GET
# Recebe parâmetros de consulta: origem, destino e data
@app.get("/voos")
def buscar_voos(origem: str, destino: str, data: str):

    api_key = os.getenv("SERPAPI_API_KEY") # Obtendo a chave da API do SerpApi a partir das variáveis de ambiente do sistema operacional

    if not api_key:
        raise RuntimeError("Variável de ambiente SERPAPI_API_KEY não definida.") # Verifica se a chave da API foi definida; caso contrário, lança um erro

    # Parâmetros que serão enviados na requisição para a API externa
    params = {
        "engine": "google_flights", # Define o mecanismo de busca a ser utilizado na API externa (neste caso, Google Flights)
        "departure_id": origem.upper(), # Código IATA do aeroporto de origem, convertido para maiúsculas
        "arrival_id": destino.upper(), # Código IATA do aeroporto de destino, convertido para maiúsculas
        "outbound_date": data, # Data da viagem
        "type": 2, # Tipo de busca (2 indica uma viagem somente de ida)
        "gl": "br", # Define o país de origem da busca (Brasil)
        "hl": "pt", # Define o idioma da resposta (Português)
        "currency": "BRL", # Define a moeda da resposta (Real Brasileiro)
        "api_key": api_key # Chave da API do SerpApi para autenticação da requisição
    }




#------------------------------------------------------------------------------
# Realizando a requisição à API externa
#------------------------------------------------------------------------------
    response = requests.get(
        SERPAPI_URL, # URL da API externa de busca de voos
        params=params, # Parâmetros da requisição (origem, destino, data, etc.)
        timeout=30 # Define o tempo máximo de espera para a resposta da API externa (30 segundos)
    )

    response.raise_for_status() # Lança uma exceção caso a resposta da API externa indique um erro (códigos de status HTTP 4xx ou 5xx)



#------------------------------------------------------------------------------
# Recebendo e processando o JSON de resposta da API externa
#------------------------------------------------------------------------------
    data_serpapi = response.json() # Converte a resposta da API externa para um objeto JSON (dicionário Python)

    # Extraindo informações relevantes do JSON de resposta da API externa
    best_flights = data_serpapi.get("best_flights", []) # Obtendo a lista de melhores voos encontrados na resposta da API externa (ou uma lista vazia caso não haja resultados)
    other_flights = data_serpapi.get("other_flights", []) # Obtendo a lista de outros voos encontrados na resposta da API externa (ou uma lista vazia caso não haja resultados)

    # Combinando as listas de melhores voos e outros voos em uma única lista
    todos_voos = best_flights + other_flights

    # Criando uma lista para armazenar informações simplificadas dos voos encontrados
    voos_simplificados = []

    # Iterando sobre cada voo encontrado na lista de todos os voos
    for voo in todos_voos: 
        trechos = voo["flights"] # Obtendo a lista de trechos do voo atual

    # Criando um dicionário com informações simplificadas do voo atual
        voo_simplificado = {
            "companhia": trechos[0]["airline"], # Obtendo o nome da companhia aérea do primeiro trecho do voo
            "saida": trechos[0]["departure_airport"]["time"], # Obtendo o horário de saída do primeiro trecho do voo
            "chegada": trechos[-1]["arrival_airport"]["time"], # Obtendo o horário de chegada do último trecho do voo
            "duracao_minutos": voo["total_duration"], # Obtendo a duração total do voo em minutos
            "escalas": len(trechos) - 1, # Calculando o número de escalas do voo (número de trechos menos 1)
            "preco": voo["price"], # Obtendo o preço do voo
            "moeda": "BRL" # Definindo a moeda do preço como Real Brasileiro (BRL)
        }

       # Adicionando o dicionário com informações simplificadas do voo atual à lista de voos simplificados
        voos_simplificados.append(voo_simplificado)

    # Ordena todos os voos do menor para o maior preço
    voos_simplificados.sort(key=lambda voo: voo["preco"])

    # Mantém somente os cinco mais baratos
    voos_simplificados = voos_simplificados[:5]




#------------------------------------------------------------------------------
# Retornando a lista de voos simplificados como resposta da API 
#------------------------------------------------------------------------------
    return {
        "origem": origem.upper(), # Convertendo o código IATA do aeroporto de origem para maiúsculas
        "destino": destino.upper(), # Convertendo o código IATA do aeroporto de destino para maiúsculas
        "data": data, # Data da viagem
        "quantidade": len(voos_simplificados), # Quantidade de voos encontrados (limitada aos 5 mais baratos)
        "voos": voos_simplificados # Retornando a lista de voos simplificados como resposta da API
    } 