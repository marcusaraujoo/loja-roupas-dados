from model import Base, engine

def criar_tabelas():
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso.")

if __name__ == "__main__":
    criar_tabelas()