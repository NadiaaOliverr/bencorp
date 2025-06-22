from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from sqlalchemy.orm import Session
from app.models import Venda
from app.database import get_db
from app.etl import processar_csv
from app.crud import criar_vendas_em_lote


router = APIRouter(prefix="/etl", tags=["ETL"])

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
