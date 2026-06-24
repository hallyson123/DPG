# Extração Automática de Dados de Diplomas (Livro de registro para CSV)

Este sistema utiliza Inteligência Artificial (Google Gemini Pro ou Meta Llama 3.3 via Groq) para ler livros de registro de diplomas em formato PDF. O script extrai as informações textuais dos alunos, aplica regras estritas de negócio (como padronização de portarias, siglas de cursos e concordância de gênero) e consolida tudo estruturado num arquivo de banco de dados (`database.csv`).

## 1. Pré-requisitos da Máquina
Para rodar este script, o computador precisa ter instalado:

* **Python 3.12** (ou superior). Ao instalar no Windows, marque a opção obrigatória "Add Python to PATH".
* **Bibliotecas Python:** Instale abrindo o terminal e executando o seguinte comando:
  `pip install google-genai groq pypdf pandas`
* **pip install python-dotenv**

## 2. Configuração das Chaves de API
Antes de rodar o sistema pela primeira vez, as chaves de acesso devem ser configuradas de forma segura dentro do arquivo de configurações:

1. Abra o arquivo `codigo/config.py` com o Bloco de Notas.
2. Cole as suas credenciais institucionais entre as aspas, como no exemplo abaixo:
   `GEMINI_API_KEY = "sua_chave_gemini_aqui"`
   `GROQ_API_KEY = "sua_chave_groq_aqui"`

## 3. Estrutura de Pastas Exigida
Mantenha os arquivos organizados exatamente desta forma na pasta do estágio para evitar erros de caminhos:

```text
📁 Sua Pasta Principal/
 ├── ⚙️ executar.bat           # Arquivo para execução rápida
 ├── 📄 livro_registro.pdf     # O PDF do livro que será lido pela IA
 └── 📁 codigo/                # Pasta interna com os scripts do sistema
      ├── 🐍 main.py
      ├── ⚙️ config.py
      ├── 🐍 extractor.py      # Módulo de extração usando Gemini
      └── 🐍 extractor_groq.py # Módulo de extração usando Groq
```

*Nota: O arquivo "database.csv" será gerado automaticamente na raiz da Pasta Principal após o término do processamento.*

## 4. Passo a Passo para Execução

1. Certifique-se de que o arquivo do livro em PDF está na pasta principal com o nome correto: `livro_registro.pdf`.
2. Vá na pasta principal e dê **dois cliques** no arquivo **`executar.bat`**.
3. O terminal abrirá sozinho e solicitará as entradas:
   * **Data de Emissão:** Digite a data de expedição que constará nos diplomas).
   * **Escolha da IA:** Digite `1` para o **Gemini** (Plano Principal) ou `2` para **Groq** (Caso o Gemini esteja instável).
4. Aguarde o processamento das páginas e a estruturação dos dados pelo Pandas.
5. Quando a mensagem de sucesso aparecer, pressione qualquer tecla para fechar. O arquivo **`database.csv`** estará pronto na raiz do projeto.