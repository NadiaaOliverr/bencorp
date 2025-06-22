from fastapi import HTTPException
from sqlalchemy import asc, desc
from app.models import Venda
import pandas as pd

def get_venda_por_id(db, venda_id):
    return db.query(Venda).filter(Venda.id == venda_id).first()

def criar_dataframe_com_dados_banco(db):
    vendas = db.query(Venda).all()
    if not vendas:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada no banco")

    df = pd.DataFrame([{
        "categoria": v.categoria,
        "preco": float(v.preco),
        "quantidade": v.quantidade,
        "data_venda": v.data_venda,
        "vendedor": v.vendedor
    } for v in vendas])

    return df

def _tratar_excecao(db, mensagem, e):
    db.rollback()
    raise HTTPException(status_code=500, detail=f"{mensagem}: {e}")

def criar_venda_db(db, dados):
    try:
        nova_venda = Venda(**dados)
        db.add(nova_venda)
        db.commit()
        db.refresh(nova_venda)
        return nova_venda
    except Exception as e:
        _tratar_excecao(db, "Erro ao criar venda", e)

def criar_vendas_em_lote(db, dados):
    try:
        db.add_all(dados)
        db.commit()
    except Exception as e:
        _tratar_excecao(db, "Erro ao importar vendas em lote", e)

def atualizar_venda_db(db, venda_existente, novos_dados):
    try:
        for campo, valor in novos_dados.items():
            setattr(venda_existente, campo, valor)
        db.commit()
        db.refresh(venda_existente)
        return venda_existente
    except Exception as e:
        _tratar_excecao(db, "Erro ao atualizar venda", e)

def deletar_venda_db(db, venda):
    try:
        db.delete(venda)
        db.commit()
    except Exception as e:
        _tratar_excecao(db, "Erro ao deletar venda", e)

def filtrar_e_ordenar_vendas(query, categoria=None, vendedor = None, ordenar_por=None, ordem="asc", pagina=1, tamanho_pagina=10):
    deslocamento = (pagina - 1) * tamanho_pagina

    if vendedor:
        query = query.filter(Venda.vendedor == vendedor)
    if categoria:
        query = query.filter(Venda.categoria == categoria)
    if ordenar_por:
        campo = getattr(Venda, ordenar_por, None)
        if not campo:
            raise ValueError(f"Campo de ordenação inválido: {ordenar_por}")

        ordem = ordem.lower()
        if ordem not in ("asc", "desc"):
            raise ValueError(f"Ordem inválida: {ordem}. Use 'asc' ou 'desc'.")

        direcao = asc if ordem == "asc" else desc
        query = query.order_by(direcao(campo))
    
    vendas = query.offset(deslocamento).limit(tamanho_pagina).all()

    if not vendas:
        raise HTTPException(status_code=404, detail="Página não encontrada")
    
    return vendas