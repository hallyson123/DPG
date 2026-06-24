from google import genai
from google.genai import types # Import necessário para forçar o JSON na saída
import config

def extrair_dados_livro(caminho_pdf: str) -> str:
    # inicia o Gemini usando a chave que ta em config
    client = genai.Client(api_key=config.API_KEY)
    
    with open(caminho_pdf, "rb") as f:
        pdf_bytes = f.read()
        
    prompt = """
    Analise o documento do livro de registro de diplomas em anexo.
    Extraia as informações de todos os alunos e retorne estritamente no formato JSON estruturado abaixo,
    onde cada objeto do array representa um aluno extraído do livro.

    Regras Críticas de Gênero (Concordância Gramatical):
    - Olhe o campo "Titulo Obtido" de cada aluno no livro de registros.
    - Se o título obtido for "Mestra", preencha obrigatoriamente:
        "gen_pessoa": "Titulada", "gen_titulo": "Mestra", "gen_portador": "portadora", "gen_nasc": "nascida"
    - Se o título obtido for "Mestre", preencha obrigatoriamente:
        "gen_pessoa": "Titulado", "gen_titulo": "Mestre", "gen_portador": "portador", "gen_nasc": "nascido"

    Regras Críticas de Fatiamento e Extração de Campos:
    - nome_aluno: O nome completo do aluno extraído do campo "Nome Civil", convertido totalmente para MAIÚSCULAS. (Não ignore se o nome tiver apóstrofo ('), coloque também)
    - n_processo: O número do processo administrativo no formato padrão do SEI (Ex: "23205.xxxxxx/xxxx-xx").
    - n_rg: Extraia exatamente como está no livro o número de documento de identidade. (matendo o formato e suas pontuações e traços)
    - emissor_rg: Mantenha o órgão expedidor completo junto com a UF.
    - cidade_natural e uf_natural: Quebre o campo "Cidade/UF" de naturalidade.
    - curso_conclusao: O nome completo do curso exatamente como está escrito no livro.

    Regras Críticas para Fatiamento de Datas:
    - Identifique a data de nascimento e a data de defesa da dissertação de cada aluno.
    - Quebre as duas datas em dia, mês por extenso e ano, respeitando o seguinte formato:
        "dia_nasc" / "dia_defesa": O dia com dois dígitos (Ex: "05", "12", "28").
        "mes_nasc" / "mes_defesa": O nome do mês por extenso escrito inteiramente em letras MINÚSCULAS (Ex: "janeiro", "março", "setembro").
        "ano_nasc" / "ano_defesa": O ano com quatro dígitos (Ex: "1998", "2026").

    Regras Críticas de Exclusão e Numeração (ATENÇÃO MÁXIMA):
    - n_registro: O número sequencial do registro do diploma individual de cada aluno no campo "Registro".
    - n_folha: O número correspondente à folha do livro onde consta o termo/registro do aluno (fica no canto inferior direito).
    - n_livro: Por padrão, deixe: 03-SS.
    - EXTRAÇÃO ESTRITA E DESCARTES: Você deve extrair EXATAMENTE os campos solicitados. Dados da coluna "Form." (geralmente indicando o ano/semestre de conclusão, ex: "2024.1", "2023/2") NÃO pertencem a nenhum campo estruturado. Eles DEVEM SER DESCARTADOS. Nunca preencha "n_processo", "n_rg", "n_registro" ou qualquer outro campo com a informação dessa coluna.

    EXEMPLO DE COMPORTAMENTO ESPERADO:
    Se no PDF constar: "João Silva, Form. 2023.1, RG 1234"
    Comportamento Correto: O valor "2023.1" é ignorado e não é inserido em nenhum lugar do JSON de saída.

    A saída deve ser uma lista JSON com as chaves exatas abaixo:
    [
        {
            "gen_pessoa": "",
            "gen_titulo": "",
            "nome_aluno": "",
            "cidade_natural": "",
            "uf_natural": "",
            "gen_portador": "",
            "n_rg": "",
            "emissor_rg": "",
            "gen_nasc": "",
            "dia_nasc": "",
            "mes_nasc": "",
            "ano_nasc": "",
            "curso_conclusao": "",
            "dia_defesa": "",
            "mes_defesa": "",
            "ano_defesa": "",
            "n_registro": "",
            "n_folha": "",
            "n_livro": "",
            "n_processo": ""
        }
    ]
    """
    
    resposta = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=[
            types.Part.from_bytes(data=pdf_bytes, mime_type='application/pdf'),
            prompt
        ],
        # MÁGICA DE BACKEND: Trava a API para devolver JSON puro, sem textos ou markdowns!
        config=types.GenerateContentConfig(
            response_mime_type="application/json"
        )
    )
    return resposta.text