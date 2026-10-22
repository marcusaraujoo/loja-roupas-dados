from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_listar_produtos():
    response = client.get("/produtos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_obter_produto_inexistente():
    response = client.get("/produtos/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Produto não encontrado"

def test_obter_resumo_metricas():
    response = client.get("/resumo")
    assert response.status_code == 200
    dados = response.json()
    assert "total_pedidos" in dados
    assert "faturamento_total" in dados
    assert "ticket_medio" in dados