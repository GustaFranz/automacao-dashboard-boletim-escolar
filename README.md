# Automação — Dashboard e Boletim Escolar

Projeto em Python para consolidar notas de simulado, provas e projeto pedagógico, calcular médias ponderadas, gerar boletins e montar um dashboard escolar.

**Status:** em construção — etapas 1 a 4 concluídas; **5_Médias** em andamento.

## Por que este projeto existe

Esta é minha **primeira automação** em Python.

Depois de um primeiro contato com automação (inspirado por material introdutório da Hashtag Treinamentos), quis aplicar o que estava aprendendo em algo ligado à minha rotina em sala de aula. Em vez de um exemplo genérico, escolhi simular uma situação que coordenação e professores reconhecem: juntar notas de fontes diferentes, calcular médias e transformar tudo em boletins e indicadores.

O foco aqui não é substituir um sistema escolar real, e sim **praticar automação com um contexto educacional fictício**, próximo da realidade do dia a dia.

## O que o projeto faz (visão geral)

Simula a rotina de uma coordenação escolar com **automação ponta a ponta**:

1. **Automatizar o portal** — com PyAutoGUI, o sistema acessa o portal local, faz login e baixa os CSVs de simulado simulando a interação humana (RPA).
2. **Processar os dados** — lê notas de CSV, Excel e PDF e consolida tudo em uma base única.
3. **Aplicar regras pedagógicas** — calcula médias ponderadas e define aprovação ou recuperação.
4. **Gerar entregas** — produz boletins individuais e um dashboard interativo com indicadores da turma.

**Escola fictícia:** Colégio Caminhos do Futuro  
**Turmas:** 6º, 7º e 8º ano matutino

> Cenário inspirado na rotina escolar: várias fontes de nota, portal sem API e tarefas repetitivas que podem ser automatizadas.

## Progresso

**4 de 8 etapas concluídas** · etapa **5_Médias** em andamento (20%)

<p align="center">
  <img src="docs/progresso-etapas.svg" alt="Progresso: 1_Dados, 2_Portal, 3_RPA e 4_Leitura concluídos; 5_Médias em andamento; demais pendentes" width="760">
</p>

| Situação | Significado |
|----------|-------------|
| anel fechado ✓ | concluído |
| anel parcial (%) | em andamento |
| anel vazio | pendente |
| anel tracejado | backlog |

Detalhes de cada etapa em **[detalhamento.md](detalhamento.md)**.

## Aprendizados (até aqui)

- Primeira automação em Python: o fluxo parecia complexo no início, mas repetir funções e mapear coordenadas com PyAutoGUI foi tornando o processo compreensível.

Registro completo por desafio em **[detalhamento.md](detalhamento.md)**.

## Automação RPA — evidências (Desafio 3)

O script [`src/automacao_portal.py`](src/automacao_portal.py) abre o portal no Chrome, faz login, navega pelas três séries e aciona o download dos CSVs de simulado.

### Ambiente calibrado

| Item | Valor |
|------|-------|
| Resolução do monitor | 1920×1080 |
| Escala do Windows | 125% (1536×864 lógico) |
| Navegador | Google Chrome maximizado |
| Zoom do navegador | 100% |

> As coordenadas do PyAutoGUI foram mapeadas nesse ambiente. Se o fluxo falhar em outra máquina, ajuste resolução, escala ou zoom antes de recalibrar.

### Demonstração

<table>
  <tr>
    <td width="50%" align="center"><strong>Mapeamento de coordenadas</strong></td>
    <td width="50%" align="center"><strong>Fluxo completo</strong></td>
  </tr>
  <tr>
    <td width="50%"><img src="gifs/rpa-mapeamento-coordenadas.gif" alt="Mapeamento de coordenadas com PyAutoGUI" width="100%"></td>
    <td width="50%"><img src="gifs/rpa-fluxo-completo-portal.gif" alt="Fluxo completo de automação do portal" width="100%"></td>
  </tr>
  <tr>
    <td width="50%" align="center"><sub>Pausa no código, mouse sobre o elemento e leitura da coordenada no terminal.</sub></td>
    <td width="50%" align="center"><sub>Login, navegação pelas séries e download dos CSVs.</sub></td>
  </tr>
</table>

### Como executar

```bash
python src/automacao_portal.py
```

Requisitos: Chrome instalado no caminho padrão e o mesmo ambiente de tela descrito acima.

## Como construir o projeto

O desenvolvimento é organizado em desafios descritos em **[detalhamento.md](detalhamento.md)**.

Cada desafio define contexto, requisitos, entradas, saídas e critérios de aceite — sem prescrever a implementação. A ideia é ir resolvendo aos poucos, pesquisando e praticando cada etapa.

## Estrutura do repositório

```text
automacao-dashboard-boletim-escolar/
├── dados/
│   ├── simulados/
│   ├── provas/
│   └── projetos/
├── docs/
│   └── progresso-etapas.svg
├── gifs/
│   ├── rpa-mapeamento-coordenadas.gif
│   └── rpa-fluxo-completo-portal.gif
├── portal_simulado/
├── src/
│   └── automacao_portal.py
├── saidas/
│   ├── boletins/
│   └── prints/
├── detalhamento.md
├── requirements.txt
└── README.md
```

## Fontes de dados (simuladas)

| Fonte | Formato | Origem fictícia |
|-------|---------|-----------------|
| Simulado | CSV | Portal HTML local |
| Provas | Excel | Professores |
| Projeto pedagógico | PDF | Coordenação |

## Tecnologias

| Uso | Ferramenta |
|-----|------------|
| Automação de interface (RPA) | PyAutoGUI |
| Leitura e consolidação de dados | Pandas, OpenPyXL, PDFPlumber |
| Dashboard | Streamlit, Plotly |
| Linguagem | Python |

Dependências listadas em `requirements.txt`.

## Portal simulado (login fictício)

Abra `portal_simulado/login.html` no navegador.

- **Email:** `coordenacao@colegiocaminhosfuturo.local`
- **Senha:** `Demo@2026`

## Transparência

O portal escolar deste projeto é uma **simulação local**. Não representa nenhuma instituição real e não utiliza dados pessoais de alunos.

Parte do material inicial (como o portal HTML) foi estruturada com apoio de ferramentas de IA, sempre dentro de um cenário fictício e educacional.
