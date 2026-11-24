import os
import time
from concurrent.futures import ProcessPoolExecutor
from model import SessionLocal, Pedido


def processar_lote(lote_valores):
    total_liquido = 0.0
    for valor in lote_valores:
        taxa_plataforma = valor * 0.08
        imposto = valor * 0.12
        custo_operacional = (valor ** 0.5) * 0.05
        liquido = valor - taxa_plataforma - imposto - custo_operacional
        for _ in range(120):
            liquido = (liquido * 1.0001) / 1.0001
        total_liquido += liquido
    return total_liquido


def carregar_dados_base():
    db = SessionLocal()
    try:
        pedidos = db.query(Pedido.valor_total).all()
        valores = [p[0] for p in pedidos]
        if not valores:
            valores = [120.0, 250.0, 89.90, 340.0, 199.90]
        return valores * 20000
    finally:
        db.close()


def dividir_em_lotes(lista, num_lotes):
    tamanho = len(lista) // num_lotes
    lotes = []
    for i in range(num_lotes):
        inicio = i * tamanho
        fim = None if i == num_lotes - 1 else (i + 1) * tamanho
        lotes.append(lista[inicio:fim])
    return lotes


if __name__ == "__main__":
    dados = carregar_dados_base()
    nucleos = os.cpu_count() or 4
    lotes = dividir_em_lotes(dados, nucleos)

    print(f"Total de registros processados: {len(dados)}")
    print(f"Nucleos de CPU utilizados: {nucleos}\n")

    inicio_seq = time.perf_counter()
    resultado_seq = sum(processar_lote(lote) for lote in lotes)
    tempo_seq = time.perf_counter() - inicio_seq
    print(f"Tempo Sequencial (antes): {tempo_seq:.4f} segundos | Total: R$ {resultado_seq:,.2f}")

    inicio_par = time.perf_counter()
    with ProcessPoolExecutor(max_workers=nucleos) as executor:
        resultados = list(executor.map(processar_lote, lotes))
    resultado_par = sum(resultados)
    tempo_par = time.perf_counter() - inicio_par
    print(f"Tempo Paralelo (depois):  {tempo_par:.4f} segundos | Total: R$ {resultado_par:,.2f}")

    ganho = tempo_seq / tempo_par
    reducao = ((tempo_seq - tempo_par) / tempo_seq) * 100
    print(f"\nSpeedup: {ganho:.2f}x mais rapido (reducao de {reducao:.1f}% no tempo)")