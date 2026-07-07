# Detalhamento do projeto

Documento de referência dos módulos desta automação. Cada seção descreve um desafio a ser implementado: requisitos, entradas, saídas e critérios de aceite — sem prescrever a solução em código.

**Escola fictícia:** Colégio Caminhos do Futuro  
**Status geral:** em construção

## Contexto geral

Este projeto simula a rotina de uma coordenação escolar fictícia. Os dados são inventados e não representam alunos ou instituições reais.

**Turmas:**

- 6º ano Matutino — 26 alunos
- 7º ano Matutino — 25 alunos
- 8º ano Matutino — 20 alunos

**Disciplinas:**

1. Língua Portuguesa
2. Matemática
3. Ciências
4. História
5. Geografia
6. Inglês
7. Educação Física
8. Artes
9. Ensino Religioso
10. Redação

**Fontes de notas:**

| Fonte | Formato | Origem fictícia |
|-------|---------|-----------------|
| Simulado | CSV | Portal HTML local |
| Provas | Excel | Professores |
| Projeto pedagógico | PDF | Coordenação |

## Visão da automação

Este projeto combina três camadas de automação:

| Camada | Descrição |
|--------|-----------|
| **Interface (RPA)** | PyAutoGUI simula a interação humana no portal local — login, navegação e download dos CSVs de simulado. |
| **Dados** | Leitura e consolidação de CSV, Excel e PDF em uma base única, com cálculo de médias e regras pedagógicas. |
| **Saída** | Geração automática de boletins individuais e dashboard interativo com indicadores das turmas. |

Cenário inspirado na rotina escolar: várias fontes de nota, portal sem API e tarefas repetitivas que podem ser automatizadas.

---

## Desafio 1 — Mapeamento dos dados de entrada

### Contexto

Antes de automatizar qualquer rotina, é preciso entender de onde vêm as notas e como estão organizadas.

### O que o sistema deve fazer

- Identificar as três fontes de dados: simulado, provas e projeto pedagógico.
- Confirmar que existem arquivos para as séries do 6º, 7º e 8º ano.
- Diferenciar claramente dados de entrada dos arquivos que o sistema irá gerar.

### Entradas

- `dados/simulados/`
- `dados/provas/`
- `dados/projetos/`
- `portal_simulado/`

### Saídas esperadas

Nenhum arquivo gerado nesta etapa. O resultado é a compreensão do cenário e dos formatos envolvidos.

### Critérios de aceite

- [ ] Consigo explicar a origem e o formato de cada tipo de nota.
- [ ] Existem arquivos de entrada para as três séries.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 2 — Validação do portal fictício

### Contexto

O simulado escolar fica em um portal local. Antes de automatizar, o fluxo manual precisa funcionar.

### O que o sistema deve fazer

- Abrir o portal local a partir dos arquivos do projeto.
- Realizar login com as credenciais de demonstração.
- Acessar o painel e as páginas das três séries.
- Baixar manualmente os CSVs de simulado para validar o fluxo.

### Entradas

- `portal_simulado/login.html`
- Credenciais fictícias descritas no README

### Saídas esperadas

Confirmação de que o portal funciona e CSVs de teste disponíveis.

### Critérios de aceite

- [ ] O login funciona com as credenciais de demonstração.
- [ ] Consigo acessar o painel e as páginas das três séries.
- [ ] Consigo baixar o CSV de simulado de cada série.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 3 — Automação do download do simulado

### Contexto

Baixar os relatórios de simulado manualmente, série por série, não escala. Esta etapa introduz automação de interface (RPA) com PyAutoGUI em um cenário próximo da rotina escolar — simular cliques e digitação no navegador quando o portal não oferece API.

### O que o sistema deve fazer

- Acessar o portal local de forma automatizada com PyAutoGUI.
- Autenticar com as credenciais de demonstração.
- Navegar pelas páginas das três séries e acionar o download dos CSVs.
- Registrar evidência da execução (capturas de tela, log ou equivalente).

### Entradas

- Portal em `portal_simulado/`
- Credenciais fictícias descritas no README

### Saídas esperadas

- CSVs do simulado prontos para uso nas etapas seguintes
- Evidência da execução em pasta de saída (ex.: `saidas/prints/`)

### Critérios de aceite

- [ ] Os CSVs das três séries são obtidos sem intervenção manual repetida.
- [ ] A automação com PyAutoGUI funciona de forma reproduzível na máquina local.
- [ ] Há registro visual ou log da execução.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 4 — Leitura dos arquivos de notas

### Contexto

As notas chegam em formatos diferentes. O sistema precisa transformá-las em uma estrutura única e utilizável.

### O que o sistema deve fazer

- Ler arquivos CSV de simulado.
- Ler planilhas Excel de provas, com um aluno por linha e as disciplinas organizadas em colunas.
- Reconhecer a aba adicional de professores presente nas planilhas de prova.
- Ler PDFs simples de projeto pedagógico.
- Produzir dados estruturados e consultáveis (turma, aluno, disciplina, nota).

### Entradas

- `dados/simulados/`
- `dados/provas/`
- `dados/projetos/`

### Saídas esperadas

Dados carregados e inspecionáveis, prontos para consolidação.

### Critérios de aceite

- [ ] CSV, Excel e PDF são lidos com sucesso.
- [ ] Consigo visualizar uma amostra dos dados carregados.
- [ ] O formato das provas (largo, com disciplinas em colunas) é reconhecido.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 5 — Consolidação e cálculo de médias

### Contexto

Com todas as notas lidas, o sistema deve reunir simulado, prova e projeto pedagógico e aplicar a regra pedagógica de aprovação.

### O que o sistema deve fazer

- Combinar as notas por turma, aluno e disciplina.
- Aplicar média ponderada considerando pesos distintos para simulado, prova e projeto pedagógico.
- Tratar a escala do projeto pedagógico de forma coerente com as demais avaliações.
- Classificar cada aluno como aprovado ou em recuperação, com base no critério mínimo de 6,0.

### Entradas

Dados estruturados produzidos na etapa anterior.

### Saídas esperadas

Base consolidada com média e situação por aluno e disciplina.

### Critérios de aceite

- [ ] Cada aluno possui média calculada nas 10 disciplinas.
- [ ] Uma amostra manual confere com o resultado esperado.
- [ ] A situação (aprovado ou recuperação) está definida para cada registro.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 6 — Geração de boletins

### Contexto

A coordenação precisa de um documento individual por aluno, claro o suficiente para conferência e comunicação.

### O que o sistema deve fazer

- Gerar um boletim por aluno com notas, médias e situação final.
- Produzir arquivos em formato simples e legível, abrível no navegador na primeira versão.
- Organizar a saída em pasta dedicada.

### Entradas

Base consolidada com médias e situação.

### Saídas esperadas

Boletins individuais em pasta de saída (ex.: `saidas/boletins/`).

### Critérios de aceite

- [ ] Existe um arquivo por aluno.
- [ ] Todas as disciplinas aparecem no boletim.
- [ ] Médias e situação conferem em uma amostra verificada manualmente.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 7 — Dashboard escolar

### Contexto

Além dos boletins individuais, a coordenação precisa enxergar o desempenho das turmas de forma agregada.

### O que o sistema deve fazer

- Criar um painel interativo executável localmente.
- Exibir indicadores como:
  - média da turma por disciplina;
  - percentual de alunos acima e abaixo da média;
  - disciplinas com melhor e pior desempenho;
  - alunos em recuperação.

### Entradas

Base consolidada com médias e situação.

### Saídas esperadas

Dashboard interativo aberto no navegador.

### Critérios de aceite

- [ ] O painel abre localmente sem erro.
- [ ] Os indicadores refletem os dados consolidados.
- [ ] É possível explorar a visão geral ou filtrar por turma.

### Status

- [ ] Pendente

### Aprendizados

_(preencher após implementação)_

---

## Desafio 8 — Evoluções (versão 2)

### Contexto

Lista de melhorias futuras. Nenhuma delas é obrigatória para concluir a primeira versão do projeto.

### Ideias

- Substituir poucas planilhas centrais por mais arquivos, aproximando o fluxo real (ex.: uma planilha por professor e turma).
- Exportar boletins em PDF.
- Adicionar filtros avançados no dashboard.
- Personalizar o visual do painel.
- Incluir testes automatizados.
- Registrar logs de execução da automação.

### Status

- [ ] Backlog

### Aprendizados

_(preencher conforme evoluir o projeto)_