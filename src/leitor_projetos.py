from pathlib import Path

import pandas as pd
import pdfplumber


pasta_projeto = Path(__file__).resolve().parent.parent
pasta_projetos = pasta_projeto / "dados" / "projetos"


def ler_um_pdf(caminho_pdf):
    linhas = []

    with pdfplumber.open(caminho_pdf) as pdf:
        for pagina in pdf.pages:
            tabelas = pagina.extract_tables()
            for tabela in tabelas:
                linhas.extend(tabela)

    if not linhas:
        raise ValueError(f"Nenhuma tabela encontrada em {caminho_pdf.name}")

    cabecalho = linhas[0]
    dados = linhas[1:]
    return pd.DataFrame(dados, columns=cabecalho)


def ler_projetos():
    arquivos = list(pasta_projetos.glob("projeto_*.pdf"))
    tabelas = []

    for arquivo in arquivos:
        tabela = ler_um_pdf(arquivo)
        tabelas.append(tabela)

    if not tabelas:
        raise FileNotFoundError("Nenhum PDF de projeto foi encontrado.")

    return pd.concat(tabelas, ignore_index=True)


def transformar_projetos_para_longo(tabela):
    tabela = tabela.rename(columns={"Turma": "turma", "Aluno": "aluno"})

    return tabela.melt(
        id_vars=["turma", "aluno"],
        var_name="disciplina",
        value_name="nota_projeto",
    )


if __name__ == "__main__":
    projetos = ler_projetos()
    projetos_longos = transformar_projetos_para_longo(projetos)
    print(projetos_longos.head())
    