# main.py
import pandas as pd
import re
import os
from config import CURSOS_OFICIAIS, MAPA_MESES, COLUNAS_AUDITORIA
from utils import normalizar_texto, ler_texto_completo_pdf

def auditar_banco_de_dados():
    arquivo_csv = 'database.csv'
    arquivo_pdf = 'livro_registro.pdf' # Ajuste para o nome do seu PDF
    
    if not os.path.exists(arquivo_csv):
        print(f"❌ Erro: O arquivo '{arquivo_csv}' não foi encontrado.")
        return

    texto_bruto_livro = ler_texto_completo_pdf(arquivo_pdf)
    if not texto_bruto_livro:
        return
    
    # print(texto_bruto_livro)
        
    texto_livro_norm = normalizar_texto(texto_bruto_livro)

    print(texto_livro_norm)

    print("⏳ Carregando os dados extraídos (CSV)...")
    df = pd.read_csv(arquivo_csv, dtype='str')
    
    # ====================================================================
    # CHECAGEM DE INTEGRIDADE: BARRANDO ALUCINAÇÕES DA IA
    # ====================================================================
    # Conta quantas vezes cada Processo SEI aparece no CSV
    processos_contagem = df['n_processo'].value_counts()
    processos_duplicados = processos_contagem[processos_contagem > 1].index.tolist()
    
    # Remove strings vazias ou 'nan' caso a IA tenha deixado linhas em branco
    processos_duplicados = [p for p in processos_duplicados if str(p).strip() and str(p).lower() != 'nan']
    
    if processos_duplicados:
        print("\n" + "!"*80)
        print(" 🚨 ALERTA CRÍTICO: ALUCINAÇÃO DA IA DETECTADA NO CSV")
        print("!"*80)
        print("A IA preencheu o mesmo Processo SEI para mais de um aluno. O banco está corrompido.")
        
        for proc in processos_duplicados:
            alunos_afetados = df[df['n_processo'] == proc]['nome_aluno'].tolist()
            print(f"  ❌ Processo Duplicado: {proc}")
            print(f"     -> Preenchido nos alunos: {', '.join(alunos_afetados)}\n")
            
        print("Por segurança, o validador foi abortado. Corrija o 'database.csv' manualmente.")
        return # Interrompe o script Python imediatamente
    # ====================================================================
    
    total_alunos = len(df)
    alunos_com_erro = 0
    erros_totais = 0
    correcoes_totais = 0

    print("\n" + "="*80)
    print(" 🚀 INICIANDO AUDITORIA E AUTOCORREÇÃO")
    print("="*80)

    for index, linen in df.iterrows():
        nome_original = str(linen.get('nome_aluno', f'Aluno {index}')).strip()
        nome_norm = normalizar_texto(nome_original)
        
        print(f"\n🔎 Verificando: {nome_original.upper()}")
        
        # ====================================================================
        # FASE 1: SISTEMA DE ÂNCORAS
        # ====================================================================
        indice_aluno = -1
        ancora_usada = ""

        proc_csv = str(linen.get('n_processo', ''))
        proc_limpo = re.sub(r'[^0-9]', '', proc_csv)
        rg_csv = str(linen.get('n_rg', ''))
        rg_limpo = re.sub(r'[^0-9]', '', rg_csv)

        if proc_limpo and len(proc_limpo) == 17:
            padrao_proc = r'[^0-9]*'.join(list(proc_limpo))
            match_proc = re.search(padrao_proc, texto_livro_norm)
            if match_proc:
                indice_aluno = match_proc.start()
                ancora_usada = "Processo SEI"

        if indice_aluno == -1 and rg_limpo and len(rg_limpo) >= 6:
            padrao_rg = r'[^0-9]*'.join(list(rg_limpo))
            match_rg = re.search(padrao_rg, texto_livro_norm)
            if match_rg:
                indice_aluno = match_rg.start()
                ancora_usada = "Número do RG"

        if indice_aluno == -1 and nome_norm:
            ocorrencias = texto_livro_norm.count(nome_norm)
            if ocorrencias == 1:
                indice_aluno = texto_livro_norm.find(nome_norm)
                ancora_usada = "Nome Civil"
            elif ocorrencias > 1:
                print(f"  ❌ MÚLTIPLOS ALUNOS: O nome '{nome_original}' aparece {ocorrencias} vezes no PDF. Homônimo detectado! Abortando.")
                alunos_com_erro += 1
                erros_totais += 1
                continue

        if indice_aluno == -1:
            print(f"  ❌ ALUNO NÃO ENCONTRADO (Nem por Processo, RG ou Nome)!")
            alunos_com_erro += 1
            erros_totais += 1
            continue
            
        print(f"  📍 Bloco localizado via: {ancora_usada}")

        # ====================================================================
        # RECORTE DO BLOCO DEFINITIVO
        # ====================================================================
        janela_tras = texto_livro_norm[max(0, indice_aluno - 400) : indice_aluno]
        matches_braida_ant = list(re.finditer(r'joao alfredo braida', janela_tras))
        
        if matches_braida_ant:
            ultimo_braida_ant = matches_braida_ant[-1]
            inicio_bloco = max(0, indice_aluno - 400) + ultimo_braida_ant.end()
        else:
            padrao_sei = r'\d{5}[\.\s]*\d{6}[/\s]*\d{4}[-\s]*\d{2}'
            matches_sei = list(re.finditer(padrao_sei, janela_tras))
            if matches_sei:
                inicio_bloco = max(0, (max(0, indice_aluno - 400) + matches_sei[-1].start()) - 15)
            else:
                inicio_bloco = max(0, indice_aluno - 120)

        janela_frente = texto_livro_norm[indice_aluno : min(len(texto_livro_norm), indice_aluno + 600)]
        match_diretor = re.search(r'joao alfredo braida', janela_frente)
        
        if match_diretor:
            fim_bloco = indice_aluno + match_diretor.end()
        else:
            fim_bloco = min(len(texto_livro_norm), indice_aluno + 300) 

        bloco_do_aluno = texto_livro_norm[inicio_bloco:fim_bloco]
        erros_neste_aluno = 0
        
        # --- FASE 2: AUDITORIA ISOLADA POR COLUNA ---
        for coluna in COLUNAS_AUDITORIA:
            if coluna not in df.columns:
                continue
                
            dado_csv = str(linen[coluna]) if pd.notna(linen[coluna]) else ""
            valor_buscado = dado_csv
            
            if coluna in ['mes_nasc', 'mes_defesa']:
                mes_limpo = normalizar_texto(dado_csv)
                if mes_limpo in MAPA_MESES:
                    valor_buscado = MAPA_MESES[mes_limpo]
            
            dado_norm = normalizar_texto(valor_buscado)
            status = "ERRO"
            novo_valor = dado_csv
            
            # 1. n_registro (Adaptado para espaços fantasmas no Processo SEI)
            if coluna == 'n_registro':
                processo_atual = str(linen.get('n_processo', '')).strip()
                proc_limpo = re.sub(r'[^0-9]', '', processo_atual)
                
                # Cria uma máscara dinâmica que aceita espaços da falha de leitura (ex: / 2026)
                if len(proc_limpo) == 17:
                    p = proc_limpo
                    proc_flex = rf'{p[:5]}[\.\s]*{p[5:11]}[/\s]*{p[11:15]}[-\s]*{p[15:]}'
                    padrao_registro = rf'\b(\d+)\s+{proc_flex}'
                else:
                    padrao_registro = rf'\b(\d+)\s+{re.escape(processo_atual)}\b'
                    
                match_reg = re.search(padrao_registro, texto_livro_norm, re.IGNORECASE)
                
                if match_reg:
                    reg_pdf = match_reg.group(1).strip()
                    if str(dado_csv).strip() == reg_pdf:
                        status = "OK"
                    else:
                        novo_valor = reg_pdf
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 2. n_processo
            elif coluna == 'n_processo':
                dado_limpo = re.sub(r'[^0-9]', '', dado_csv)
                bloco_limpo = re.sub(r'[^0-9]', '', bloco_do_aluno)
                formato_perfeito = r'^\d{5}\.\d{6}/\d{4}-\d{2}$'
                
                if re.match(formato_perfeito, dado_csv) and dado_limpo in bloco_limpo:
                    status = "OK"
                else:
                    padrao_sei = r'\d{5}[\.\s]*\d{6}[/\s]*\d{4}[-\s]*\d{2}'
                    match = re.search(padrao_sei, bloco_do_aluno)
                    if match:
                        pesca = re.sub(r'[^0-9]', '', match.group())
                        if len(pesca) == 17:
                            novo_valor = f"{pesca[:5]}.{pesca[5:11]}/{pesca[11:15]}-{pesca[15:]}"
                            status = "CORRIGIDO_N3"
                    else:
                        status = "ERRO"

            # 3. n_rg
            elif coluna == 'n_rg':
                padrao_rg = r'nao se aplica\s+(.+?)\s+(?:[a-z]{2,7}\s*/\s*[a-z]{2}|\bpf\b)\s+\d{3}\.\d{3}'
                match_rg = re.search(padrao_rg, bloco_do_aluno, re.IGNORECASE)
                if match_rg:
                    rg_real_pdf = match_rg.group(1).strip().upper()
                    if str(dado_csv).strip().upper() == rg_real_pdf:
                        status = "OK"
                    else:
                        novo_valor = rg_real_pdf
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 4. emissor_rg
            elif coluna == 'emissor_rg':
                padrao_emissor = r'nao se aplica\s+[a-zA-Z0-9\.\-\s]+?\s+([a-z]{2,7}\s*/\s*[a-z]{2}|\bpf\b)'
                match_emissor = re.search(padrao_emissor, bloco_do_aluno, re.IGNORECASE)
                if match_emissor:
                    emissor_real_pdf = match_emissor.group(1).replace(' ', '').upper()
                    dado_csv_limpo = str(dado_csv).replace(' ', '').upper()
                    if dado_csv_limpo == emissor_real_pdf:
                        status = "OK"
                    else:
                        novo_valor = emissor_real_pdf
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 5. Datas (Nascimento e Defesa)
            elif coluna in ['dia_nasc', 'mes_nasc', 'ano_nasc', 'dia_defesa', 'mes_defesa', 'ano_defesa']:
                prefixo = 'nasc' if 'nasc' in coluna else 'defesa'
                dia = str(linen.get(f'dia_{prefixo}', '')).strip()
                mes = str(linen.get(f'mes_{prefixo}', '')).strip()
                ano = str(linen.get(f'ano_{prefixo}', '')).strip()
                
                dia_fmt = dia.zfill(2) if dia.isdigit() else ""
                mes_num = MAPA_MESES.get(normalizar_texto(mes), "")
                mes_fmt = mes_num.zfill(2) if mes_num else ""
                ano_fmt = ano if ano.isdigit() and len(ano) == 4 else ""
                
                data_csv_limpa = f"{dia_fmt}{mes_fmt}{ano_fmt}"
                padrao_data = r'\b(\d{2})[/\.](\d{2})[/\.](\d{4})\b'
                todas_as_datas = re.findall(padrao_data, bloco_do_aluno)
                
                data_real = None
                if prefixo == 'nasc' and len(todas_as_datas) >= 1:
                    data_real = todas_as_datas[0]
                elif prefixo == 'defesa' and len(todas_as_datas) >= 2:
                    data_real = todas_as_datas[1]
                    
                if data_real:
                    dia_pdf, mes_pdf, ano_pdf = data_real
                    data_pdf_limpa = f"{dia_pdf}{mes_pdf}{ano_pdf}"
                    
                    if data_csv_limpa == data_pdf_limpa:
                        status = "OK"
                    else:
                        if 'dia' in coluna: novo_valor = dia_pdf
                        elif 'mes' in coluna: 
                            meses_inversos = {v: k for k, v in MAPA_MESES.items()}
                            novo_valor = meses_inversos.get(str(int(mes_pdf)), mes_pdf).lower()
                        elif 'ano' in coluna: novo_valor = ano_pdf
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 6. Naturalidade (Adaptado para espaços fantasmas na UF, ex: "s c", "a m")
            elif coluna in ['cidade_natural', 'uf_natural']:
                # O trecho ([a-z]\s*[a-z]) agora permite que o OCR tenha colocado espaço na sigla
                padrao_naturalidade = r'\b\d{2}[/\.]\d{2}[/\.]\d{4}\b\s*([a-z\s\-]+?)\s*/\s*([a-z]\s*[a-z])\b'
                match_nat = re.search(padrao_naturalidade, bloco_do_aluno, re.IGNORECASE)
                
                if match_nat:
                    cidade_pdf = match_nat.group(1).strip()
                    # Remove os espaços internos da UF e deixa maiúsculo (ex: "a m" vira "AM")
                    uf_pdf = match_nat.group(2).replace(' ', '').strip().upper()
                    
                    if coluna == 'cidade_natural':
                        if normalizar_texto(dado_csv) == normalizar_texto(cidade_pdf):
                            status = "OK"
                        else:
                            status = "ERRO"
                    elif coluna == 'uf_natural':
                        dado_csv_limpo = re.sub(r'[^A-Z]', '', str(dado_csv).upper())
                        if dado_csv_limpo == uf_pdf:
                            status = "OK"
                        else:
                            novo_valor = uf_pdf
                            status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 7. nome_aluno (Adaptado para espaços fantasmas na âncora do SEI)
            elif coluna == 'nome_aluno':
                # A âncora do SEI agora usa a máscara genérica e tolera espaços
                padrao_sei_flex = r'\d{5}[\.\s]*\d{6}[/\s]*\d{4}[-\s]*\d{2}'
                padrao_nome = padrao_sei_flex + r'\s+([a-z\s]+?)\s+nao\s+se\s+aplica'
                match_nome = re.search(padrao_nome, bloco_do_aluno, re.IGNORECASE)
                
                if match_nome:
                    nome_pdf = match_nome.group(1).strip()
                    if normalizar_texto(dado_csv) == normalizar_texto(nome_pdf):
                        status = "OK"
                    else:
                        status = "ERRO"
                else:
                    status = "ERRO"

            # 7.1. curso_conclusao
            elif coluna == 'curso_conclusao':
                match_inicio = re.search(r'\b(?:mestrado|doutorado)\s+em\s+', bloco_do_aluno, re.IGNORECASE)
                match_fim = re.search(r'\b(?:mestre|mestra)\b', bloco_do_aluno, re.IGNORECASE)
                if match_inicio and match_fim and match_fim.start() > match_inicio.end():
                    recheio = bloco_do_aluno[match_inicio.start() : match_fim.start()].strip()
                    recheio_sem_uf = re.sub(r'/[a-z]{2}$', '', recheio, flags=re.IGNORECASE).strip()
                    campi_uffs = r'\s+(chapeco|cerro\s+largo|erechim|passo\s+fundo|laranjeiras\s+do\s+sul|realeza)$'
                    curso_extraido = re.sub(campi_uffs, '', recheio_sem_uf, flags=re.IGNORECASE).strip()
                    curso_norm_pdf = normalizar_texto(curso_extraido)
                    curso_ouro = CURSOS_OFICIAIS.get(curso_norm_pdf, curso_extraido.upper())
                    
                    if str(dado_csv).strip() == curso_ouro:
                        status = "OK"
                    else:
                        novo_valor = curso_ouro
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 8. gen_titulo
            elif coluna == 'gen_titulo':
                padrao_titulo = r'\b(mestre|mestra)\s+\d{2}[/\.]\d{2}[/\.]\d{4}\b'
                match_titulo = re.search(padrao_titulo, bloco_do_aluno, re.IGNORECASE)
                if match_titulo:
                    titulo_real = match_titulo.group(1).strip().lower().capitalize()
                    if titulo_real == 'Mestra':
                        pacote = {'gen_titulo': 'Mestra', 'gen_pessoa': 'Titulada', 'gen_nasc': 'nascida', 'gen_portador': 'portadora'}
                    else:
                        pacote = {'gen_titulo': 'Mestre', 'gen_pessoa': 'Titulado', 'gen_nasc': 'nascido', 'gen_portador': 'portador'}
                    
                    df.at[index, 'gen_pessoa'] = pacote['gen_pessoa']
                    df.at[index, 'gen_nasc'] = pacote['gen_nasc']
                    df.at[index, 'gen_portador'] = pacote['gen_portador']

                    if str(dado_csv).strip().lower().capitalize() == pacote['gen_titulo']:
                        status = "OK"
                    else:
                        novo_valor = pacote['gen_titulo']
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # 9. n_folha (Ajustado para o erro de OCR "registr o")
            elif coluna == 'n_folha':
                texto_para_tras = texto_livro_norm[:indice_aluno]
                
                # A mágica do \s* permite encontrar tanto "registro" quanto "registr o"
                padrao_folha = r'\b(\d{1,4})\s+registr\s*o\b'
                numeros_folha = re.findall(padrao_folha, texto_para_tras, re.IGNORECASE)
                
                if numeros_folha:
                    # Pega o último número encontrado (a página mais recente antes do aluno)
                    folha_real_pdf = numeros_folha[-1]
                    
                    if str(dado_csv).strip() == folha_real_pdf:
                        status = "OK"
                    else:
                        novo_valor = folha_real_pdf
                        status = "CORRIGIDO_N3"
                else:
                    status = "ERRO"

            # --- VEREDITO E ATUALIZAÇÃO DO DATAFRAME ---
            if status == "OK":
                # print(f"  ✅ {coluna.upper()}: OK ({dado_csv})")
                status = "OK"
            elif status == "CORRIGIDO_N1":
                print(f"  ✨ {coluna.upper()}: Formatado (Nível 1) -> De: '{dado_csv}' Para: '{novo_valor}'")
                df.at[index, coluna] = novo_valor
                correcoes_totais += 1
            elif status == "CORRIGIDO_N2":
                print(f"  🔧 {coluna.upper()}: Corrigido por Semelhança (Nível 2) -> De: '{dado_csv}' Para: '{novo_valor}'")
                df.at[index, coluna] = novo_valor
                correcoes_totais += 1
            elif status == "CORRIGIDO_N3":
                print(f"  🎯 {coluna.upper()}: Pescado/Recriado (Nível 3) -> De: '{dado_csv}' Para: '{novo_valor}'")
                df.at[index, coluna] = novo_valor
                correcoes_totais += 1
            elif status == "ERRO":
                vazio_aviso = "[Vazio]" if not dado_csv.strip() else f"'{dado_csv}'"
                print(f"  ❌ {coluna.upper()}: ERRO CRÍTICO. Não encontrado {vazio_aviso}")
                erros_neste_aluno += 1
                erros_totais += 1
                
        if erros_neste_aluno > 0:
            alunos_com_erro += 1

    # SALVA O RESULTADO
    arquivo_saida = 'database_corrigido.csv'
    df.to_csv(arquivo_saida, index=False)

    print("\n" + "="*80)
    print(" 📊 RELATÓRIO FINAL DA AUDITORIA")
    print("="*80)
    print(f"Total de alunos analisados: {total_alunos}")
    print(f"Correções automáticas aplicadas: {correcoes_totais}")
    
    if erros_totais == 0:
        print(f"🟢 STATUS EXCELENTE: Arquivo 100% validado salvo como '{arquivo_saida}'.")
    else:
        print(f"🔴 ATENÇÃO: Restaram {erros_totais} erro(s) em {alunos_com_erro} aluno(s).")

if __name__ == "__main__":
    auditar_banco_de_dados()