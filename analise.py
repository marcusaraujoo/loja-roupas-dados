import pandas as pd
import matplotlib.pyplot as plt
from model import engine


def executar_analise():
    query = """
        SELECT 
            p.categoria,
            pe.quantidade,
            pe.valor_total
        FROM pedido pe
        JOIN produto p ON pe.produto_id = p.id
    """

    df = pd.read_sql(query, engine)

    if df.empty:
        print("Nenhum pedido encontrado no banco. Rode 'python popular.py' primeiro.")
        return

    resumo = (
        df.groupby("categoria", as_index=False)
        .agg(
            total_itens=("quantidade", "sum"),
            faturamento_total=("valor_total", "sum")
        )
        .sort_values(by="faturamento_total", ascending=False)
    )

    faturamento_geral = resumo["faturamento_total"].sum()
    resumo["percentual"] = (resumo["faturamento_total"] / faturamento_geral) * 100

    lider = resumo.iloc[0]

    print("=== RESUMO DE FATURAMENTO POR CATEGORIA ===")
    print(resumo.to_string(index=False))
    print("\n=== RESPOSTA DA PERGUNTA (E0) ===")
    print(
        f"A categoria '{lider['categoria']}' traz o maior faturamento total para a loja: "
        f"R$ {lider['faturamento_total']:,.2f} ({lider['percentual']:.1f}% do total)."
    )

    plt.figure(figsize=(9, 5))
    barras = plt.bar(resumo["categoria"], resumo["faturamento_total"], color="#2b5c8f", width=0.55)

    plt.title("Faturamento Total por Categoria de Roupa", fontsize=13, pad=12)
    plt.xlabel("Categoria", fontsize=11)
    plt.ylabel("Faturamento Total (R$)", fontsize=11)
    plt.grid(axis="y", linestyle="--", alpha=0.5)

    for barra, pct in zip(barras, resumo["percentual"]):
        altura = barra.get_height()
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            altura + (faturamento_geral * 0.01),
            f"R$ {altura:,.2f}\n({pct:.1f}%)",
            ha="center",
            va="bottom",
            fontsize=9
        )

    plt.ylim(0, resumo["faturamento_total"].max() * 1.18)
    plt.tight_layout()
    plt.savefig("grafico_faturamento.png", dpi=150)
    print("\nGrafico salvo como 'grafico_faturamento.png'.")


if __name__ == "__main__":
    executar_analise()