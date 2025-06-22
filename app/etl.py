import io
import pandas as pd
from fastapi.responses import StreamingResponse
from datetime import datetime
from fastapi import HTTPException
from app.crud import criar_dataframe_com_dados_banco


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
    df = df.dropna(how='all').drop_duplicates()
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


def _get_dataframe_filtrado_por_mes(db, mes):
    df = criar_dataframe_com_dados_banco(db)

    df['data_venda'] = pd.to_datetime(df['data_venda'], errors='coerce')
    df['mes'] = df['data_venda'].dt.to_period('M').astype(str)

    df_mes = df[df['mes'] == mes]

    if df_mes.empty:
        raise HTTPException(status_code=404, detail=f"Nenhuma venda para o mês {mes}")

    return df_mes

def processar_csv(arquivo_csv):
    df = _ler_csv(arquivo_csv)
    _validar_colunas(df)
    df = _limpar_linhas(df)
    df = _converter_tipos(df)
    df = _validar_regras_negocio(df)
    return df


def gerar_relatorio_mensal(db, mes):
    df_mes = _get_dataframe_filtrado_por_mes(db, mes)

    total_vendas = round((df_mes['preco'] * df_mes['quantidade']).sum(), 2)
    total_itens = int(df_mes['quantidade'].sum())

    vendas_categoria = (df_mes.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum()) .to_dict())
    vendas_categoria = {categoria: round(valor, 2) for categoria, valor in vendas_categoria.items()}

    vendas_por_vendedor = (df_mes.groupby('vendedor').apply(lambda grupo: (grupo['preco'] * grupo['quantidade']).sum()))

    top_vendedor = vendas_por_vendedor.idxmax()
    total_vendido_top_vendedor = round(float(vendas_por_vendedor.max()), 2)

    relatorio = {
        "mes": mes,
        "total_vendas": total_vendas,
        "total_itens": total_itens,
        "vendas_por_categoria": vendas_categoria,
        "top_vendedor": top_vendedor,
        "total_vendido_vendedor": total_vendido_top_vendedor
    }

    return relatorio

def gerar_top_vendedores_mensal(db, mes: str, top: int = 3):
    df_mes = _get_dataframe_filtrado_por_mes(db, mes)

    vendas_por_vendedor = (df_mes.groupby('vendedor').apply(lambda x: (x['preco'] * x['quantidade']).sum()) .sort_values(ascending=False) .head(top) .round(2))

    top_vendedores = []
    for vendedor, total in vendas_por_vendedor.items():
        df_vendedor = df_mes[df_mes['vendedor'] == vendedor]
        por_categoria = (df_vendedor.groupby('categoria').apply(lambda x: (x['preco'] * x['quantidade']).sum()) .round(2) .to_dict())
        top_vendedores.append({"vendedor": vendedor, "total_vendas": float(total), "vendas_por_categoria": por_categoria})

    relatorio = {
        "mes": mes,
        "top_vendedores": top_vendedores
    }

    return relatorio


def exportar_dados(db, formato, categoria, vendedor):
    df = criar_dataframe_com_dados_banco(db)

    if categoria:
        df = df[df['categoria'] == categoria]
    if vendedor:
        df = df[df['vendedor'] == vendedor]

    if df.empty:
        raise HTTPException(status_code=404, detail="Nenhuma venda encontrada com os filtros informados")

    if formato == "csv":
        buffer = io.StringIO()
        df.to_csv(buffer, index=False)
        buffer.seek(0)
        return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={"Content-Disposition": "attachment; filename=vendas.csv"})

    elif formato == "json":
        return df.to_dict(orient="records")

    else:
        raise HTTPException(status_code=400, detail="Formato inválido. Use 'csv' ou 'json'")