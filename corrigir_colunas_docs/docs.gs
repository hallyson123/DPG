function onOpen() {
  var ui = DocumentApp.getUi();
  ui.createMenu('⚙️ Minhas Tabelas')
      .addItem('Verificar e Fixar Colunas', 'verificarColunasLivro')
      .addToUi();
}

function verificarColunasLivro() {
  var doc = DocumentApp.getActiveDocument();
  var body = doc.getBody();
  var tables = body.getTables();
  
  if (tables.length === 0) {
    DocumentApp.getUi().alert('Nenhuma tabela encontrada no documento.');
    return;
  }

  // Seus tamanhos exatos em centímetros (na ordem da 1ª à 17ª coluna)
  var tamanhosDesejadosCm = [1.208, 1.834, 1.27, 2.222, 1.429, 2.011, 1.323, 2.011, 1.773, 1.64, 2.434, 2.09, 1.244, 1.508, 1.587, 1.984, 1.27]; 

  var largurasIdeais = tamanhosDesejadosCm.map(function(cm) {
    return cm * 28.3465; 
  });

  var modificou = false;

  // Percorre todas as tabelas encontradas no documento
  for (var i = 0; i < tables.length; i++) {
    var table = tables[i];
    var numColumns = table.getRow(0).getNumCells();
    
    // FILTRO: Se a tabela NÃO tiver exatamente 17 colunas, o script ignora ela
    if (numColumns !== 17) {
      continue; 
    }
    
    // Se a tabela tiver 17 colunas, o programa faz checagem abaixo (isso foi feito pra ignorar a ultima tabela "Formulários invalidados"):
    for (var j = 0; j < numColumns; j++) {
      if (j >= largurasIdeais.length) break; 
      
      var larguraAtual = table.getColumnWidth(j);
      var larguraEsperada = largurasIdeais[j];

      // Verifica se o tamanho atual foi alterado (com margem de tolerância de 1 ponto)
      if (Math.abs(larguraAtual - larguraEsperada) > 1) {
        table.setColumnWidth(j, larguraEsperada);
        modificou = true;
      }
    }
  }

  // Alerta visual de destaque caso alguma tabela de 17 colunas tenha sido corrigida
  if (modificou) {
    DocumentApp.getUi().alert('⚠️ ALERTA: Uma ou mais colunas foram movidas sem querer! O layout original de 17 colunas foi restaurado com sucesso.');
  } else {
    DocumentApp.getUi().alert('✅ Tudo sob controle! Suas tabelas de 17 colunas continuam com os tamanhos travados.');
  }
}
