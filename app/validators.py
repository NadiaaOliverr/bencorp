import re
from datetime import datetime
from fastapi import HTTPException

def _lancar_erro(mensagem):
    raise HTTPException(status_code=400, detail=mensagem)

def validar_campo_obrigatorio_e_nao_vazio(valor, nome):
    if not valor or not valor.strip():
        _lancar_erro(f"{nome} é obrigatório e não pode estar em branco")

def validar_tamanho_maximo(valor, nome, tamanho):
    if len(valor) > tamanho:
        _lancar_erro(f"{nome} deve ter no máximo {tamanho} caracteres")

def validar_maior_que_zero(valor, nome):
    if valor <= 0:
        _lancar_erro(f"{nome} deve ser maior que zero")

def validar_data_nao_futura(data_str):
    try:
        data = datetime.strptime(str(data_str), "%Y-%m-%d")
    except ValueError:
        _lancar_erro("Data de venda deve estar no formato YYYY-MM-DD")
    if data > datetime.today():
        _lancar_erro("Data de venda não pode ser futura")

def validar_categoria_permitida(categoria):
    permitidas = {"Eletrônicos", "Roupas", "Casa", "Esportes", "Livros"}
    if categoria not in permitidas:
        _lancar_erro(f"Categoria '{categoria}' não é válida. Permitidas: {', '.join(permitidas)}")

def validar_regiao_permitida(regiao):
    permitidas = {"Norte", "Sul", "Sudeste", "Centro-Oeste", "Nordeste"}
    if regiao not in permitidas:
        _lancar_erro(f"Região '{regiao}' não é válida. Permitidas: {', '.join(permitidas)}")

def validar_texto_sanitizado(valor, nome):
    padrao = r"^[a-zA-Z0-9\s\-\.,áéíóúãõçÁÉÍÓÚÃÕÇ]+$"
    if not re.match(padrao, valor):
        _lancar_erro(f"{nome} contém caracteres inválidos")


def validar_venda(dados):
    preco = dados.get("preco")
    quantidade = dados.get("quantidade")
    data_venda = dados.get("data_venda")
    produto = dados.get("produto")
    categoria = dados.get("categoria")
    vendedor = dados.get("vendedor")
    regiao = dados.get("regiao")

    validar_campo_obrigatorio_e_nao_vazio(produto, "Produto")
    validar_campo_obrigatorio_e_nao_vazio(categoria, "Categoria")
    validar_campo_obrigatorio_e_nao_vazio(vendedor, "Vendedor")
    validar_campo_obrigatorio_e_nao_vazio(regiao, "Região")

    validar_texto_sanitizado(produto, "Produto")
    validar_texto_sanitizado(vendedor, "Vendedor")

    validar_maior_que_zero(preco, "Preço")
    validar_maior_que_zero(quantidade, "Quantidade")
    validar_categoria_permitida(categoria)
    validar_regiao_permitida(regiao)
    validar_tamanho_maximo(produto, "Produto", 100)
    validar_data_nao_futura(data_venda)