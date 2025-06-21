from pydantic import BaseModel
from datetime import date, datetime

class VendaSchema(BaseModel):
    produto: str
    categoria: str
    preco: float
    quantidade: int
    data_venda: date
    vendedor: str
    regiao: str

    model_config = {
        "from_attributes": True
    }

class VendaSchemaOut(BaseModel):
    id: int
    produto: str
    categoria: str
    preco: float
    quantidade: int
    data_venda: date
    vendedor: str
    regiao: str
    created_at: datetime

    model_config = {
        "from_attributes": True
    }