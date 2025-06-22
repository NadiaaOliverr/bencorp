import io
import pandas as pd
from datetime import datetime
from fastapi import HTTPException


def _ler_csv(arquivo_csv):
    try:
        return pd.read_csv(io.StringIO(arquivo_csv.decode('utf-8')))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro ao ler CSV: {e}")

def _validar_colunas(df):
    colunas_esperadas = ["produto", "categoria", "preco", "quantidade", "data_venda", "vendedor", "regiao"]
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            raise HTTPException(status_code=400, detail=f"Coluna obrigatória ausente: {coluna}")

def _limpar_linhas(df):
    df = df.dropna(how='all')
    return df

def _converter_tipos(df):
    df['preco'] = pd.to_numeric(df['preco'], errors='coerce')
    df['quantidade'] = pd.to_numeric(df['quantidade'], errors='coerce').astype('Int64')
    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df = df.dropna(subset=['produto', 'categoria', 'preco', 'quantidade', 'data_venda', 'vendedor', 'regiao'])
    return df

def _validar_regras_negocio(df):
    df = df[df['preco'] > 0]
    df = df[df['quantidade'] > 0]
    df = df[df['produto'].str.strip() != ""]
    df = df[df['categoria'].str.strip() != ""]
    df = df[df['vendedor'].str.strip() != ""]
    df = df[df['regiao'].str.strip() != ""]

    hoje = pd.Timestamp(datetime.today().date())
    df = df[df['data_venda'] <= hoje]
    return df
    
def processar_csv(arquivo_csv):

    df = _ler_csv(arquivo_csv)
    _validar_colunas(df)
    df = _limpar_linhas(df)
    df = _converter_tipos(df)
    df = _validar_regras_negocio(df)
    return df