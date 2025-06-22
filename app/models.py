from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Date, DECIMAL, DateTime, Numeric, func
from datetime import date

class Base(DeclarativeBase):
    pass

class Venda(Base):
    __tablename__ = "vendas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    produto: Mapped[str] = mapped_column(String(100), nullable=False)
    categoria: Mapped[str] = mapped_column(String(50), nullable=False)
    preco: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    quantidade: Mapped[int] = mapped_column(Integer, nullable=False)
    data_venda: Mapped[date] = mapped_column(Date, nullable=False)
    vendedor: Mapped[str] = mapped_column(String(100), nullable=False)
    regiao: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[date] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    def __repr__(self) -> str:
        return (
            f"<Venda(id={self.id}, produto={self.produto}, categoria={self.categoria}, "
            f"preco={self.preco}, quantidade={self.quantidade}, data_venda={self.data_venda}, "
            f"vendedor={self.vendedor}, regiao={self.regiao}, created_at={self.created_at})>"
        )