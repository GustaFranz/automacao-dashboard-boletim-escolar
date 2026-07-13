# Roadmap de melhorias — School Data Pipeline

Documento de refer�ncia para evolu��o do projeto ap�s a **v1 conclu�da**.

Cada melhoria descreve: **o que �**, **por que fazer**, **como fazer**, **recursos**, **conceitos Python** e **o que estudar**.

---

## Diagn�stico do estado atual (v1)

O projeto cumpre o escopo da v1: RPA do portal ? leitura de 3 formatos ? consolida��o com m�dia ponderada ? boletins HTML ? dashboard Streamlit.

### Pontos fortes

- Separa��o razo�vel por responsabilidade (`leitor_*`, `consolidacao`, `boletins`, `automacao_portal`)
- Uso correto de `pathlib`, `pandas.melt`, `merge`, `groupby`
- Documenta��o narrativa forte (`README.md`, `detalhamento.md`)

### Fragilidades identificadas

| �rea | Situa��o atual |
|------|----------------|
| Configura��o | Caminhos, credenciais, pesos e coordenadas espalhados/hardcoded |
| Reuso de dados | `consolidar_notas()` � recalculado em `boletins.py` e `dashboard.py` |
| RPA | Coordenadas fixas; sem captura de tela nem log estruturado |
| Robustez | `inner merge` descarta alunos sem nota em alguma fonte, sem aviso |
| Qualidade de c�digo | Sem testes, sem docstrings padronizadas, arquivos tempor�rios no repo |
| Depend�ncias | `reportlab` listado mas n�o usado |
| Pacote Python | `src/` sem `__init__.py`, sem vers�o formal do projeto |

---

## Mapa de vers�es (resumo)

| Vers�o | Foco principal |
|--------|----------------|
| **v1.2** | Organizar: config centralizada, single source of truth, limpeza, deps, erros |
| **v1.3** | Confiar: valida��o, logging, screenshots RPA, CLI, pacote, docstrings |
| **v1.4** | Apresentar: boletim visual, regras pedag�gicas isoladas |
| **v2** | Produto confi�vel: testes, PDF, templates, config externa, dashboard rico, RPA robusto |
| **Alto n�vel** | Plataforma: BD, API, agendamento, multi-escola, LGPD, analytics |

---

## N�vel b�sico � v1.2, v1.3, v1.4

Melhorias pequenas, de baixo risco, que refinam o que j� existe. Prioridade para implementa��o imediata.

---

### B1 � Centralizar configura��o do projeto

**Vers�o sugerida:** v1.2

**O que �**  
Um �nico lugar com caminhos de pastas, nomes de arquivos, pesos da m�dia, nota m�nima, credenciais de demo e par�metros do RPA.

**Por que fazer**  
Hoje cada m�dulo repete `pasta_projeto = Path(__file__).resolve().parent.parent`. Pesos e regra de aprova��o est�o s� em `consolidacao.py`. Qualquer mudan�a exige ca�ar valores em v�rios arquivos.

**Como fazer**  
Criar `src/config.py` (ou `config/settings.py`) com constantes e fun��es que retornam `Path`:

```python
PASTA_PROJETO = Path(__file__).resolve().parent.parent
PASTA_SIMULADOS = PASTA_PROJETO / "dados" / "simulados"
PESO_SIMULADO = 10
PESO_PROVA = 10
PESO_PROJETO = 5
NOTA_MINIMA = 6.0
```

**Recursos**  
`pathlib.Path`, constantes em mai�sculas, eventualmente `dataclasses` para agrupar config.

**Python para dominar**  
`Path`, `__file__`, imports entre m�dulos, `dataclass` (opcional).

**Estudar**  
Pathlib, organiza��o de pacotes Python, princ�pio DRY.

---

### B2 � Evitar recalcular consolida��o tr�s vezes

**Vers�o sugerida:** v1.2

**O que �**  
Hoje o fluxo recalcula tudo em momentos diferentes:

- `main.py` ? `consolidar_notas()` + salva CSV
- `boletins.py` ? chama `consolidar_notas()` de novo
- `dashboard.py` ? chama `consolidar_notas()` de novo

**Por que fazer**  
Desperd�cio de processamento, risco de inconsist�ncia (boletim e dashboard podem divergir do CSV salvo) e dificulta debug.

**Como fazer**  
Duas op��es simples:

1. **Ler o CSV salvo** em `boletins.py` e `dashboard.py` via `pd.read_csv()`
2. **Passar o DataFrame** como par�metro: `gerar_boletins(notas)`

Padr�o recomendado:

```python
def gerar_boletins(notas=None):
    if notas is None:
        notas = pd.read_csv(caminho_consolidado)
```

Criar fun��o reutiliz�vel `carregar_notas_consolidadas()`.

**Recursos**  
`pandas.read_csv`, par�metros opcionais.

**Python para dominar**  
Par�metros default, separa��o �gerar� vs �carregar�, fluxo de dados entre fun��es.

**Estudar**  
Pipeline de dados simples; padr�o �single source of truth�.

---

### B3 � Valida��o b�sica antes da consolida��o

**Vers�o sugerida:** v1.2 ou v1.3

**O que �**  
Checagens simples: arquivos existem? colunas esperadas? quantos alunos sumiram no merge?

**Por que fazer**  
O `inner merge` em `consolidacao.py` elimina silenciosamente quem n�o tem nota nas tr�s fontes. Na pr�tica escolar, isso deveria gerar alerta, n�o sumi�o quieto.

**Como fazer**  
Antes/depois do merge:

- Contar linhas em cada fonte
- Comparar conjuntos de `(turma, aluno, disciplina)` com `set` ou `merge(..., indicator=True)`
- `print` ou `logging.warning` com resumo: �3 registros sem nota de projeto�

**Recursos**  
`DataFrame.shape`, `merge(..., how='outer', indicator=True)`, `value_counts()`, `isna().sum()`.

**Python para dominar**  
Conjuntos (`set`), compara��o de DataFrames, tratamento de dados faltantes.

**Estudar**  
Pandas merge (inner/outer/left), data quality b�sica.

---

### B4 � Logging simples em vez de s� `print`

**Vers�o sugerida:** v1.3

**O que �**  
Substituir/complementar `print()` por `logging` com n�veis (INFO, WARNING, ERROR).

**Por que fazer**  
O Desafio 3 pede �registro visual ou log da execu��o�, mas o RPA hoje s� imprime movimenta��o de arquivo. Logs ajudam a rastrear falhas do PyAutoGUI, leitura de PDF e gera��o de boletins.

**Como fazer**  
Criar `src/log_config.py`:

```python
import logging

def configurar_log():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[
            logging.FileHandler("saidas/relatorios/execucao.log"),
            logging.StreamHandler(),
        ],
    )
```

Usar `logger.info("CSVs movidos com sucesso")` nos m�dulos.

**Recursos**  
M�dulo `logging` da stdlib.

**Python para dominar**  
`logging.basicConfig`, `getLogger`, handlers, n�veis de log.

**Estudar**  
[logging � Python docs](https://docs.python.org/3/library/logging.html)

---

### B5 � Capturas de tela no RPA

**Vers�o sugerida:** v1.3

**O que �**  
Salvar screenshots em `saidas/prints/` em etapas-chave: ap�s login, ap�s cada download.

**Por que fazer**  
Est� nos crit�rios de aceite do Desafio 3 e no README como evid�ncia; a pasta existe na estrutura, mas `automacao_portal.py` n�o grava imagens.

**Como fazer**  

```python
import pyautogui
from datetime import datetime

def capturar(nome):
    pasta_prints.mkdir(parents=True, exist_ok=True)
    arquivo = pasta_prints / f"{nome}_{datetime.now():%Y%m%d_%H%M%S}.png"
    pyautogui.screenshot(str(arquivo))
```

Chamar ap�s login e ap�s cada `mover_csv_baixado`.

**Recursos**  
`pyautogui.screenshot()`, `datetime`, `Path.mkdir`.

**Python para dominar**  
Nomes de arquivo com timestamp, organiza��o de pastas de sa�da.

**Estudar**  
PyAutoGUI screenshot; boas pr�ticas de evid�ncia em automa��o.

---

### B6 � Docstrings e tipagem leve

**Vers�o sugerida:** v1.3

**O que �**  
Documentar objetivo, par�metros e retorno em cada fun��o exportada; adicionar type hints onde ajuda.

**Por que fazer**  
Facilita revisitar etapas densas sem depender s� da mem�ria. Alinha com arquitetura modular.

**Como fazer**  

```python
def consolidar_notas() -> pd.DataFrame:
    """Combina simulado, prova e projeto e calcula media ponderada.

    Returns:
        DataFrame com colunas turma, aluno, disciplina, notas e situacao.
    """
```

**Recursos**  
Docstrings, `typing` (opcional: `from __future__ import annotations`).

**Python para dominar**  
Conven��es de documenta��o, anota��es de tipo b�sicas.

**Estudar**  
PEP 257 (docstrings), PEP 484 (type hints introdut�rio).

---

### B7 � Limpar arquivos tempor�rios e organizar auxiliares

**Vers�o sugerida:** v1.2

**O que �**  
Remover ou mover para pasta adequada:

- `src/tempCodeRunnerFile.py`
- `tempCodeRunnerFile.py` (raiz)
- Mover `auxiliar.py` para `scripts/calibrar_coordenadas.py`

**Por que fazer**  
Arquivos de editor poluem o repo, confundem quem rel� o projeto e podem ser commitados por engano.

**Como fazer**  

- Deletar tempor�rios
- Mover `auxiliar.py` para `scripts/` com README curto de uso
- Adicionar `tempCodeRunnerFile.py` ao `.gitignore`

**Recursos**  
`.gitignore`, organiza��o `scripts/`.

---

### B8 � Melhorar visual dos boletins HTML

**Vers�o sugerida:** v1.3 ou v1.4

**O que �**  
CSS simples, ordem fixa das disciplinas, acentua��o correta (�M�dia�, �Situa��o�, �Recupera��o�), layout mais leg�vel para impress�o.

**Por que fazer**  
Boletim atual � HTML cru com `border="1"`. Para contexto escolar e inclus�o (baixa leitura, TDAH), hierarquia visual e contraste importam.

**Como fazer**  

- Arquivo `templates/boletim_base.html` com placeholders
- CSS com fonte grande, zebra striping, `@media print`
- Lista ordenada de disciplinas em `config.py`
- `string.Template` ou f-strings com template externo

**Recursos**  
HTML/CSS b�sico, `string.Template`.

**Python para dominar**  
Leitura de template com `Path.read_text()`, formata��o de strings.

**Estudar**  
CSS para impress�o (`@media print`), acessibilidade visual b�sica (contraste, tamanho de fonte).

---

### B9 � `main.py` com op��es de execu��o (CLI m�nima)

**Vers�o sugerida:** v1.3

**O que �**  
Permitir rodar s� uma etapa: `--somente-rpa`, `--somente-consolidacao`, `--somente-boletins`.

**Por que fazer**  
Hoje, para testar boletins voc� recalcula tudo incluindo RPA (lento e fr�gil). Facilita debug e estudo modular.

**Como fazer**  

```python
parser.add_argument("--etapa", choices=["tudo", "rpa", "consolidacao", "boletins"])
```

**Recursos**  
`argparse` (stdlib).

**Python para dominar**  
CLI simples, `if __name__ == "__main__"`.

**Estudar**  
Argparse tutorial oficial.

---

### B10 � Fixar vers�es no `requirements.txt`

**Vers�o sugerida:** v1.2

**O que �**  
De `pandas` para `pandas==2.x.x` (vers�es testadas no ambiente local).

**Por que fazer**  
Evita que atualiza��o de biblioteca quebre leitura de Excel/PDF ou Streamlit no futuro.

**Como fazer**  

```bash
pip freeze > requirements-lock.txt
```

Ou pinar manualmente as principais depend�ncias.

**Recursos**  
`pip freeze`, ambientes virtuais.

**Estudar**  
Gerenciamento de depend�ncias em Python (venv + requirements).

---

### B11 � Resolver `reportlab` �rf�o

**Vers�o sugerida:** v1.2 (remover) ou v2 (usar)

**O que �**  
`reportlab` est� em `requirements.txt` mas n�o � usado em lugar nenhum.

**Por que fazer**  
Depend�ncia fantasma aumenta instala��o sem benef�cio.

**Como fazer**  

- **v1.2:** remover do `requirements.txt`
- **v2:** usar para exporta��o PDF (ver I2)

---

### B12 � `src/__init__.py` e exports expl�citos

**Vers�o sugerida:** v1.3

**O que �**  
Tornar `src` um pacote Python formal.

**Por que fazer**  
Permite `from src import consolidar_notas` e evita surpresas de import.

**Como fazer**  

```python
# src/__init__.py
from .consolidacao import consolidar_notas, salvar_relatorio_final
```

**Recursos**  
Pacotes Python, `__init__.py`.

**Estudar**  
Imports absolutos vs relativos.

---

### B13 � Separar regra pedag�gica em fun��es puras

**Vers�o sugerida:** v1.3

**O que �**  
Extrair de `consolidacao.py` fun��es como:

- `converter_nota_projeto(nota) -> float`
- `calcular_media_ponderada(sim, prova, proj) -> float`
- `classificar_situacao(media) -> str`

**Por que fazer**  
Separa �ler e juntar dados� de �aplicar regra escolar�. Facilita testes manuais e automatizados.

**Como fazer**  
M�dulo `src/regras_pedagogicas.py` sem depend�ncia de arquivos � s� n�meros e strings.

**Recursos**  
Fun��es puras, m�dulo sem side effects.

**Python para dominar**  
Fun��es pequenas, responsabilidade �nica.

**Estudar**  
Separation of concerns.

---

### B14 � Mensagens de erro mais amig�veis nos leitores

**Vers�o sugerida:** v1.2

**O que �**  
Quando `FileNotFoundError` ou PDF sem tabela, indicar pasta esperada e exemplos de nome de arquivo.

**Por que fazer**  
Erros atuais s�o corretos mas pouco orientadores para quem est� aprendendo ou rodando em m�quina nova.

**Como fazer**  

```python
raise FileNotFoundError(
    f"Nenhum simulado em {pasta_simulados}. "
    f"Execute o RPA ou coloque arquivos simulado_*.csv"
)
```

---

## N�vel intermedi�rio � caminho para v2

Cada item sozinho ainda � v1.x �grande�. Juntando v�rios deles, voc� tem um **v2** coerente.

---

### I1 � Testes automatizados com pytest

**O que �**  
Testes que verificam regras de m�dia, leitura de arquivos de exemplo e gera��o de boletim.

**Por que fazer**  
Backlog expl�cito no Desafio 8. Sem testes, qualquer refatora��o vira medo.

**Como fazer**  

```text
tests/
  test_regras_pedagogicas.py
  test_consolidacao.py
  fixtures/   # CSV/Excel/PDF m�nimos
```

```python
def test_media_ponderada():
    assert calcular_media(8.0, 7.0, 4.0) == pytest.approx(7.2, abs=0.1)
```

**Recursos**  
`pytest`, `pytest.approx`, fixtures, `tmp_path`.

**Python para dominar**  
`assert`, fixtures, arquivos tempor�rios com `tmp_path`.

**Estudar**  
pytest Getting Started; testes de fun��es puras antes de integra��o.

**Combina com**  
B13 (regras isoladas).

---

### I2 � Exporta��o de boletins em PDF

**O que �**  
Gerar PDF al�m do HTML, pronto para impress�o/arquivo.

**Por que fazer**  
Backlog do Desafio 8; contexto escolar real pede PDF. `reportlab` j� est� listado.

**Como fazer � duas rotas**

| Abordagem | Pr�s | Contras |
|-----------|------|---------|
| **ReportLab** | Controle total no Python | Layout manual (tabelas, fontes) |
| **WeasyPrint / pdfkit** | HTML ? PDF reaproveita B8 | Mais depend�ncias/sistema |

Fluxo modular:

1. `boletins_html.py` � gera HTML
2. `exportacao_pdf.py` � converte HTML ou monta PDF
3. `boletins.py` � orquestra

**Recursos**  
`reportlab.platypus` (Table, Paragraph) ou `weasyprint.HTML(string).write_pdf()`.

**Python para dominar**  
Pipeline em etapas, paths de sa�da, arquivos bin�rios.

**Estudar**  
ReportLab User Guide (tabelas); ou WeasyPrint para HTML?PDF.

---

### I3 � Sistema de templates reutiliz�veis

**O que �**  
Separar estrutura (layout) de conte�do (notas do aluno) para boletins, relat�rios e futuros e-mails.

**Por que fazer**  
HTML est� embutido em f-string dentro de `gerar_boletins()`. Escalar visual ou criar varia��es (TEA, vers�o simplificada) fica dif�cil.

**Como fazer**  

- Pasta `templates/`
- `Jinja2` para placeholders: `{{ aluno }}`, loop `{% for disciplina in notas %}`
- Par�metro `versao_acessivel=true` ? fonte maior, menos colunas

**Recursos**  
`Jinja2.Template`, `Environment(loader=FileSystemLoader(...))`.

**Python para dominar**  
Renderiza��o de templates, context dict, separa��o dados/apresenta��o.

**Estudar**  
Jinja2 docs.

---

### I4 � Configura��o externa (YAML/JSON)

**O que �**  
Pesos, nota m�nima, disciplinas, turmas e caminhos em `config/escola.yaml`.

**Por que fazer**  
Permite mudar regra pedag�gica sem editar c�digo; prepara multi-escola no futuro.

**Como fazer**  

```yaml
medias:
  peso_simulado: 10
  peso_prova: 10
  peso_projeto: 5
  nota_minima: 6.0
disciplinas:
  - Lingua Portuguesa
  - Matematica
```

Carregar com `import yaml` ou `json.load`.

**Recursos**  
`PyYAML` ou JSON da stdlib, `dataclasses` para validar estrutura.

**Estudar**  
Config-driven applications; opcionalmente Pydantic (I6).

---

### I5 � RPA mais robusto: Selenium ou Playwright

**O que �**  
Trocar cliques por coordenada por automa��o baseada em elementos HTML (bot�o �Baixar CSV�, link da turma).

**Por que fazer**  
PyAutoGUI depende de resolu��o 1920�1080, escala 125%, Chrome maximizado. Para portal **local em HTML**, Selenium/Playwright � muito mais est�vel.

**Como fazer**  

```python
driver.get(portal_login.as_uri())
driver.find_element(By.LINK_TEXT, "Abrir notas").click()
```

**Recursos**  
`selenium` ou `playwright`, seletores CSS/XPath, `webdriver.ChromeOptions`.

**Python para dominar**  
Esperas expl�citas (`WebDriverWait`), exce��es de elemento n�o encontrado.

**Estudar**  
Selenium com Python (ou Playwright Python).

**Nota**  
Manter `automacao_portal.py` como m�dulo hist�rico e criar `automacao_portal_selenium.py`.

---

### I6 � Valida��o de schema com Pydantic

**O que �**  
Modelar cada registro de nota como objeto validado: turma, aluno, disciplina, notas entre 0 e 10.

**Por que fazer**  
PDFs e Excel podem trazer string vazia, �N/A� ou nota fora da escala. Pandas aceita e o erro aparece tarde.

**Como fazer**  

```python
class RegistroNota(BaseModel):
    turma: str
    aluno: str
    disciplina: str
    nota_simulado: float = Field(ge=0, le=10)
```

**Recursos**  
`pydantic.BaseModel`, `Field`, validators.

**Estudar**  
Pydantic V2 docs.

---

### I7 � Dashboard v2: filtros e visual avan�ado

**O que �**  
Expandir `dashboard.py` com:

- Filtro por disciplina e aluno
- Comparativo entre turmas
- Gr�fico de distribui��o (histograma de m�dias)
- Indicador por bimestre (quando houver hist�rico)
- Tema visual consistente

**Por que fazer**  
Backlog Desafio 8. Painel atual � funcional mas enxuto.

**Como fazer**  

- `st.multiselect` para disciplinas
- `plotly.express.histogram`, `px.line` para evolu��o futura
- `st.cache_data` em `carregar_notas()` para performance
- CSS custom via `st.markdown(unsafe_allow_html=True)`

**Recursos**  
Streamlit widgets, Plotly Express, cache do Streamlit.

**Estudar**  
Streamlit docs (caching, session state); Plotly chart types.

---

### I8 � M�ltiplos arquivos por professor/turma (provas)

**O que �**  
Em vez de um `provas_6ano.xlsx` central, simular `provas_port_6A.xlsx`, `provas_mat_6A.xlsx`, etc.

**Por que fazer**  
Backlog Desafio 8; aproxima fluxo real onde cada professor entrega planilha.

**Como fazer**  

- `ler_provas()` j� usa `glob("provas_*.xlsx")` � generalizar padr�o e metadados no nome
- Normalizar colunas diferentes entre professores
- M�dulo `normalizacao_provas.py` para padronizar nomes de disciplina

**Recursos**  
`glob`, `rename` de colunas, dicion�rios de mapeamento.

**Estudar**  
ETL leve: ingest�o ? normaliza��o ? consolida��o.

---

### I9 � Pipeline �nico orquestrado

**O que �**  
M�dulo `src/pipeline.py` que define etapas com status, tempo e falha controlada.

**Por que fazer**  
`main.py` hoje � linear sem try/except. Se o RPA falha, o resto nem roda � ou pior, roda com dados velhos.

**Como fazer**  

```python
def executar_pipeline(pular_rpa=False):
    etapas = [
        ("rpa", executar_automacao),
        ("consolidacao", lambda: salvar_relatorio_final(consolidar_notas())),
        ("boletins", gerar_boletins),
    ]
```

Com logging e op��o de continuar se CSV j� existir.

**Recursos**  
Fun��es de ordem superior, exce��es customizadas, logging.

**Estudar**  
Padr�es de pipeline; introdu��o a Prefect/Airflow.

---

### I10 � CI b�sico (GitHub Actions)

**O que �**  
Workflow que roda pytest a cada push.

**Por que fazer**  
Garante que refatora��es n�o quebrem consolida��o silenciosamente.

**Como fazer**  
`.github/workflows/test.yml` com `pip install -r requirements.txt` e `pytest`.

**Recursos**  
GitHub Actions, YAML de workflow.

**Estudar**  
CI para projetos Python pequenos.

---

### I11 � Adapta��es de inclus�o (TEA, TDAH, baixa leitura)

**O que �**  
Vers�es alternativas de boletim e dashboard: menos informa��o por tela, �cones de situa��o, cores consistentes, modo �foco�.

**Por que fazer**  
Contexto educacional pede materiais adaptados; boletim e dashboard atuais s�o neutros mas n�o adaptados.

**Como fazer**  

- Template `boletim_simples.html`: s� disciplina + m�dia + �cone
- Dashboard: toggle �Modo simplificado� (menos m�tricas, fonte maior)
- PDF com espa�amento amplo

**Recursos**  
Templates m�ltiplos (I3), CSS, par�metros de exporta��o.

**Estudar**  
Design universal de leitura; WCAG contraste b�sico.

---

### Crit�rio �quando vira v2?�

**v2** quando houver, no m�nimo:

| Pilar | Melhorias |
|-------|-----------|
| Confiabilidade | I1 testes + I6 valida��o + B3/B4 logging |
| Entrega | I2 PDF + I3 templates + B8 visual |
| Dados | I4 config externa + I8 multi-arquivo |
| Interface | I7 dashboard avan�ado |
| Automa��o | I5 RPA por browser driver (ou I9 pipeline s�lido) |

---

## N�vel alto � vis�o de produto / sistema escolar

Horizontes que transformam o projeto de �primeira automa��o� em **plataforma**. N�o � prioridade imediata.

---

### A1 � Arquitetura em camadas formal

**O que �**  
Reorganizar em camadas expl�citas:

```text
dominio/        # regras pedag�gicas puras
dados/          # leitores e reposit�rios
aplicacao/      # pipeline, casos de uso
apresentacao/   # boletins, dashboard, CLI
infra/          # RPA, logging, config
```

**Por que fazer**  
Escala para novas fontes e novas sa�das sem reescrever tudo.

**Estudar**  
Clean Architecture simplificada; arquitetura escal�vel em Python.

---

### A2 � Banco de dados e hist�rico multi-bimestre

**O que �**  
SQLite ou PostgreSQL com tabelas: alunos, turmas, avaliacoes, bimestres, notas.

**Por que fazer**  
CSV �nico sobrescreve hist�rico. Coordena��o real precisa comparar bimestres.

**Recursos**  
`sqlite3`, `SQLAlchemy`, ou `DuckDB`.

**Estudar**  
Modelagem relacional b�sica; migrations com Alembic.

---

### A3 � API REST (FastAPI)

**O que �**  
Backend que exp�e: `/notas/consolidadas`, `/boletim/{aluno_id}`, `/turmas/{id}/indicadores`.

**Por que fazer**  
Desacopla dashboard de leitura local; permite integra��o com outros sistemas.

**Recursos**  
`FastAPI`, `uvicorn`, Pydantic schemas.

**Estudar**  
FastAPI tutorial; OpenAPI.

---

### A4 � Frontend web completo

**O que �**  
Interface React/Vue ou Streamlit multi-p�gina profissional com autentica��o.

**Por que fazer**  
Streamlit � �timo para MVP; produto escolar costuma pedir UX custom e perfis (coordena��o vs professor).

**Estudar**  
Streamlit multipage apps como meio-termo; depois FastAPI + frontend.

---

### A5 � Orquestra��o agendada (Prefect / Airflow)

**O que �**  
Rodar pipeline automaticamente em hor�rio definido.

**Por que fazer**  
Automa��o de verdade = sem rodar `python main.py` manualmente.

**Recursos**  
Prefect 2.x (mais simples) ou Apache Airflow.

**Estudar**  
Workflow scheduling; retry e alertas.

---

### A6 � Integra��o com sistemas reais

**O que �**  
Conectores para Google Sheets, Microsoft 365, APIs de secretaria digital.

**Por que fazer**  
Portal HTML fict�cio � excelente para aprendizado; produ��o exige fontes reais (com LGPD e permiss�es).

**Estudar**  
OAuth, APIs Google; LGPD e tratamento de dados de menores.

---

### A7 � Analytics preditivo

**O que �**  
Modelos que estimam risco de recupera��o com base em hist�rico.

**Por que fazer**  
Dashboard reativo ? coordena��o preventiva.

**Recursos**  
`scikit-learn`, features por aluno/disciplina.

**Estudar**  
ML tabular b�sico; �tica em dados educacionais.

---

### A8 � Multi-escola e multi-tenant

**O que �**  
Um deploy atende v�rias escolas com config e dados isolados.

**Estudar**  
Multi-tenancy patterns; config por tenant.

---

### A9 � Deploy em nuvem

**O que �**  
Dashboard e API em Render, Railway, AWS ou Azure; RPA em VM dedicada.

**Estudar**  
Docker, vari�veis de ambiente, secrets.

---

### A10 � Governan�a, auditoria e LGPD

**O que �**  
Trilha de quem gerou boletim, quando, com quais dados; anonimiza��o para demos p�blicas.

**Estudar**  
LGPD aplicada a educa��o; logs de auditoria.

---

## Prioriza��o sugerida

### Fase 1 � Estudo (relat�rio e leitura do c�digo)

1. Ler este roadmap por vers�o
2. Reler `consolidacao.py`, `boletins.py`, `automacao_portal.py` com B1�B5 em mente
3. Anotar d�vidas por m�dulo

### Fase 2 � Implementa��o (�nfase b�sica)

**Primeiro pacote (m�ximo retorno, m�nimo risco):**

1. B1 + B2 + B7 + B14 ? base s�lida **v1.2**
2. B3 + B4 + B5 ? confiabilidade **v1.3**
3. B13 ? prepara I1 (testes)
4. Intermedi�ria opcional: I3 (templates) antes de I2 (PDF)

### Trilha de estudo alinhada ao c�digo

| Ordem | Tema | Para implementar |
|-------|------|------------------|
| 1 | Pathlib + organiza��o de pacotes | B1, B7, B12 |
| 2 | Pandas merge/valida��o | B2, B3 |
| 3 | logging | B4 |
| 4 | argparse | B9 |
| 5 | Fun��es puras + pytest | B13, I1 |
| 6 | Jinja2 | I3, B8 |
| 7 | ReportLab ou WeasyPrint | I2 |
| 8 | Selenium/Playwright | I5 |
| 9 | Streamlit cache + widgets | I7 |

---

## Riscos a monitorar

1. **`inner merge`** � qualquer refatora��o deve documentar ou reportar perdas de registros
2. **RPA** � melhorias b�sicas (screenshot, log) n�o removem fragilidade de coordenadas; I5 � o salto real
3. **Duplica��o de consolida��o** � corrigir cedo (B2) evita bugs fantasmas no dashboard
4. **Dados no `.gitignore`** � `dados/simulados/*.csv` e `saidas/` ignorados: testes precisar�o de `fixtures/` versionadas (I1)
5. **Inclus�o** � I11 pode come�ar j� na v1.4 com template simples

---

## Checklist por vers�o

### v1.2

- [ ] B1 � Centralizar configura��o
- [ ] B2 � Single source of truth (CSV)
- [ ] B7 � Limpar arquivos tempor�rios
- [ ] B10 � Fixar vers�es no requirements
- [ ] B11 � Resolver reportlab �rf�o
- [ ] B14 � Mensagens de erro amig�veis

### v1.3

- [ ] B3 � Valida��o antes da consolida��o
- [ ] B4 � Logging estruturado
- [ ] B5 � Screenshots no RPA
- [ ] B6 � Docstrings e type hints
- [ ] B9 � CLI no main.py
- [ ] B12 � `src/__init__.py`
- [ ] B13 � Regras pedag�gicas isoladas

### v1.4

- [ ] B8 � Boletins HTML com CSS e acessibilidade b�sica

### v2 (conjunto de intermedi�rias)

- [ ] I1 � Testes com pytest
- [ ] I2 � Exporta��o PDF
- [ ] I3 � Templates Jinja2
- [ ] I4 � Config externa YAML/JSON
- [ ] I5 � RPA Selenium/Playwright
- [ ] I6 � Valida��o Pydantic
- [ ] I7 � Dashboard avan�ado
- [ ] I8 � M�ltiplos arquivos de prova
- [ ] I9 � Pipeline orquestrado
- [ ] I10 � CI GitHub Actions
- [ ] I11 � Adapta��es de inclus�o

---

## Refer�ncias no reposit�rio

- [detalhamento.md](../detalhamento.md) � desafios e crit�rios de aceite da v1
- [README.md](../README.md) � vis�o geral e como executar
- Desafio 8 em `detalhamento.md` � backlog original que originou este roadmap
