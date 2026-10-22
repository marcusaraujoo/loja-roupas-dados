import os
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Produto(Base):
    __tablename__ = "produto"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    categoria = Column(String(50), nullable=False)
    preco = Column(Float, nullable=False)

    pedidos = relationship("Pedido", back_populates="produto", cascade="all, delete-orphan")


class Pedido(Base):
    __tablename__ = "pedido"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produto.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    valor_total = Column(Float, nullable=False)
    data_pedido = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto", back_populates="pedidos")