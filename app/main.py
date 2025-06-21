from fastapi import FastAPI
from app.routes import vendas

app = FastAPI(
    title="Case Bencorp",
    version="1.0.0",
    description=(
        "API desenvolvida para o case da Bencorp. "
        "Permite realizar operações de CRUD de vendas com validações de dados, "
        "integração com banco de dados relacional (PostgreSQL) e endpoints para ingestão e processamento "
        "de dados (ETL). Tem suporte a paginação e filtros."
    )
)

app.include_router(vendas.router)