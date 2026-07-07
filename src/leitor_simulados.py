from pathlib import Path
import pandas as pd

pasta_projeto = Path(__file__).resolve().parent.parent
pasta_simulados = pasta_projeto / "dados" / "simulados"


def ler_simulados():
    arquivos = list(pasta_simulados.glob("simulado_*.csv"))
    tabelas = []

    for arquivo in arquivos:
        tabela = pd.read_csv(arquivo)
        tabelas.append(tabela)

    if not tabelas:
        raise FileNotFoundError("Nenhum arquivo de simulado foi encontrado.")

    return pd.concat(tabelas, ignore_index=True)


def transformar_simulados_para_longo(tabela):
    return tabela.melt(
        id_vars=["turma", "aluno"],
        var_name="disciplina",
        value_name="nota_simulado",
    )


if __name__ == "__main__":
    simulados = ler_simulados()
    simulados_longos = transformar_simulados_para_longo(simulados)
    print(simulados_longos.head())

    