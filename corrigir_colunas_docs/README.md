# ⚙️ Verificador e Fixador de Tabelas - Google Docs

Este script foi desenvolvido para solucionar o problema de redimensionamento automático e acidental de colunas no Google Docs (No livro de registro de diplomas). Ele varre o documento, identifica tabelas com uma estrutura específica e força o retorno das colunas para as posições originais.

## 🚀 Como Funciona
* **Filtro Inteligente (Opção 1):** O script analisa apenas tabelas que possuem **exatamente 17 colunas** (o padrão do livro de registros). Qualquer outra tabela com número diferente de colunas (como cabeçalhos ou notas) é completamente ignorada e preservada.
* **Correção em Tempo Real:** Ao rodar o script, ele mede cada coluna e, se houver qualquer divergência maior que 1 ponto (decorrente de arrastar o mouse sem querer ou quebra de texto), ele restaura os centímetros exatos e exibe um alerta visual na tela.

## 📋 Medidas Travadas (17 Colunas)
As larguras ideais configuradas (da 1ª à 17ª coluna em centímetros) são:
`1.208`, `1.834`, `1.27`, `2.222`, `1.429`, `2.011`, `1.323`, `2.011`, `1.773`, `1.64`, `2.434`, `2.09`, `1.244`, `1.508`, `1.587`, `1.984`, `1.27`.

## 🔧 Como Instalar no Google Docs
1. No seu documento do Google Docs, vá ao menu superior e clique em **Extensões** > **Apps Script**.
2. Cole o código do arquivo `.gs` no editor de texto.
3. Clique no ícone de **Salvar** (o disquete) e feche a aba do Apps Script.
4. Volte ao documento e **atualize a página (F5)**.

## 🛠️ Como Usar no Dia a Dia
1. Após atualizar a página, um novo menu chamado **`⚙️ Minhas Tabelas`** aparecerá no topo do Google Docs.
2. Sempre que desconfiar que alguma coluna saiu do lugar, clique em:
   **`⚙️ Minhas Tabelas`** > **`Verificar e Fixar Colunas`**.
3. Se algo tiver mudado, o script corrige na hora e exibe o alerta:
   * ⚠️ *ALERTA: Uma ou mais colunas foram movidas sem querer! O layout original foi restaurado com sucesso.*
4. Se o layout já estiver correto, ele apenas confirma:
   * ✅ *Tudo sob controle! As colunas continuam exatamente com os tamanhos travados :)*