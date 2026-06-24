# utils.py
import re
import os
import unicodedata
import difflib
import pandas as pd
from pypdf import PdfReader

def normalizar_texto(texto):
    """Remove acentos e espaços extras, mas MANTÉM a pontuação padronizada."""
    if pd.isna(texto) or not str(texto).strip():
        return ""
    texto = str(texto)
    texto = re.sub(r'[‘’´`]', "'", texto)
    texto = re.sub(r'[“”]', '"', texto)
    texto = re.sub(r'[–—]', '-', texto)
    texto_limpo = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo.lower()).strip()
    return texto_limpo

def ler_texto_completo_pdf(caminho_pdf):
    if not os.path.exists(caminho_pdf):
        print(f"❌ Erro: O arquivo '{caminho_pdf}' não foi encontrado.")
        return ""
    print(f"⏳ Lendo o livro original ({caminho_pdf})...")
    leitor = PdfReader(caminho_pdf)
    texto_total = ""
    for pagina in leitor.pages:
        texto_total += pagina.extract_text() + " "
    return texto_total

def busca_fuzzy(alvo, bloco, limiar=0.85):
    """NÍVEL 2: Procura por semelhança para arrumar erros de digitação/OCR."""
    if not alvo or not bloco: return None
    palavras_alvo = alvo.split()
    palavras_bloco = bloco.split()
    tamanho = len(palavras_alvo)
    melhor_match = None
    maior_ratio = 0.0

    for janela_tam in [tamanho, tamanho + 1, tamanho - 1]:
        if janela_tam <= 0 or janela_tam > len(palavras_bloco): continue
        for i in range(len(palavras_bloco) - janela_tam + 1):
            trecho = " ".join(palavras_bloco[i:i+janela_tam])
            ratio = difflib.SequenceMatcher(None, alvo, trecho).ratio()
            if ratio > maior_ratio:
                maior_ratio = ratio
                melhor_match = trecho

    if maior_ratio >= limiar:
        return melhor_match
    return None

def capitalizar_correto(coluna, texto):
    if coluna in ['nome_aluno', 'curso_conclusao']:
        return texto.upper()
    elif coluna in ['cidade_natural']:
        return texto.title()
    return texto