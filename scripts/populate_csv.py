import pandas as pd
import os
from faker import Faker
from random import choice, randint, uniform
from datetime import datetime, timedelta


def seed_dados_csv():

    fake = Faker('pt_BR')
    vendedores = [fake.name() for _ in range(10)]
    regioes = ["Norte", "Sul", "Sudeste", "Centro-Oeste", "Nordeste"]
    produtos = {
        "Notebook Dell Inspiron": "Eletrônicos",
        "Smartphone Samsung Galaxy": "Eletrônicos",
        "Fone de Ouvido JBL": "Eletrônicos",
        "Monitor LG UltraWide": "Eletrônicos",
        "Headset HyperX Cloud": "Eletrônicos",
        "Camiseta Adidas": "Roupas",
        "Calça Jeans Levi's": "Roupas",
        "Jaqueta Nike Sportswear": "Roupas",
        "Tênis Puma Runner": "Roupas",
        "Vestido Zara Floral": "Roupas",
        "Sofá Retrátil 3 Lugares": "Casa",
        "Mesa de Jantar 6 Cadeiras": "Casa",
        "Cama Box Casal Ortobom": "Casa",
        "Armário Cozinha Itatiaia": "Casa",
        "Liquidificador Philips Walita": "Casa",
        "Bola de Futebol Nike": "Esportes",
        "Raquete de Tênis Wilson": "Esportes",
        "Bicicleta Caloi 29": "Esportes",
        "Livro Python Avançado": "Livros",
        "Livro Clean Code": "Livros",
    }

    return vendedores, regioes, produtos

def seed_dados_ruins():

    vendas = []

    vendas.append(["Notebook Dell Inspiron", "Eletrônicos", -1500.00, 2, datetime.today().date(), "João da Silva", "Sudeste"])
    vendas.append(["","Eletrônicos", 2000.00, 1, datetime.today().date(), "Maria da Silva", "Norte" ])
    vendas.append([ "Mesa de Jantar 6 Cadeiras", "Casa", 1000.00, 0, datetime.today().date(), "Carlos Souza", "Sul" ])
    vendas.append([ "Monitor LG UltraWide", "Eletrônicos", 1500.00, 1, (datetime.today() + timedelta(days=30)).date(), "Ana Paula", "Sudeste" ])
    vendas.append([ "Notebook Dell Inspiron", "Eletrônicos", 3000.00, 1, datetime.today().date(), "João da Silva", "Sudeste" ])

    return vendas

def criar_dados_csv(produtos, vendedores, regioes, quantidade=100):

    vendas = []

    for _ in range(quantidade - 5):
        produto = choice(list(produtos.keys()))
        hoje = datetime.today()
        data_limite = randint(0, 180)
        data_venda = hoje - timedelta(days=data_limite)

        vendas.append([
            produto,
            produtos[produto],
            round(uniform(50.0, 5000.0), 2),
            randint(1, 5),
            data_venda.date(),
            choice(vendedores),
            choice(regioes)
        ])

    vendas.extend(seed_dados_ruins())
    
    return vendas


if __name__ == '__main__':

    vendedores, regioes, produtos = seed_dados_csv()
    linhas = criar_dados_csv(produtos, vendedores, regioes)
    caminho_pasta = '../data'
    caminho_csv = os.path.join(caminho_pasta, "vendas_exemplo.csv")


    os.makedirs(caminho_pasta, exist_ok=True)

    df = pd.DataFrame(linhas, columns=["produto", "categoria", "preco", "quantidade", "data_venda", "vendedor", "regiao"])
    df.to_csv(caminho_csv, index=False, encoding="utf-8")
    
    if os.path.exists(caminho_csv):
        print("Arquivo vendas_exemplo.csv gerado com sucesso na pasta 'data'")
    else:
        print(f"Falha ao gerar '{caminho_csv}'")