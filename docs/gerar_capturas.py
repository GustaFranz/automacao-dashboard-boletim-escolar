# -*- coding: utf-8 -*-
"""Gera capturas estaticas para documentacao do README."""

import sys
from pathlib import Path

PASTA_DOCS = Path(__file__).resolve().parent
PASTA_PROJETO = PASTA_DOCS.parent
sys.path.insert(0, str(PASTA_PROJETO))

from PIL import Image, ImageDraw, ImageFont

from src import consolidacao


PASTA_CAPTURAS = PASTA_DOCS / "capturas"


def _fonte(tamanho=16, negrito=False):
    """Carrega fonte do sistema ou usa padrao do Pillow."""
    candidatos = [
        "C:/Windows/Fonts/segoeuib.ttf" if negrito else "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/arialbd.ttf" if negrito else "C:/Windows/Fonts/arial.ttf",
    ]
    for caminho in candidatos:
        if Path(caminho).exists():
            return ImageFont.truetype(caminho, tamanho)
    return ImageFont.load_default()


def _fundo(largura, altura, cor="#f4f7fb"):
    """Cria imagem base com fundo claro."""
    imagem = Image.new("RGB", (largura, altura), cor)
    return imagem, ImageDraw.Draw(imagem)


def _card(draw, x, y, largura, altura, titulo, linhas, fonte_titulo, fonte_texto):
    """Desenha card branco com titulo e linhas de texto."""
    draw.rounded_rectangle(
        (x, y, x + largura, y + altura),
        radius=12,
        fill="white",
        outline="#d9e2ec",
        width=2,
    )
    draw.text((x + 20, y + 18), titulo, fill="#17324d", font=fonte_titulo)
    pos_y = y + 52
    for linha in linhas:
        draw.text((x + 20, pos_y), linha, fill="#334155", font=fonte_texto)
        pos_y += 24


def gerar_portal():
    """Gera captura do portal ficticio de login."""
    imagem, draw = _fundo(960, 640)
    titulo = _fonte(28, True)
    texto = _fonte(15)
    _card(
        draw,
        250,
        120,
        460,
        360,
        "Portal do Simulado",
        [
            "Colegio Caminhos do Futuro",
            "",
            "Email",
            "coordenacao@colegiocaminhosfuturo.local",
            "Senha",
            "********",
            "[ Entrar ]",
        ],
        titulo,
        texto,
    )
    imagem.save(PASTA_CAPTURAS / "01-portal-login.png")


def gerar_fontes():
    """Gera captura das tres fontes de dados simuladas."""
    imagem, draw = _fundo(960, 520)
    titulo = _fonte(22, True)
    texto = _fonte(14)
    blocos = [
        ("CSV - Simulado", ["simulado_6ano.csv", "Portal HTML local", "turma, aluno, disciplinas..."]),
        ("Excel - Provas", ["provas_6ano.xlsx", "Professores", "aba: Notas das Provas"]),
        ("PDF - Projetos", ["projeto_6ano.pdf", "Coordenacao", "tabela por turma e aluno"]),
    ]
    x = 30
    for nome, linhas in blocos:
        _card(draw, x, 70, 290, 380, nome, linhas, titulo, texto)
        x += 310
    imagem.save(PASTA_CAPTURAS / "02-fontes-dados.png")


def gerar_consolidado(notas):
    """Gera captura da base consolidada em formato tabular."""
    amostra = notas.head(8)[
        ["turma", "aluno", "disciplina", "nota_simulado", "nota_prova", "media", "situacao"]
    ]
    colunas = list(amostra.columns)
    largura_col = [130, 210, 150, 90, 90, 70, 100]
    largura = sum(largura_col) + 40
    altura = 420
    imagem, draw = _fundo(largura, altura)
    titulo = _fonte(20, True)
    cabecalho = _fonte(12, True)
    corpo = _fonte(11)
    draw.text((20, 16), "saidas/relatorios/notas_consolidadas.csv", fill="#17324d", font=titulo)
    y = 56
    x = 20
    for indice, coluna in enumerate(colunas):
        draw.rectangle((x, y, x + largura_col[indice], y + 28), fill="#17324d")
        draw.text((x + 6, y + 7), coluna, fill="white", font=cabecalho)
        x += largura_col[indice]
    y += 28
    for _, linha in amostra.iterrows():
        x = 20
        valores = [str(linha[c])[:24] for c in colunas]
        for indice, valor in enumerate(valores):
            draw.rectangle((x, y, x + largura_col[indice], y + 26), outline="#d9e2ec")
            draw.text((x + 6, y + 6), valor, fill="#1f2937", font=corpo)
            x += largura_col[indice]
        y += 26
    imagem.save(PASTA_CAPTURAS / "03-notas-consolidadas.png")


def gerar_boletim(notas):
    """Gera captura de boletim individual."""
    primeiro_aluno = notas["aluno"].iloc[0]
    tabela = notas[notas["aluno"] == primeiro_aluno]

    imagem, draw = _fundo(920, 620)
    titulo = _fonte(24, True)
    texto = _fonte(14)
    cabecalho = _fonte(12, True)
    corpo = _fonte(11)
    draw.text((24, 20), "Boletim Escolar - 2 Bimestre", fill="#17324d", font=titulo)
    draw.text((24, 58), f"Aluno: {tabela.iloc[0]['aluno']}", fill="#334155", font=texto)
    draw.text((24, 82), f"Turma: {tabela.iloc[0]['turma']}", fill="#334155", font=texto)
    colunas = ["Disciplina", "Simulado", "Prova", "Projeto", "Media", "Situacao"]
    larguras = [220, 80, 80, 80, 80, 110]
    y = 120
    x = 24
    for indice, nome in enumerate(colunas):
        draw.rectangle((x, y, x + larguras[indice], y + 28), fill="#17324d")
        draw.text((x + 8, y + 7), nome, fill="white", font=cabecalho)
        x += larguras[indice]
    y += 28
    for _, linha in tabela.iterrows():
        x = 24
        valores = [
            str(linha["disciplina"])[:28],
            str(linha["nota_simulado"]),
            str(linha["nota_prova"]),
            str(linha["nota_projeto"]),
            str(linha["media"]),
            str(linha["situacao"]),
        ]
        for indice, valor in enumerate(valores):
            draw.rectangle((x, y, x + larguras[indice], y + 24), outline="#d9e2ec")
            draw.text((x + 8, y + 5), valor, fill="#1f2937", font=corpo)
            x += larguras[indice]
        y += 24
    imagem.save(PASTA_CAPTURAS / "04-boletim-aluno.png")


def gerar_dashboard(notas):
    """Gera captura estatica do dashboard com dados reais."""
    turma = sorted(notas["turma"].unique())[0]
    dados = notas[notas["turma"] == turma]
    media_geral = dados["media"].mean()
    total_alunos = dados["aluno"].nunique()
    perc_rec = dados["situacao"].eq("Recuperacao").mean() * 100
    perc_acima = (dados["media"] >= 6).mean() * 100
    perc_abaixo = (dados["media"] < 6).mean() * 100
    media_disc = (
        dados.groupby("disciplina", as_index=False)["media"]
        .mean()
        .sort_values("media", ascending=False)
    )
    melhor = media_disc.iloc[0]
    pior = media_disc.iloc[-1]

    imagem, draw = _fundo(980, 720, "#ffffff")
    titulo = _fonte(26, True)
    texto = _fonte(14)
    metrica = _fonte(22, True)
    draw.text((24, 18), "Dashboard de Boletins Escolares", fill="#111827", font=titulo)
    draw.text((24, 52), f"Turma selecionada: {turma}", fill="#6b7280", font=texto)

    metricas = [
        ("Media geral", f"{media_geral:.1f}"),
        ("Total de alunos", str(total_alunos)),
        ("% em recuperacao", f"{perc_rec:.1f}%"),
        ("% acima da media", f"{perc_acima:.1f}%"),
        ("% abaixo da media", f"{perc_abaixo:.1f}%"),
    ]
    x = 24
    for rotulo, valor in metricas:
        draw.rounded_rectangle((x, 90, x + 175, 160), radius=10, fill="#f8fafc", outline="#e5e7eb")
        draw.text((x + 12, 102), rotulo, fill="#6b7280", font=texto)
        draw.text((x + 12, 126), valor, fill="#111827", font=metrica)
        x += 190

    draw.text(
        (24, 178),
        f"Melhor disciplina: {melhor['disciplina']} ({melhor['media']:.1f})  |  "
        f"Pior disciplina: {pior['disciplina']} ({pior['media']:.1f})",
        fill="#6b7280",
        font=texto,
    )

    grafico_top = 220
    grafico_base = 520
    max_media = max(10.0, media_disc["media"].max())
    barras = media_disc.head(8)
    largura_barra = 90
    espaco = 24
    x = 40
    for _, linha in barras.iterrows():
        altura = int((linha["media"] / max_media) * (grafico_base - grafico_top - 40))
        y_topo = grafico_base - altura
        draw.rectangle((x, y_topo, x + largura_barra, grafico_base), fill="#2563eb")
        draw.text((x, y_topo - 18), f"{linha['media']:.1f}", fill="#111827", font=texto)
        nome = str(linha["disciplina"])[:10]
        draw.text((x, grafico_base + 8), nome, fill="#374151", font=_fonte(10))
        x += largura_barra + espaco

    draw.text((24, 560), "Alunos em recuperacao (amostra)", fill="#111827", font=_fonte(16, True))
    recuperacao = dados[dados["situacao"] == "Recuperacao"].head(3)
    y = 590
    for _, linha in recuperacao.iterrows():
        draw.text(
            (24, y),
            f"{linha['aluno']} | {linha['disciplina']} | media {linha['media']}",
            fill="#334155",
            font=texto,
        )
        y += 22

    imagem.save(PASTA_CAPTURAS / "05-dashboard.png")


def gerar_progresso_png():
    """Gera PNG de progresso alinhado ao SVG atualizado."""
    etapas = [
        ("1_Dados", "Mapear fontes"),
        ("2_Portal", "Testar login"),
        ("3_RPA", "Automatizar"),
        ("4_Leitura", "Ler arquivos"),
        ("5_Medias", "Consolidar"),
        ("6_Boletins", "Gerar HTML"),
        ("7_Dashboard", "Painel"),
        ("8_v2", "Backlog"),
    ]
    largura, altura = 760, 118
    imagem, draw = _fundo(largura, altura, "#ffffff")
    titulo = _fonte(11, True)
    subtitulo = _fonte(9)
    centro = _fonte(12, True)
    posicoes = [47, 142, 237, 332, 427, 522, 617, 712]
    for indice, ((nome, desc), x) in enumerate(zip(etapas, posicoes)):
        if indice == 7:
            draw.ellipse((x - 26, 10, x + 26, 62), outline="#d1d5db", width=3)
            draw.text((x - 8, 30), "v2", fill="#9ca3af", font=centro)
        else:
            draw.ellipse((x - 26, 10, x + 26, 62), outline="#0d9488", width=5)
            draw.text((x - 6, 30), "OK", fill="#111827", font=_fonte(10, True))
        draw.text((x, 82), nome, fill="#111827", font=titulo, anchor="mm")
        draw.text((x, 96), desc, fill="#6b7280", font=subtitulo, anchor="mm")
    imagem.save(PASTA_DOCS / "progresso-etapas.png")


def gerar_todas():
    """Gera todas as capturas usadas no README."""
    PASTA_CAPTURAS.mkdir(parents=True, exist_ok=True)
    notas = consolidacao.consolidar_notas()
    gerar_portal()
    gerar_fontes()
    gerar_consolidado(notas)
    gerar_boletim(notas)
    gerar_dashboard(notas)
    gerar_progresso_png()
    print(f"Capturas salvas em: {PASTA_CAPTURAS}")


if __name__ == "__main__":
    gerar_todas()
