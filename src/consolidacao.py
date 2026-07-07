from pathlib import Path
from leitor_projetos import ler_projetos, transformar_projetos_para_longo
from leitor_provas import ler_provas, transformar_provas_para_longo
from leitor_simulados import ler_simulados, transformar_simulados_para_longo

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_relatorios = pasta_projeto / "saidas" / "relatorios"

def consolidar_notas():
    simulados = transformar_simulados_para_longo(ler_simulados())
    provas = transformar_provas_para_longo(ler_provas())
    projetos = transformar_projetos_para_longo(ler_projetos())

    tabela = simulados.merge(
        provas,
        on=["turma", "aluno", "disciplina"],
        how="inner",
    )

    tabela = tabela.merge(
        projetos,
        on=["turma", "aluno", "disciplina"],
        how="inner",
    )

    tabela["nota_simulado"] = tabela["nota_simulado"].astype(float)
    tabela["nota_prova"] = tabela["nota_prova"].astype(float)
    tabela["nota_projeto"] = tabela["nota_projeto"].astype(float)

    tabela["nota_projeto_convertida"] = tabela["nota_projeto"] * 2

    tabela["media"] = (
        tabela["nota_simulado"] * 10
        + tabela["nota_prova"] * 10
        + tabela["nota_projeto_convertida"] * 5
    ) / 25

    tabela["media"] = tabela["media"].round(1)
    tabela["situacao"] = tabela["media"].apply(
        lambda media: "Aprovado" if media >= 6 else "Recuperacao"
    )

    return tabela

def salvar_relatorio_final(tabela):
    pasta_relatorios.mkdir(parents=True, exist_ok=True)
    caminho = pasta_relatorios / "notas_consolidadas.csv"
    tabela.to_csv(caminho, index=False, encoding="utf-8-sig")
    return caminho

if __name__ == "__main__":
    notas = consolidar_notas()
    caminho = salvar_relatorio_final(notas)
    print(notas.head())
    print(f"Relatorio salvo em: {caminho}")