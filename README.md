# Travel API ✈️

API para busca simplificada de voos desenvolvida com **Python** e **FastAPI**.

Este projeto foi desenvolvido como trabalho final da disciplina **Python para IA (PYAI)** da Especialização em Inteligência Artificial Generativa da **Universidade Federal do Paraná (UFPR)**.

A aplicação recebe um aeroporto de origem, um aeroporto de destino e uma data de viagem, consulta dados de voos por meio da [SerpApi — Google Flights API](https://serpapi.com/google-flights-api) e retorna uma resposta JSON simplificada com até cinco opções ordenadas pelo menor preço.

## Funcionamento

O fluxo da aplicação é:

```text
Origem + destino + data
          ↓
       FastAPI
          ↓
       SerpApi
          ↓
    Google Flights
          ↓
   JSON de resultados
          ↓
Processamento em Python
          ↓
5 opções ordenadas por preço
```

A API externa retorna uma estrutura relativamente extensa. A aplicação processa esses dados em Python e devolve apenas as informações relevantes para o usuário.

## Tecnologias utilizadas

- Python 3.12
- FastAPI
- Requests
- Uvicorn
- Truststore
- Conda
- Docker
- [SerpApi — Google Flights API](https://serpapi.com/google-flights-api)
- Oracle Cloud

## Estrutura do projeto

```text
genaiufpr-fastapi/
├── main.py
├── environment.yml
├── Dockerfile
├── README.md
└── .gitignore
```

## Endpoint principal

### `GET /voos`

Realiza uma busca de voos somente de ida.

Parâmetros:

| Parâmetro | Descrição | Exemplo |
|---|---|---|
| `origem` | Código IATA do aeroporto de origem | `CWB` |
| `destino` | Código IATA do aeroporto de destino | `GIG` |
| `data` | Data da viagem no formato `AAAA-MM-DD` | `2026-08-28` |

Exemplo:

```text
GET /voos?origem=CWB&destino=GIG&data=2026-08-28
```

A API converte automaticamente os códigos IATA para letras maiúsculas.

### Exemplo de resposta

```json
{
  "origem": "CWB",
  "destino": "GIG",
  "data": "2026-08-28",
  "quantidade": 5,
  "voos": [
    {
      "companhia": "Azul",
      "saida": "2026-08-28 07:30",
      "chegada": "2026-08-28 09:00",
      "duracao_minutos": 90,
      "escalas": 0,
      "preco": 969,
      "moeda": "BRL"
    }
  ]
}
```

Os valores apresentados acima são apenas um exemplo. Preços, horários e opções disponíveis dependem dos resultados obtidos no momento da consulta.

## Processamento realizado pela aplicação

A aplicação:

1. recebe os parâmetros pela FastAPI;
2. consulta a SerpApi utilizando o mecanismo Google Flights;
3. combina as listas de voos retornadas pela API externa;
4. percorre as ofertas e extrai apenas os campos necessários;
5. calcula o número de escalas a partir da quantidade de trechos;
6. ordena os resultados pelo preço;
7. retorna até cinco opções.

Dessa forma, a API não funciona apenas como um redirecionamento da API externa, mas realiza tratamento e simplificação dos dados utilizando Python.

## Configuração da SerpApi

É necessário possuir uma chave da [SerpApi](https://serpapi.com/).

Por segurança, a chave **não deve ser inserida diretamente no código ou enviada ao GitHub**. A aplicação lê a chave por meio da variável de ambiente:

```text
SERPAPI_API_KEY
```

No PowerShell:

```powershell
$env:SERPAPI_API_KEY="SUA_CHAVE"
```

No Linux:

```bash
export SERPAPI_API_KEY="SUA_CHAVE"
```

## Execução local com Conda

Clone o repositório:

```bash
git clone https://github.com/mrossetto47/genaiufpr-fastapi.git
cd genaiufpr-fastapi
```

Crie o ambiente a partir do arquivo `environment.yml`:

```bash
conda env create -f environment.yml
```

Ative o ambiente:

```bash
conda activate travel_api
```

Configure a variável `SERPAPI_API_KEY` e execute a aplicação:

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

```text
http://127.0.0.1:8000
```

A documentação interativa gerada automaticamente pelo FastAPI pode ser acessada em:

```text
http://127.0.0.1:8000/docs
```

## Execução com Docker

Construa a imagem:

```bash
docker build -t travel-api .
```

No Linux, após definir a variável `SERPAPI_API_KEY`, execute:

```bash
docker run --name travel-api-container \
  -e SERPAPI_API_KEY="$SERPAPI_API_KEY" \
  -p 8000:8000 \
  travel-api
```

A aplicação estará disponível na porta `8000`.

## Deploy

O projeto foi testado em uma **VM Ubuntu na Oracle Cloud**.

O fluxo utilizado para o deploy foi:

```text
GitHub
   ↓
clone do repositório na VM
   ↓
docker build
   ↓
docker run
   ↓
porta 8000
   ↓
acesso pelo IP público
```

Foram testados remotamente tanto o endpoint `/voos` quanto a documentação automática `/docs`.

## Escopo do MVP

A versão atual considera:

- viagem somente de ida;
- um aeroporto de origem;
- um aeroporto de destino;
- uma data de partida;
- preços em BRL;
- até cinco opções ordenadas pelo menor preço.

Funcionalidades como ida e volta, múltiplos passageiros, filtros adicionais, reserva de passagens e interface gráfica não fazem parte do MVP.

## Possíveis evoluções

Uma evolução futura prevista para o projeto é o **MatchTrip**: integração entre calendário de partidas de futebol e busca de viagens.

A ideia é permitir que o usuário informe um time, identificar uma futura partida fora de casa e utilizar automaticamente a cidade e a data do jogo para pesquisar opções de viagem.

Essa funcionalidade não faz parte da versão atual do projeto.

## Autor

**Matheus Rossetto**

Projeto desenvolvido para a disciplina **Python para IA (PYAI)** — Especialização em Inteligência Artificial Generativa — **UFPR**.