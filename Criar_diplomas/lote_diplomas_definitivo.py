import time
import pandas as pd
import os
import zipfile # Biblioteca nativa que substitui o docxtpl

def formatar_nome_proprio(texto):
    if not isinstance(texto, str):
        return texto
    # conectivos que devem permanecer em minúsculo
    conectivos = ['de', 'da', 'do', 'dos', 'das', 'e', 'em']
    palavras = texto.strip().lower().split()
    palavras_formatadas = [
        palavra if palavra in conectivos else palavra.capitalize() 
        for palavra in palavras
    ]
    # Garante que a primeira palavra do nome sempre comece maiúscula
    if palavras_formatadas:
        palavras_formatadas[0] = palavras_formatadas[0].capitalize()
    return ' '.join(palavras_formatadas)

def formatar_curso(texto):
    if not isinstance(texto, str):
        return texto
    
    texto_limpo = texto.upper().replace("MESTRADO EM ", "").replace("DOUTORADO EM ", "")
    return formatar_nome_proprio(texto_limpo)

# LÊ O ARQUIVO UMA ÚNICA VEZ PARA DEIXAR O SCRIPT MAIS RÁPIDO
df = pd.read_csv('database.csv', dtype='str')

# Trata os nomes do aluno e curso
df['nome_aluno'] = df['nome_aluno'].apply(formatar_nome_proprio)
if 'curso_conclusao' in df.columns:
    df['curso_conclusao'] = df['curso_conclusao'].apply(formatar_curso)

# Converte o dataframe para uma lista de dicionários
lista_alunos = df.to_dict(orient='records')
df2 = len(lista_alunos)

if not os.path.exists('docs'):
    os.makedirs('docs')

def mkw(aluno):
    # Puxa os dados para montar o nome do arquivo
    n_registro = str(aluno.get('n_registro', ''))
    sigla_curso = str(aluno.get('sigla_curso', ''))
    nome_aluno = str(aluno.get('nome_aluno', ''))

    # MUDA A EXTENSÃO DO ARQUIVO FINAL PARA .odt
    filename = f"{n_registro}-{sigla_curso}-{nome_aluno} - DIPLOMA.odt"
    caminho_final = os.path.join('docs', filename)

    # NOVA LÓGICA DE SUBSTITUIÇÃO: Abre o template.odt e injeta os dados
    with zipfile.ZipFile('template.odt', 'r') as zin:
        with zipfile.ZipFile(caminho_final, 'w') as zout:
            for item in zin.infolist():
                conteudo = zin.read(item.filename)
                
                # 'content.xml' é onde o LibreOffice guarda o texto do documento
                if item.filename == 'content.xml':
                    texto_xml = conteudo.decode('utf-8')
                    
                    # Procura pelas tags (ex: {{nome_aluno}}) e substitui pelo valor real
                    for tag, valor in aluno.items():
                        # O replace no XML puro requer conversão de string
                        texto_xml = texto_xml.replace(f"{{{{{tag}}}}}", str(valor))
                        
                    conteudo = texto_xml.encode('utf-8')
                    
                zout.writestr(item, conteudo)


print('There will be', df2, 'files')

# Passa o dicionário com os dados do aluno direto para a função
for i, aluno_atual in enumerate(lista_alunos):
    print("Gerando arquivo:", f"{i}" ,"...")
    mkw(aluno_atual)
