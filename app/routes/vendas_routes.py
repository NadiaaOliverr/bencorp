from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import Venda    
from app.database import get_db
from app.crud import get_venda_por_id, criar_venda_db, deletar_venda_db, atualizar_venda_db, filtrar_e_ordenar_vendas
from app.validators import validar_venda
from app.schemas import VendaSchema, VendaSchemaOut
from typing import List, Optional

router = APIRouter(prefix="/vendas", tags=["vendas"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[VendaSchemaOut])
def listar_vendas(pagina: int = 1, tamanho_pagina: int = 10, categoria: Optional[str] = None, vendedor: Optional[str] = None, ordenar_por: Optional[str] = None, ordem: Optional[str] = "asc", db: Session = Depends(get_db)):
    """
    Retorna uma lista de vendas com paginação, ordenação dinâmica e filtro por categoria.  Responde com 404 se a página não existir.
    """
    query = db.query(Venda)

    try:
        vendas = filtrar_e_ordenar_vendas(query, categoria, vendedor, ordenar_por, ordem, pagina, tamanho_pagina)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return vendas

@router.get("/{venda_id}", status_code=status.HTTP_200_OK, response_model=VendaSchemaOut)
def buscar_venda_por_id(venda_id: int, db: Session = Depends(get_db)):
    """
    Retorna os detalhes de uma venda pelo ID. Responde com 404 se a venda não for encontrada.
    """
    venda = get_venda_por_id(db, venda_id)
    if not venda:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Venda não encontrada")
    return venda

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=VendaSchemaOut)
def criar_venda(venda: VendaSchema, db=Depends(get_db)):
    """
    Cria uma nova venda com os dados informados. Valida os campos antes de salvar no banco.
    """

    dados = venda.model_dump()
    validar_venda(dados)
    nova_venda = criar_venda_db(db, dados)
    return nova_venda


@router.put("/{venda_id}", status_code=status.HTTP_200_OK, response_model=VendaSchemaOut)
def atualizar_venda(venda_id: int, nova_venda: VendaSchema, db: Session = Depends(get_db)):
    """
    Atualiza os dados de uma venda pelo ID. Recebe um objeto com os novos dados. Retorna a venda atualizada ou 404 se não existir.
    """
    venda_existente = get_venda_por_id(db, venda_id)
    if not venda_existente:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    dados = nova_venda.model_dump()
    validar_venda(dados)

    venda_atualizada = atualizar_venda_db(db, venda_existente, dados)
    return venda_atualizada

@router.delete("/{venda_id}", status_code=status.HTTP_200_OK)
def deletar_venda(venda_id: int, db: Session = Depends(get_db)):
    """
    Remove uma venda do banco de dados pelo ID. Retorna uma mensagem de sucesso ou 404 se a venda não for encontrada.
    """
    venda = get_venda_por_id(db, venda_id)
    if not venda:
        raise HTTPException(status_code=404, detail="Venda não encontrada")

    deletar_venda_db(db, venda)
    return {"mensagem": "Venda deletada com sucesso"}