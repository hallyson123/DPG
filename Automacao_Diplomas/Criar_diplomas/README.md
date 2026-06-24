# Sistema de Geração Automática de Diplomas (Word para PDF)

Este sistema automatiza a criação de diplomas, lendo os dados de uma planilha (`database.csv`), preenchendo o modelo oficial (`template.docx`) e convertendo os documentos finais para PDF usando o LibreOffice.

## 1. Pré-requisitos da Máquina
Para que o sistema funcione corretamente, o computador precisa ter:

* **Python 3.12** (ou superior) instalado.
* **LibreOffice** instalado no disco local padrão (`C:\Program Files\LibreOffice\program\soffice.exe`).
* **Bibliotecas Python:** Instale abrindo o terminal e executando o seguinte comando:
  `pip install pandas docxtpl`

## 2. Estrutura de Pastas Exigida
Antes de rodar, certifique-se de que os arquivos estão organizados exatamente desta forma na mesma pasta:

[Pasta Principal]
 ├── lote_diplomas_definitivo.py  (Script principal)
 ├── database.csv                 (Planilha com os dados extraídos)
 └── template.docx                (Modelo do diploma em Word)

*Nota: As pastas "docs" e "pdfs" serão criadas automaticamente pelo sistema.*

## 3. Passo a Passo para Execução

### Passo 1: Gerar os Diplomas em Word
1. Abra o terminal dentro da pasta onde estão os arquivos acima.
2. Digite o comando abaixo e pressione Enter:
   `python lote_diplomas_definitivo.py`
3. Aguarde a mensagem "Done! - now Check your files". Todos os arquivos `.docx` gerados estarão dentro da nova pasta `docs`.

### Passo 2: Converter para PDF em Lote
1. No mesmo terminal, copie o comando abaixo, cole e pressione Enter:
   `& "C:\Program Files\LibreOffice\program\soffice.exe" --headless --convert-to pdf --outdir pdfs docs/*.docx`
2. Aguarde alguns segundos. O LibreOffice irá processar os arquivos silenciosamente.
3. Pronto! Abra a nova pasta `pdfs` para acessar todos os diplomas finalizados.