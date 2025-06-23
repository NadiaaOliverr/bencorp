# Olá!

Este repositório implementa uma solução para disponibilizar endpoints de um CRUD de vendas, com filtros, paginação e operações de ETL. O objetivo é permitir o cadastro individual de vendas, processamento em lote via arquivos CSV, persistência dos dados em banco relacional e exportação em formatos CSV ou JSON. Veja uma **demonstração** por **vídeo** acessando [este link](https://youtu.be/UjVPZiTI6rM).

![](https://i.imgur.com/vBhG2Ve.png)

*Acesse a API na nuvem por [essa URL](https://bencorp-api-796987028771.southamerica-east1.run.app/vendas) e aplique os filtros ou faça `posts` conforme necessário.*

## 📚 Índice
- [🏗️ Arquitetura](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#%EF%B8%8F-arquitetura)
- [🗂️ Endpoints disponíveis](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#%EF%B8%8F-endpoints-dispon%C3%ADveis)
- [🛠️ Decisões de implementação](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#%EF%B8%8F-decis%C3%B5es-de-implementa%C3%A7%C3%A3o)
- [🚀 Funcionalidades extras que foram implementadas](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#-funcionalidades-extras-que-foram-implementadas)
- [⚡ Como executar](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#-como-executar)
- [💡 Ideias futuras](https://github.com/NadiaaOliverr/bencorp?tab=readme-ov-file#-ideias-futuras)

### 🏗️ Arquitetura

A solução foi estruturada para rodar **tanto em ambiente local quanto em produção na nuvem**, mantendo a paridade de configuração via Docker e variáveis de ambiente.

![](https://i.imgur.com/H9Qd1b8.png)

### 🗂️ Endpoints disponíveis

| Endpoint | Método | Descrição | Parâmetros |
| -------- | ------ | --------- | ----------- |
| `/vendas/` | `GET` | Lista vendas com filtros, ordenação e paginação. | `pagina`, `tamanho_pagina`, `categoria`, `vendedor`, `ordenar_por`, `ordem` |
| `/vendas/{id}` | `GET` | Retorna detalhes de uma venda específica. | `id` |
| `/vendas/` | `POST` | Cria uma nova venda. | Body: JSON |
| `/vendas/{id}` | `PUT` | Atualiza uma venda existente. | `id`, Body: JSON |
| `/vendas/{id}` | `DELETE` | Remove uma venda. | `id` |
| `/etl/importar-csv` | `POST` | Importa dados em lote via arquivo CSV. | Arquivo: CSV |
| `/etl/exportar-dados` | `GET` | Exporta vendas em CSV ou JSON, com filtros. | `formato`, `categoria`, `vendedor` |
| `/etl/relatorio-mensal` | `GET` | Gera relatório agregado de vendas por mês. | `mes` (YYYY-MM) |
| `/etl/top-vendedores` | `GET` | Lista os top N vendedores de um período. | `mes`, `top` |

### 🛠️ Decisões de implementação

Durante o desenvolvimento deste projeto, tomei alguamas decisões além dos requisitos obrigatórios, com o objetivo de melhorar a robustez, a segurança dos dados e a clareza da arquitetura. Abaixo detalho cada uma delas e o porquê de ter seguido por esse caminho.

- **Coluna `created_at`**  
  
  Adicionei uma coluna `created_at` na tabela `vendas` para registrar a data e hora em que cada registro é inserido. Isso foi feito pensando em  rastreabilidade dos dados.

- **Validações adicionais**  
  
  Para além das validações mínimas, implementei:
  - `validar_categoria_permitida` e `validar_regiao_permitida`: restringe as categorias a um conjunto fechado que foi pré-definido, evitando erros de digitação do usuário.
  - `validar_texto_sanitizado`: impede caracteres especiais indesejados em campos de texto, como emojis por exemplo, reduzindo risco de dados sujos ou ataques de injeção.
  - Verificação de campos obrigatórios e não vazios para todas as strings.
  - Validação de tamanho máximo do nome do produto (100 caracteres).

- **Testes adicionais:**
 
  Além dos testes mínimos, desenvolvi casos específicos para validar:
  - Filtros por categoria e vendedor combinados com paginação.
  - Exportação de formatos e validação de formatos inválidos.
  - Exclusão (delete) de vendas.
  - Geração do relatório de top vendedores.

- **Filtros e ordenações extras na listagem de vendas**
  
  O endpoint `/vendas/` foi ampliado para aceitar filtros dinâmicos por:
  - Categoria (`categoria`)
  - Vendedor (`vendedor`)
  - Ordenação por campo específico (`ordenar_por`)
  - Direção da ordenação (`ordem` asc/desc)
  - Paginação com parâmetros de página e tamanho de página.

- **Estrutura de arquivos**
  
  Para além dos arquivos sugeridos na estrutura, foi criado:
  - Pasta `routes`: separa rotas de vendas e ETL.
  - Arquivo `schemas`: define os modelos de entrada e saída usando `Pydantic`.
  - Arquivo `validators`: centraliza todas as regras de validação de dados.
  - Arquivo `populate_csv`: foi criado para popular com 100 dados inicias bons e ruins para tratamento do ETL e inserção no banco via upload de arquivo.


### 🚀 Funcionalidades extras que foram implementadas

- **Filtros adicionais na exportação de dados**  
  Foi incluída a possibilidade de exportar os dados de vendas em **CSV ou JSON**, aplicando filtros dinâmicos por **categoria** e **vendedor**, através da rota `/etl/exportar-dados`. Isso permite extrair subconjuntos de dados específicos. Exemplo de rota: `localhost:8080/etl/exportar-dados?formato=csv&categoria=Eletrônicos`

  ![](https://i.imgur.com/SLEzkHf.png)

- **Filtros dinâmicos na listagem de vendas**  
  A rota `/vendas/` suporta filtros por **categoria** e **vendedor**, além de o**ordenação por campo, e paginação**.  Exemplo de rota: `localhost:8080/vendas?pagina=1&tamanho_pagina=5&categoria=Eletrônicos&vendedor=Dom%20Brito&ordenar_por=preco&ordem=asc`

  ![](https://i.imgur.com/dLE18BW.png)

- **Relatório de Top N Vendedores por mês**  
  Foi implementado o relatório de **Top N Vendedores**, detalhando o total vendido por cada vendedor, discriminado por categoria de produto. Isso é útil para análises de performance individual dado um período de tempo. Exemplo de rota: `localhost:8080/etl/top-vendedores?mes=2025-06&top=4`

  ![](https://i.imgur.com/ldY50RE.png)

- **Containerização e deploy automatizado**

    Toda a stack é orquestrada via `docker-compose` para facilitar o setup local, incluindo a API FastAPI, o banco de dados PostgreSQL e o PgAdmin. 

    Para produção, utilizei o **Google Cloud Run** para hospedar a aplicação de forma serverless. O fluxo de entrega contínua (CI/CD) foi configurado usando **GitHub Actions**, que realiza o build da imagem Docker, armazena no **Artifact Registry** e executa o deploy no Cloud Run de forma automatizada a cada push na branch principal.

    O banco de dados em produção utiliza uma instância do **Google Cloud SQL (PostgreSQL)**, provisionada em um ambiente de sandbox para fins de demonstração, com custo estimado de aproximadamente **USD 0,12/hora** em uma configuração de máquina pequena, com 2 GB de armazenamento. Para cenários de produção real, seria necessário ajustar o tamanho da máquina, e escolher regiões mais econômicas para otimização de custo e latência.

    ![](https://i.imgur.com/AYCeQol.png)

### ⚡ Como executar

Para rodar o projeto localmente, é necessário ter **[Docker](https://docs.docker.com/get-started/introduction/get-docker-desktop/)** e **[Git](https://git-scm.com/downloads)** instalados na máquina.

**Passo 1: Clonar o repositório** 
```
git clone git@github.com:NadiaaOliverr/bencorp.git
```
```
cd bencorp
```
**Passo 2: Configurar variáveis de ambiente** 

Crie um arquivo **.env** dentro da pasta `bencorp` conforme o arquivo `.env.example` e ajuste as credenciais:

cp .env.example .env

nano .env


```
# VARIÁVEIS DO POSTGRESQL
POSTGRES_DB=NOME_DO_BANCO               
POSTGRES_USER=SEU_NOME_DE_USUARIO
POSTGRES_PASSWORD=SUA_SENHA

# STRING DE CONEXÃO PARA SQLALCHEMY
DATABASE_URL=postgresql+psycopg2://SEU_NOME_DE_USUARIO:SUA_SENHA@db:5432/NOME_DO_BANCO

# VARIÁVEIS DO PGADMIN
PGADMIN_DEFAULT_EMAIL=SEU_EMAIL@EXEMPLO.COM
PGADMIN_DEFAULT_PASSWORD=SUA_SENHA_PGADMIN
```
**Passo 3: Subir os containers** 

Com o Docker em execução, suba os serviços:
```
docker-compose up --build
```
Isso irá criar os containers da API, do banco de dados e do PgAdmin, como mostro a seguir:

![Banco pronto](https://i.imgur.com/Dnt0RT2.png)
**Passo 4: Acessar o PgAdmin** 

- Acesse: `http://localhost:5050/browser/`
- Faça login usando as credenciais definidas no `.env`
- Crie um **Servidor** e conecte ao banco PostgreSQL:
  - Host: `postgres_db`
  - Porta: `5432`
  - Usuário e senha: conforme `.env`

**Passo 5: Popular o banco com dados de teste** 

Abra um terminal dentro da pasta `bencorp` e execute o script para popular o banco:
```
docker-compose exec api bash
```
```
python -m scripts.populate_db
```
**Passo 6: Acessar as rotas** 

- Documentação: `http://localhost:8080/docs`
- Para testar os endpoints do tipo `POST`, `PUT` ou `DELETE`, você pode [importar o JSON de rotas](https://github.com/NadiaaOliverr/bencorp/blob/main/endpoints-insomnia-postman.json) no Insomnia ou Postman para testar.

### 💡 Ideias futuras

- Implementar novos endpoints para métricas de comparativos de vendas ano a ano, projeções de demanda e relatórios por região.

- Criar uma aplicação Frontend para exibir dashboards em tempo real ou consumir a API no Power BI por exemplo.

- Adicionar um sistema de alertas para disparar e-mails ou mensagens quando certas metas de vendas forem atingidas.

- Incorporar IA generativa ou modelos LLM para gerar análises descritivas ou insights sobre as vendas, além de prever tendências futuras com base no histórico, podendo expor essas informações por novos endpoints.


#### Obrigada por ler até aqui! Fico à disposição para dúvidas, feedbacks ou sugestões.
