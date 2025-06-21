from fastapi import FastAPI
from app.routes import vendas

app = FastAPI()
app.include_router(vendas.router)