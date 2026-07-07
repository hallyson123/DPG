import pandas as pd

def contar_alunos_por_curso_campus(caminho_arquivo):
    try:
        # df = pd.read_excel(caminho_arquivo, engine='odf')
        df = pd.read_excel(caminho_arquivo, engine='xlrd')
        df.columns = df.columns.str.strip().str.upper()
        
        #nomes das colunas
        coluna_cpf = 'CPF'
        coluna_nome = 'NOME'
        coluna_aluno = 'MATRÍCULA'
        coluna_curso = 'CURSO'
        coluna_campus = 'CAMPUS'

        # contando
        contagem = df.groupby([coluna_campus, coluna_curso])[coluna_aluno].count().reset_index()
        contagem = contagem.rename(columns={coluna_aluno: 'TOTAL_ALUNOS'})
        
        return contagem

    except Exception as e:
        print(f"Erro ao processar a planilha: {e}")
        return None

if __name__ == "__main__":
    arquivo_ods = 'Relatorio.ods' 
    resultado = contar_alunos_por_curso_campus(arquivo_ods)
    
    if resultado is not None:
        print("=== Contagem de Alunos ===")
        print(resultado)
        
        resultado.to_csv('relatorio_contagem.csv', index=False)
