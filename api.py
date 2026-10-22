from typing import List
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from sqlalchemy import func
from model import SessionLocal, Produto, Pedido

app = FastAPI(
    title="Loja de Roupas API",
    description="API RESTful para gestão de catálogo e métricas de vendas.",
    version="1.0.0"
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class ProdutoSchema(BaseModel):
    nome: str
    categoria: str
    preco: float = Field(..., gt=0)

class ProdutoResponse(ProdutoSchema):
    id: int

    class Config:
        from_attributes = True


@app.get("/produtos", response_model=List[ProdutoResponse], tags=["Produtos"])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(Produto).all()


@app.get("/produtos/{produto_id}", response_model=ProdutoResponse, tags=["Produtos"])
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    return produto


@app.post("/produtos", response_model=ProdutoResponse, status_code=status.HTTP_201_CREATED, tags=["Produtos"])
def criar_produto(produto: ProdutoSchema, db: Session = Depends(get_db)):
    novo_produto = Produto(
        nome=produto.nome,
        categoria=produto.categoria,
        preco=produto.preco
    )
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto


@app.get("/resumo", tags=["Métricas"])
def obter_resumo(db: Session = Depends(get_db)):
    total_pedidos = db.query(func.count(Pedido.id)).scalar() or 0
    faturamento_total = db.query(func.sum(Pedido.valor_total)).scalar() or 0.0
    ticket_medio = db.query(func.avg(Pedido.valor_total)).scalar() or 0.0

    return {
        "total_pedidos": total_pedidos,
        "faturamento_total": round(faturamento_total, 2),
        "ticket_medio": round(ticket_medio, 2)
    }