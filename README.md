# Loja de Roupas - API e Pipeline de Dados

Projeto prático para gerenciamento de catálogo e histórico de vendas de um e-commerce de roupas. O sistema conecta uma API RESTful em Python a um banco de dados relacional PostgreSQL.

## Tecnologias Utilizadas

- Python 3.10+
- FastAPI e Uvicorn
- SQLAlchemy
- PostgreSQL (driver psycopg2)
- Pydantic
- Pytest e HTTPX

## Estrutura do Repositório

- `model.py`: Mapeamento ORM das tabelas (produto e pedido) e conexão com o banco.
- `api.py`: Endpoints para listagem, cadastro e cálculo de métricas de vendas.
- `criar_tabelas.py`: Script DDL para criação das tabelas no banco de dados.
- `popular.py`: Script para inserção de dados sintéticos para testes.
- `test_api.py`: Testes unitários e de integração para validação das rotas.

## Instruções de Execução

### 1. Clonar o repositório e configurar o ambiente virtual
```bash
git clone [https://github.com/marcusaraujoo/loja-roupas-dados.git](https://github.com/marcusaraujoo/loja-roupas-dados.git)
cd loja-roupas-dados

python -m venv venv
source venv/Scripts/activate