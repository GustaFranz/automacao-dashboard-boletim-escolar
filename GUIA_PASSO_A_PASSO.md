# Guia passo a passo - automacao-dashboard-boletim-escolar

Este projeto simula uma rotina de coordenação escolar: receber notas de várias fontes, consolidar tudo em um único lugar, calcular médias ponderadas, gerar boletins e criar um dashboard.

## Contexto do projeto

Escola fictícia: Colégio Caminhos do Futuro

Turmas:

- 6º ano Matutino: 26 alunos
- 7º ano Matutino: 25 alunos
- 8º ano Matutino: 20 alunos

Fontes de notas:

- Simulado: portal HTML local, baixado em CSV com PyAutoGUI
- Provas: arquivos Excel, um por série, com um aluno por linha e as disciplinas em colunas
- Projeto pedagógico: arquivos PDF simples, um por série

Disciplinas:

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

## ETAPA 1 - Entender os dados de entrada

Objetivo:
Entender quais arquivos o sistema vai usar.

Explicação:
O projeto usa três tipos de arquivo para simular uma situação real de escola. O simulado vem de um portal, as provas vêm dos professores e o projeto vem da coordenação.

Código:
Nesta etapa, apenas abra as pastas:

```text
dados/simulados/
dados/provas/
dados/projetos/
portal_simulado/
```

O que testar:
Confira se existem arquivos para 6ano, 7ano e 8ano.

Erros comuns:
Confundir dados de entrada com saídas do sistema.

Como saber se deu certo:
Você consegue explicar de onde vem cada nota.

## ETAPA 2 - Testar o portal fictício

Objetivo:
Abrir o portal local e entender onde o PyAutoGUI será usado.

Explicação:
O portal é um site local fictício. Ele serve para simular um sistema escolar sem usar login real, dados reais ou internet.

Código:
Abra este arquivo no navegador:

```text
portal_simulado/login.html
```

Use:

```text
Email: coordenacao@colegiocaminhosfuturo.local
Senha: Demo@2026
```

O que testar:
Entre no painel e abra as páginas das três séries.

Erros comuns:
Digitar a senha diferente, esquecer letra maiúscula ou abrir o arquivo errado.

Como saber se deu certo:
Você acessa o painel e consegue baixar os CSVs de simulado.

## ETAPA 3 - Automatizar o download do simulado com PyAutoGUI

Objetivo:
Usar PyAutoGUI para abrir o portal, fazer login e baixar os CSVs.

Explicação:
Aqui o PyAutoGUI tem uma função realista: simular uma pessoa acessando um portal escolar e baixando relatórios.

Código:
Crie depois um arquivo:

```text
src/automacao_portal.py
```

Esse arquivo deverá:

- abrir o navegador;
- acessar `portal_simulado/login.html`;
- digitar email e senha;
- entrar no painel;
- abrir 6ano, 7ano e 8ano;
- clicar em Baixar CSV;
- salvar prints em `saidas/prints/`.

O que testar:
Execute a automação com o navegador aberto e em foco.

Erros comuns:
Tela em zoom diferente, navegador sem foco, download indo para a pasta Downloads do Windows.

Como saber se deu certo:
Os CSVs do simulado são baixados e há prints em `saidas/prints/`.

## ETAPA 4 - Ler os arquivos de notas

Objetivo:
Criar funções para ler CSV, Excel e PDF.

Explicação:
O Python deve transformar todos os arquivos em tabelas compatíveis.

Bibliotecas:

- `pandas` para CSV e tabelas
- `openpyxl` para Excel
- `pdfplumber` para PDF

Arquivos de entrada:

```text
dados/simulados/simulado_6ano.csv
dados/provas/provas_6ano.xlsx
dados/projetos/projeto_6ano.pdf
```

Formato do Excel de provas:

```text
turma | aluno | Língua Portuguesa | Matemática | Ciências | História | Geografia | Inglês | Educação Física | Artes | Ensino Religioso | Redação
```

Cada arquivo Excel também possui uma aba chamada `Professores`, com o professor responsável por cada disciplina.

O que testar:
Imprimir as primeiras linhas de cada arquivo.

Erros comuns:
PDF com tabela difícil de extrair, coluna escrita diferente, arquivo salvo em pasta errada.

Como saber se deu certo:
Você consegue carregar as notas em tabelas.

## ETAPA 5 - Consolidar as notas

Objetivo:
Juntar simulado, prova e projeto em uma única tabela.

Explicação:
O sistema deve combinar as notas por turma, aluno e disciplina.

Observação:
As provas chegam em formato largo, com uma disciplina por coluna. Para calcular o dashboard, uma boa estratégia é transformar essas colunas em linhas usando `pandas.melt`. Assim a tabela interna fica com as colunas:

```text
turma | aluno | disciplina | nota_prova
```

Cálculo:

```text
projeto_convertido = nota_projeto * 2
media = (simulado * 10 + prova * 10 + projeto_convertido * 5) / 25
```

Critério:

```text
media >= 6.0 -> aprovado
media < 6.0 -> recuperação
```

O que testar:
Verifique alguns alunos manualmente.

Erros comuns:
Nome do aluno diferente entre arquivos, nota do projeto esquecida na escala 0 a 5.

Como saber se deu certo:
Cada aluno tem média calculada nas 10 disciplinas.

## ETAPA 6 - Gerar boletins

Objetivo:
Criar boletins individuais por aluno.

Explicação:
Cada boletim pode ser HTML na primeira versão. HTML é mais fácil de gerar e abrir no navegador.

Saída esperada:

```text
saidas/boletins/
```

O que testar:
Abrir alguns boletins e verificar médias e situação.

Erros comuns:
Boletim sem todas as disciplinas, média arredondada errado.

Como saber se deu certo:
Cada aluno possui um boletim claro e legível.

## ETAPA 7 - Criar dashboard com Streamlit e Plotly

Objetivo:
Criar um painel visual interativo.

Explicação:
Streamlit e Plotly permitem criar um dashboard bonito rapidamente. Isso é uma boa escolha para a primeira versão do portfólio, porque economiza tempo sem esconder a lógica principal do projeto.

Indicadores:

- média da turma por disciplina;
- percentual de alunos acima e abaixo da média;
- disciplinas com melhor e pior desempenho;
- alunos em recuperação.

O que testar:
Rodar:

```bash
streamlit run dashboard.py
```

Erros comuns:
Não instalar dependências, rodar o comando fora da pasta do projeto.

Como saber se deu certo:
O navegador abre um dashboard interativo.

## ETAPA 8 - Melhorias para versão 2

Ideias:

- trocar 3 Excels por 30 planilhas, uma por professor e por turma;
- gerar boletins em PDF;
- criar filtros avançados no dashboard;
- personalizar visual do Streamlit;
- adicionar testes automatizados;
- criar logs de execução.

