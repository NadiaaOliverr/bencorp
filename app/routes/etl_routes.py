from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends, status
from sqlalchemy.orm import Session
from app.models import Venda
from app.database import get_db
from app.etl import processar_csv, gerar_relatorio_mensal, gerar_top_vendedores_mensal, exportar_dados
from app.crud import criar_vendas_em_lote
from typing import Optional

router = APIRouter(prefix="/etl", tags=["ETL"])

@router.get("/exportar-dados", status_code=200)
def exportar_dados_csv_json(formato:str = Query(...), categoria: Optional[str] = Query(None), vendedor:Optional[str] = Query(None), db:Session = Depends(get_db)):
    """ 
    Exporta os dados de vendas como CSV ou JSON na resposta. Permite filtros por categoria e vendedor.
    """
    return exportar_dados(db, formato, categoria, vendedor)

@router.get("/relatorio-mensal", status_code=status.HTTP_200_OK)
def relatorio_mensal(mes: str = Query(..., description="Formato YYYY-MM"), db: Session = Depends(get_db)):
    """
    Gera um relatório mensal de vendas retornando o agregado do mês, incluindo o maior vendedor.
    """

    relatorio = gerar_relatorio_mensal(db, mes)

    return relatorio

@router.get("/top-vendedores", status_code=status.HTTP_200_OK)
def top_vendedores(mes: str, top: int = Query(3), db: Session = Depends(get_db)):
    """
    Retorna o total de vendas do TOP N vendedores do mês especificado e detalha as vendas feitas por categoria.
    """
    relatorio = gerar_top_vendedores_mensal(db, mes, top)
    
    return relatorio


@router.post("/importar-csv", status_code=status.HTTP_200_OK)
def importar_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Importa um arquivo CSV de vendas, valida com pandas e insere no banco.
    """
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Arquivo deve ser CSV")

    df = processar_csv(file.file.read())
    vendas = []

    for _, linha in df.iterrows():
        nova_venda = Venda( produto=linha["produto"], categoria=linha["categoria"], preco=linha["preco"], quantidade=int(linha["quantidade"]), data_venda=linha["data_venda"].date(), vendedor=linha["vendedor"], regiao=linha["regiao"] )
        vendas.append(nova_venda)
    
    criar_vendas_em_lote(db, vendas)

    return {"mensagem": f"{len(df)} vendas importadas com sucesso!"}
