from app.models import Base, Venda
from app.database import engine, SessionLocal
from faker import Faker
from random import choice, randint, uniform
from datetime import datetime, timedelta


def seed_dados_fake():

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

def criar_dados_fake(produtos, vendedores, regioes, quantidade=500):

    vendas = []

    for _ in range(quantidade):

        produto = choice(list(produtos.keys()))
        hoje = datetime.today()
        data_limite = randint(0, 180)
        data_venda = hoje - timedelta(days=data_limite)

        venda = Venda(
            produto=produto,
            categoria=produtos[produto],
            preco=round(uniform(50.0, 5000.0), 2),
            quantidade=randint(1, 5),
            data_venda=data_venda.date(),
            vendedor=choice(vendedores),
            regiao=choice(regioes)
        )
        vendas.append(venda)

    return vendas

if __name__ == '__main__':

    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    vendedores, regioes, produtos = seed_dados_fake()
    vendas = criar_dados_fake(produtos, vendedores, regioes)
    db.add_all(vendas)
    db.commit()
    db.close()

    print("Tabela criada e populada com 500 vendas fake!")