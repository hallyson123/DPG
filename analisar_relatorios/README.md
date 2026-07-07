# Analisador de Relatórios Institucionais (PROPEPG)

Este projeto contém um script em Python para automatizar a extração e contagem de dados de alunos a partir de planilhas de relatórios. O objetivo principal é agrupar e contabilizar o total de alunos matriculados por **Curso** e por **Campus**.

## ⚙️ Pré-requisitos

Para rodar este projeto, você precisará do Python instalado e de duas bibliotecas específicas. 

No terminal, instale as dependências executando:

```bash
pip install pandas xlrd
```

* **pandas:** Utilizado para a manipulação, limpeza e agrupamento massivo dos dados.
* **xlrd:** Motor necessário para que o pandas consiga ler arquivos legados `.xls` (mesmo que estejam mascarados como `.ods`).

## 🚀 Como Executar

1. Coloque o arquivo de relatório na mesma pasta do script `main.py`.
2. Abra o terminal na pasta do projeto (`...\analisar_relatorios`).
3. Execute o script:

```bash
python main.py
```

## 📊 Estrutura Esperada dos Dados

Para que o script funcione corretamente, a planilha de entrada deve conter as seguintes colunas em sua linha de cabeçalho:

* `CPF`
* `NOME`
* `MATRÍCULA`
* `CURSO`
* `CAMPUS`

> **Nota:** O script padroniza automaticamente os nomes das colunas para letras maiúsculas e remove espaços em branco extras para evitar erros de leitura.