import pandas as pd
import json
import os
from datetime import datetime
from google.genai.errors import ServerError, APIError
import config
import extrator

def obter_data_emissao():
    while True:
        entrada = input("Digite a data de emissão para os diplomas deste lote (DD/MM/AAAA): ").strip()
        try:
            data_objeto = datetime.strptime(entrada, "%d/%m/%Y")
        except ValueError:
            print("    [ERRO] Formato inválido! Digite como DD/MM/AAAA (Ex: 02/06/2026).\n")
            continue
        
        meses_extenso = {
            1: "janeiro", 2: "fevereiro", 3: "março", 4: "abril",
            5: "maio", 6: "junho", 7: "julho", 8: "agosto",
            9: "setembro", 10: "outubro", 11: "novembro", 12: "dezembro"
        }
        
        dia = f"{data_objeto.day:02d}"
        mes = meses_extenso[data_objeto.month]
        ano = str(data_objeto.year)
        
        return dia, mes, ano

def escolher_ia():
    print("\n--- SELEÇÃO DE INTELIGÊNCIA ARTIFICIAL ---")
    print("[ 1 ] Google Gemini (Padrão)")
    print("[ 2 ] Groq (Caso o Gemini esteja instável.)")
    
    while True:
        opcao = input("Escolha a opção desejada (1 ou 2): ").strip()
        if opcao == "1":
            return "gemini"
        elif opcao == "2":
            return "groq"
        else:
            print("    [ERRO] Opção inválida. Digite apenas 1 ou 2.\n")

def rodar_fluxo_automacao(caminho_livro, arquivo_saida):
    if not os.path.exists(caminho_livro):
        print(f"Erro: O arquivo '{caminho_livro}' não foi encontrado.")
        return

    dia_e, mes_e, ano_e = obter_data_emissao()
    ia_escolhida = escolher_ia()

    print("\nSolicitando extração...")
    
    try:
        if ia_escolhida == "gemini":
            print("   -> Utilizando Gemini...")
            resultado_texto = extrator.extrair_dados_livro(caminho_livro).strip()
        else:
            print("   -> Utilizando Groq...")
            import extrator_groq
            resultado_texto = extrator_groq.extrair_dados_livro(caminho_livro).strip()

    except (ServerError, APIError):
        print("\n[AVISO] Os servidores do Gemini estão temporariamente sobrecarregados (Erro 503).")
        print("Aguarde alguns segundos ou execute o script novamente escolhendo a Groq (Opção 2).")
        return
    except Exception as erro_inesperado:
        print(f"\n[ERRO] Falha na comunicação com a IA selecionada: {erro_inesperado}")
        return
    
    try:
        # Tratamento de segurança
        if resultado_texto.startswith("```"):
            resultado_texto = resultado_texto.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if resultado_texto.startswith("json"):
                resultado_texto = resultado_texto.split("\n", 1)[1].strip()

        # Converte a resposta em dados manipuláveis
        lista_alunos = json.loads(resultado_texto)
        print(f"   [OK] Foram processados dados de {len(lista_alunos)} alunos com sucesso.")
        
        # Estrutura inicial com os dados coletados do livro
        df_final = pd.DataFrame(lista_alunos, columns=config.COLUNAS_DATABASE)
        
        # PROCV Automatizado: Preenche sigla, área e portaria olhando para o dicionário do config
        df_final['sigla_curso'] = df_final['curso_conclusao'].apply(lambda x: config.MAPEAMENTO_CURSOS.get(x, {}).get('sigla', ''))
        df_final['area']        = df_final['curso_conclusao'].apply(lambda x: config.MAPEAMENTO_CURSOS.get(x, {}).get('area', ''))
        df_final['portaria']    = df_final['curso_conclusao'].apply(lambda x: config.MAPEAMENTO_CURSOS.get(x, {}).get('portaria', ''))
        
        # Aloca os dados de data de emissão decididos por você para todas as linhas
        df_final['dia_emissao'] = dia_e
        df_final['mes_emissao'] = mes_e
        df_final['ano_emissao'] = ano_e
        
        # Salva o arquivo final estruturado
        df_final.to_csv(arquivo_saida, index=False, encoding='utf-8-sig')
        print(f"\n[SUCESSO] Planilha '{arquivo_saida}' gerada!\n")
        
    except Exception as e:
        print(f"\n[ERRO] Falha crítica no processamento da estrutura dos dados. Detalhes: {e}")

# Executa o programa
if __name__ == "__main__":
    LIVRO_ALUNOS = "./livro_registro.pdf"
    # LIVRO_ALUNOS = "./livro.pdf"
    #LIVRO_ALUNOS = "./livro_teste.pdf"
    #LIVRO_ALUNOS = "./um.pdf"
    BANCO_DESTINO = "./database.csv"
    
    rodar_fluxo_automacao(LIVRO_ALUNOS, BANCO_DESTINO)
