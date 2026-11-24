# Loja de Roupas - API e Pipeline de Dados

Projeto prático para gerenciamento de catálogo, histórico de vendas e análise de faturamento de um e-commerce de roupas. O sistema conecta uma API RESTful em Python a um banco de dados relacional PostgreSQL.

## Tecnologias Utilizadas

- Python 3.10+
- FastAPI e Uvicorn
- SQLAlchemy
- PostgreSQL (driver psycopg2)
- Pandas e Matplotlib
- Concurrent Futures (ProcessPoolExecutor)
- Pytest e HTTPX

## Estrutura do Repositório

- `model.py`: Mapeamento ORM das tabelas (`produto` e `pedido`) e conexão com o banco.
- `api.py`: Endpoints para listagem, cadastro e cálculo de métricas de vendas.
- `criar_tabelas.py`: Script DDL para criação das tabelas no banco de dados.
- `popular.py`: Script para inserção de dados sintéticos para testes.
- `test_api.py`: Testes unitários e de integração para validação das rotas.
- `processamento_paralelo.py`: Processamento em lote de cálculos financeiros comparando execução sequencial e paralela.
- `analise.py`: Análise exploratória com Pandas e geração de gráfico com Matplotlib (`grafico_faturamento.png`).
- `requirements.txt`: Dependências do projeto.

## Escolha Técnica: Processamento Paralelo

Para a etapa de escalabilidade, optei pelo processamento paralelo (`ProcessPoolExecutor`) em vez do MongoDB porque o modelo de dados da loja de roupas (produtos e pedidos) é fortemente relacional e já está bem estruturado no PostgreSQL, não havendo necessidade de dados semiestruturados ou sem esquema fixo. O gargalo real em operações de fechamento financeiro e auditoria de pedidos está no tempo de CPU ao processar grandes volumes de registros.

**Medição de Desempenho (processamento de 1.200.000 registros):**
- Execução sequencial (antes): **5.0902 segundos**
- Execução paralela com 12 núcleos (depois): **2.0538 segundos**
- Ganho de performance: **2.48x mais rápido** (redução de **59.7%** no tempo total).

## Análise de Dados (Pergunta do E0)

**Pergunta:** *Qual categoria de roupa traz o maior faturamento total para a loja?*

**Resposta:** A categoria **Casacos** traz o maior faturamento total para a loja, gerando **R$ 14.793,40** (**64,6%** do faturamento total, com 66 unidades vendidas), conforme ilustrado no gráfico gerado (`grafico_faturamento.png`). Inicialmente esperava-se que categorias de peças básicas e mais baratas (como Camisetas) liderassem o faturamento pelo giro cotidiano, mas os dados mostraram que os Casacos combinam alto volume de saída com um ticket médio muito superior, concentrando quase dois terços de toda a receita.

## Instruções de Execução

### 1. Clonar o repositório e configurar o ambiente virtual
```bash
git clone [https://github.com/marcusaraujoo/loja-roupas-dados.git](https://github.com/marcusaraujoo/loja-roupas-dados.git)
cd loja-roupas-dados

python -m venv venv
source venv/Scripts/activate