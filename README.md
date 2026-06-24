# 🎓 Sistema de Automação de Diplomas — PROPEPG

Este repositório contém uma solução completa e integrada para a esteira de geração, auditoria e processamento de diplomas de pós-graduação. O sistema transforma um processo manual propício a erros humanos em um fluxo de **um único clique**, garantindo consistência através de validação cruzada assistida por IA e processamento automatizado.

---

## 🏗️ Arquitetura e Fluxo do Projeto

O ecossistema é orquestrado de forma modular e escalável, dividido em três microsserviços/etapas que se comunicam através de arquivos de dados controlados:

    [ Documentos Originais ] 
             │
             ▼
     1. Criar_banco_de_dados  ──► Gera o 'database.csv' cru via IA
             │
             ▼
     2. Verificador           ──► Valida contra o livro de registros oficial e gera o 'database.csv' corrigido
             │
             ▼
     3. Criar_diplomas        ──► Injeta os dados no template .ODT, gera os PDFs finais e abre no navegador

### 📁 Estrutura de Pastas e Componentes

* **`Criar_banco_de_dados/`**: Módulo responsável pela extração inteligente de dados brutos a partir de fontes e documentos originais utilizando LLMs (Gemini e Groq).
* **`Verificador/`**: O "filtro de segurança" do sistema. Executa rotinas avançadas de Expressões Regulares (Regex) com tolerância a falhas de leitura de OCR para auditar a integridade dos dados gerados, prevenindo duplicações e alucinações.
* **`Criar_diplomas/`**: Sistema de renderização e compilação de documentos que injeta os metadados corrigidos em um arquivo estruturado LibreOffice (`.odt`), convertendo-os em lote para arquivos `.pdf` e gerenciando a limpeza dos temporários.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.x**: Linguagem base para os scripts de processamento de dados e IA.
* **Pandas**: Manipulação estruturada de dataframes para tratamento dos dados acadêmicos.
* **LibreOffice (Headless CLI)**: Engine de segundo plano utilizado para conversão em lote de documentos sem necessidade de interface gráfica.
* **Windows Batch (Scripts `.bat`)**: Orquestração e automação da esteira de execução local.

---

## 🚀 Como Executar

### Pré-requisitos

1.  **LibreOffice** instalado no caminho padrão do Windows (`C:\Program Files\LibreOffice`).
2.  **Python** instalado no sistema e adicionado às variáveis de ambiente (`PATH`).
3.  Instalação das dependências necessárias através do terminal:
    ```bash
    pip install pandas python-dotenv
    ```

### Configuração das Chaves de API

Para proteger as credenciais utilizadas pelos serviços de inteligência artificial, o sistema utiliza variáveis de ambiente. 

1. Acesse a pasta `Criar_banco_de_dados/Codigo/`.
2. Crie um arquivo chamado `.env`.
3. Adicione suas chaves no seguinte formato:
    ```env
    API_KEY=Sua_Chave_Gemini_Aqui
    GROQ_API_KEY=Sua_Chave_Groq_Aqui
    ```
*Nota: O arquivo `.env` está devidamente configurado no `.gitignore` para garantir que credenciais locais nunca sejam publicadas no histórico do repositório.*

### Executando a Esteira Completa

Para rodar todo o ecossistema (Extração ──► Auditoria ──► Geração ──► Visualização), basta ir na raiz do projeto e dar um duplo clique em:

👉 **`gerar_tudo.bat`**

O terminal guiará o processo passo a passo e, ao final, perguntará se você deseja abrir os PDFs gerados automaticamente no Google Chrome para conferência visual.

---

## 🛡️ Camadas de Segurança Implementadas

1.  **Princípio Fail-Fast (Anti-Alucinação)**: O validador inspeciona a integridade das colunas e intercepta chaves primárias duplicadas (como reuso de número de processo SEI) antes de processar os arquivos, abortando execuções corrompidas.
2.  **Regex Elástica para OCR**: Filtros capazes de identificar dados sensíveis (Nomes, RGs, Páginas) mesmo quando o motor de OCR injeta espaços fantasmas ou falhas de caracteres nos textos do livro de registro.
3.  **Ambiente Isolado**: Cada script trabalha dentro do seu próprio escopo e diretório relativo `%~dp0`, tornando a automação portátil para qualquer máquina Windows por meio de pendrives ou redes internas.