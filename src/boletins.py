from pathlib import Path
import re

from src.consolidacao import consolidar_notas


pasta_projeto = Path(__file__).resolve().parent.parent
pasta_boletins = pasta_projeto / "saidas" / "boletins"


def limpar_nome_arquivo(texto):
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")


def gerar_boletins():
    notas = consolidar_notas()
    pasta_boletins.mkdir(parents=True, exist_ok=True)

    for (turma, aluno), tabela_aluno in notas.groupby(["turma", "aluno"]):
        nome = limpar_nome_arquivo(f"{turma}_{aluno}") + ".html"
        caminho = pasta_boletins / nome

        linhas = ""
        for _, linha in tabela_aluno.iterrows():
            linhas += f"""
            <tr>
                <td>{linha['disciplina']}</td>
                <td>{linha['nota_simulado']}</td>
                <td>{linha['nota_prova']}</td>
                <td>{linha['nota_projeto']}</td>
                <td>{linha['media']}</td>
                <td>{linha['situacao']}</td>
            </tr>
            """

        html = f"""
        <!doctype html>
        <html lang="pt-br">
        <head>
            <meta charset="utf-8">
            <title>Boletim - {aluno}</title>
        </head>
        <body>
            <h1>Boletim Escolar - 2 Bimestre</h1>
            <p><strong>Aluno:</strong> {aluno}</p>
            <p><strong>Turma:</strong> {turma}</p>
            <table border="1" cellpadding="6">
                <tr>
                    <th>Disciplina</th>
                    <th>Simulado</th>
                    <th>Prova</th>
                    <th>Projeto</th>
                    <th>Media</th>
                    <th>Situacao</th>
                </tr>
                {linhas}
            </table>
        </body>
        </html>
        """

        caminho.write_text(html, encoding="utf-8")

    print(f"Boletins gerados em: {pasta_boletins}")


if __name__ == "__main__":
    gerar_boletins()