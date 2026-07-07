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

col1, col2, col3 = st.columns(3)
col1.metric("Media geral", f"{media_geral:.1f}")
col2.metric("Total de alunos", total_alunos)
col3.metric("% em recuperacao", f"{percentual_recuperacao:.1f}%")

media_disciplina = (
    dados.groupby("disciplina", as_index=False)["media"]
    .mean()
    .sort_values("media", ascending=False)
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