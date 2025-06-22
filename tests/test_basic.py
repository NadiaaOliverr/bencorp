import requests
import pandas as pd
import time
import traceback

BASE_URL = "http://localhost:8000"

def test_basic_crud():
    """Testa operações CRUD básicas"""

    venda_data = {
        "produto": "Notebook",
        "categoria": "Eletrônicos",
        "preco": 2500.00,
        "quantidade": 1,
        "data_venda": "2024-01-15",
        "vendedor": "João",
        "regiao": "Sudeste"
    }
    
    response = requests.post(f"{BASE_URL}/vendas", json=venda_data)
    assert response.status_code == 201
    venda_id = response.json()["id"]
    
    response = requests.get(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200
    
    response = requests.get(f"{BASE_URL}/vendas")
    assert response.status_code == 200

    response = requests.delete(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 200
    assert "mensagem" in response.json()
    
    response = requests.get(f"{BASE_URL}/vendas/{venda_id}")
    assert response.status_code == 404
    

def test_etl_csv():
    """Testa importação de CSV"""

    df = pd.DataFrame({
        'produto': ['Mouse', 'Teclado'],
        'categoria': ['Eletrônicos', 'Eletrônicos'],
        'preco': [50.0, 150.0],
        'quantidade': [2, 1],
        'data_venda': ['2024-01-10', '2024-01-11'],
        'vendedor': ['Maria', 'José'],
        'regiao': ['Sul', 'Norte']
    })
    
    csv_content = df.to_csv(index=False)
    
    files = {'file': ('test.csv', csv_content, 'text/csv')}
    response = requests.post(f"{BASE_URL}/etl/importar-csv", files=files)
    
    assert response.status_code == 200

def test_relatorio():
    """Testa relatório mensal"""

    response = requests.get(f"{BASE_URL}/etl/relatorio-mensal?mes=2024-01")
    assert response.status_code == 200
    
    data = response.json()
    assert "total_vendas" in data
    assert "vendas_por_categoria" in data

def test_filtro_categoria_e_paginacao():
    """Testa listagem com filtro de categoria e paginação"""

    response = requests.get(f"{BASE_URL}/vendas?categoria=Eletrônicos&pagina=1&tamanho_pagina=5")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert all(venda['categoria'] == 'Eletrônicos' for venda in data)

def test_top_vendedores():
    """Testa geração do top vendedores"""

    response = requests.get(f"{BASE_URL}/etl/top-vendedores?mes=2024-01&top=2")
    assert response.status_code == 200
    data = response.json()
    assert "top_vendedores" in data
    assert len(data["top_vendedores"]) <= 2

def test_exportacao():
    """Testa a exportação de dados em CSV, JSON e erro de formato inválido"""

    response = requests.get(f"{BASE_URL}/etl/exportar-dados?formato=csv")
    assert response.status_code == 200
    assert "text/csv" in response.headers["content-type"]

    response = requests.get(f"{BASE_URL}/etl/exportar-dados?formato=json")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

    response = requests.get(f"{BASE_URL}/etl/exportar-dados?formato=xml")
    assert response.status_code == 400
    assert "Formato inválido" in response.json()["detail"]


def run_all_tests():
    print("\nIniciando testes...\n")

    time.sleep(5)

    tests = [
        ("Teste: CRUD básico", test_basic_crud),
        ("Teste: Importação CSV", test_etl_csv),
        ("Teste: Relatório mensal", test_relatorio),
        ("Teste: Filtro por categoria e paginação", test_filtro_categoria_e_paginacao),
        ("Teste: Top Vendedores", test_top_vendedores),
        ("Teste: Exportação de dados", test_exportacao)
    ]

    for nome, func in tests:
        try:
            func()
            print(f"✅ {nome} funcionando!\n")
        except AssertionError as e:
            print(f"\n❌ Falhou: {nome}")
            print("\nDetalhes do traceback:")
            traceback.print_exc()
            return
        except Exception as e:
            print(f"\n❌ Erro inesperado em: {nome}")
            traceback.print_exc()
            return

    print("\nTODOS OS TESTES PASSARAM COM SUCESSO!!!\n")

if __name__ == "__main__":
    run_all_tests()