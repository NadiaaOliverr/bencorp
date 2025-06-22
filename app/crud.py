from sqlalchemy.orm import Session
from sqlalchemy import asc, desc
from app.models import Venda

def get_venda_por_id(db, venda_id):
    return db.query(Venda).filter(Venda.id == venda_id).first()

def get_vendas_paginadas(db, deslocamento, tamanho_pagina):
    return db.query(Venda).offset(deslocamento).limit(tamanho_pagina).all()

def criar_venda_db(db, dados):
    nova_venda = Venda(**dados)
    db.add(nova_venda)
    db.commit()
    db.refresh(nova_venda)
    return nova_venda

def atualizar_venda_db(db, venda_existente, novos_dados):
    for campo, valor in novos_dados.items():
        setattr(venda_existente, campo, valor)
    db.commit()
    db.refresh(venda_existente)
    return venda_existente

def deletar_venda_db(db, venda):
    db.delete(venda)
    db.commit()

def filtrar_e_ordenar_vendas(query, categoria=None, ordenar_por=None, ordem="asc"):
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
    return query