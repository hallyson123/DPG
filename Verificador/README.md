# Auditor e Validador de Registros (PDF vs CSV)

Uma ferramenta autônoma de engenharia de dados projetada para auditar, validar e corrigir bancos de dados (CSV) extraídos por Inteligência Artificial, confrontando-os com o texto bruto de livros de registro em PDF.

---

## 🎯 O Que o Projeto Faz

O script atua como um "validador de duas vias". Ele cruza os dados pré-preenchidos no seu arquivo `database.csv` com as páginas do arquivo `livro.pdf`. 

* **Preservação da Beleza:** Se o CSV estiver gramaticalmente correto (com acentos e formatação) e corresponder à leitura do PDF, o script aprova o dado sem remover a acentuação.
* **Correção Estrutural:** Se o dado no CSV estiver vazio, corrompido ou apontando para o aluno errado, o script usa expressões regulares e fatiamento posicional para extrair a informação real do PDF e injetar no banco de dados.
* **Dicionário de Ouro:** Padroniza nomes de cursos usando um mapeamento interno oficial, ignorando falhas de leitura de OCR do PDF.

---

## 📂 Estrutura do Projeto

A arquitetura foi dividida em três arquivos para facilitar a manutenção e a Separação de Preocupações (Separation of Concerns):

* **`main.py`**: O maestro do projeto. Contém o laço principal de repetição, a lógica de ancoragem de blocos (recorte por aluno) e as regras de negócio de validação coluna a coluna.
* **`config.py`**: O arquivo de constantes. Guarda a lista de colunas auditadas, o conversor de meses e o *Dicionário de Ouro* com as nomenclaturas oficiais dos cursos da instituição.
* **`utils.py`**: A caixa de ferramentas. Contém as funções de leitura do PDF, algoritmos de similaridade (Fuzzy Matching) e o motor de normalização de texto (remoção de acentos para comparação invisível).

---

## ⚙️ Pré-requisitos e Instalação

O projeto foi construído em Python. Certifique-se de ter as seguintes bibliotecas instaladas no seu ambiente virtual:

```bash
pip install pandas pypdf
```

*Nota: As bibliotecas `re`, `os`, `difflib` e `unicodedata` são nativas do Python e não exigem instalação separada.*

---

## 🚀 Como Executar

1. Coloque o seu arquivo de banco de dados na mesma pasta com o nome **`database.csv`**.
2. Coloque o arquivo PDF contendo as folhas de registro na mesma pasta com o nome **`livro.pdf`**.
3. Execute o maestro no seu terminal:

```bash
python main.py
```

O script gerará um log em tempo real no terminal detalhando o veredito de cada coluna. Ao final da execução, um novo arquivo chamado **`database_corrigido.csv`** será gerado com todas as correções aplicadas.

---

## 📊 Legenda de Status de Auditoria

Durante a execução, o terminal exibirá os seguintes marcadores para cada campo validado:

| Marcador | Status | O que significa |
| :--- | :--- | :--- |
| ✅ | **OK** | O dado do CSV está perfeito e corresponde ao PDF. O script não alterou nada. |
| ✨ | **CORRIGIDO_N1** | Formatação simples (ex: remoção de espaços extras ou capitalização). |
| 🔧 | **CORRIGIDO_N2** | Recuperação por Semelhança (Fuzzy). Ocorreu um pequeno erro de digitação/OCR. |
| 🎯 | **CORRIGIDO_N3** | O dado estava ausente/errado. O script pescou a informação diretamente do PDF. |
| ❌ | **ERRO CRÍTICO** | Falha na extração. O padrão não foi encontrado e requer revisão humana. |

---

## 🛠️ Tecnologias Utilizadas

* **Pandas:** Manipulação do Dataframe em memória e exportação do CSV final.
* **PyPDF:** Extração do texto bruto das páginas do livro de registros.
* **Expressões Regulares (Regex):** Fatiamento de blocos em formato de "sanduíche" e ancoragem posicional de informações isoladas (como números de processo SEI, RG e Datas).