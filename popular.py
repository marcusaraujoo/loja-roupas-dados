import random
from datetime import datetime, timedelta
from model import SessionLocal, Produto, Pedido

def popular_banco():
    db = SessionLocal()
    try:
        produtos_iniciais = [
            Produto(nome="Camiseta Algodão Premium", categoria="Camisetas", preco=59.90),
            Produto(nome="Calça Jeans Slim Fit", categoria="Calças", preco=179.90),
            Produto(nome="Jaqueta Jeans Oversized", categoria="Casacos", preco=249.90),
            Produto(nome="Moletom Streetwear Capuz", categoria="Casacos", preco=199.90),
            Produto(nome="Bermuda Cargo Utilitária", categoria="Bermudas", preco=99.90),
        ]
        
        db.add_all(produtos_iniciais)
        db.commit()

        produtos = db.query(Produto).all()

        for _ in range(30):
            prod = random.choice(produtos)
            qtd = random.randint(1, 4)
            data_historica = datetime.now() - timedelta(days=random.randint(0, 45))
            
            pedido = Pedido(
                produto_id=prod.id,
                quantidade=qtd,
                valor_total=round(prod.preco * qtd, 2),
                data_pedido=data_historica
            )
            db.add(pedido)

        db.commit()
        print("Banco de dados populado com sucesso.")

    except Exception as e:
        db.rollback()
        print(f"Erro ao popular o banco de dados: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    popular_banco()