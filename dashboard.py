import plotly.express as px
import streamlit as st

from src import consolidacao


st.set_page_config(page_title="Dashboard de Boletins", layout="wide")

st.title("Dashboard de Boletins Escolares")
st.caption("Colegio Caminhos do Futuro - dados ficticios")

notas = consolidacao.consolidar_notas()

turmas = sorted(notas["turma"].unique())
turma_selecionada = st.sidebar.selectbox("Turma", turmas)

dados = notas[notas["turma"] == turma_selecionada]

media_geral = dados["media"].mean()
total_alunos = dados["aluno"].nunique()
percentual_recuperacao = dados["situacao"].eq("Recuperacao").mean() * 100
percentual_acima = (dados["media"] >= 6).mean() * 100
percentual_abaixo = (dados["media"] < 6).mean() * 100

media_disciplina = (
    dados.groupby("disciplina", as_index=False)["media"]
    .mean()
    .sort_values("media", ascending=False)
)
melhor = media_disciplina.iloc[0]
pior = media_disciplina.iloc[-1]

col1, col2, col3 = st.columns(3)
col1.metric("Media geral", f"{media_geral:.1f}")
col2.metric("Total de alunos", total_alunos)
col3.metric("% em recuperacao", f"{percentual_recuperacao:.1f}%")

col4, col5 = st.columns(2)
col4.metric("% acima da media", f"{percentual_acima:.1f}%")
col5.metric("% abaixo da media", f"{percentual_abaixo:.1f}%")

st.caption(
    f"Melhor disciplina: {melhor['disciplina']} ({melhor['media']:.1f}) · "
    f"Pior disciplina: {pior['disciplina']} ({pior['media']:.1f})"
)

fig = px.bar(
    media_disciplina,
    x="disciplina",
    y="media",
    title="Media por disciplina",
    text_auto=".1f",
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Alunos em recuperacao")
recuperacao = dados[dados["situacao"] == "Recuperacao"]
st.dataframe(recuperacao[["aluno", "disciplina", "media"]], use_container_width=True)