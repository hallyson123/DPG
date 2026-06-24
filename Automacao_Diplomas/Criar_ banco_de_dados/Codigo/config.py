import os
from dotenv import load_dotenv

load_dotenv()

#chave de api do Gemini
API_KEY = os.getenv("API_KEY", "CHAVE_NAO_CONFIGURADA")

# chave api do Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "CHAVE_NAO_CONFIGURADA")

# configuração das colunas da database.csv
COLUNAS_DATABASE = [
    "gen_pessoa", "gen_titulo", "nome_aluno", "cidade_natural", "uf_natural", 
    "gen_portador", "n_rg", "emissor_rg", "gen_nasc", "dia_nasc", 
    "mes_nasc", "ano_nasc", "curso_conclusao", "sigla_curso", "dia_defesa", 
    "mes_defesa", "ano_defesa", "area", "dia_emissao", "mes_emissao", 
    "ano_emissao", "n_registro", "n_folha", "n_livro", "n_processo", "portaria"
]

# Dicionario com infos de Areas de concentração e Portarias
# Chave: Curso -> Valor: (sigla, area, portaria)
MAPEAMENTO_CURSOS = {
    "MESTRADO EM AGROECOLOGIA E DESENVOLVIMENTO RURAL SUSTENTÁVEL": {
        "sigla": "PPGADR",
        "area": "Agroecologia e Desenvolvimento Rural Sustentável",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 128."
    },
    "MESTRADO EM AMBIENTE E TECNOLOGIAS SUSTENTÁVEIS": {
        "sigla": "PPGATS",
        "area": "Monitoramento, Controle e Gestão Ambiental",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 89."
    },
    "MESTRADO EM CIÊNCIA E TECNOLOGIA AMBIENTAL": {
        "sigla": "PPGCTA",
        "area": "Produção Sustentável e Conservação Ambiental",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "DOUTORADO EM CIÊNCIA E TECNOLOGIA AMBIENTAL": {
        "sigla": "PPGCTA",
        "area": "Produção Sustentável e Conservação Ambiental",
        "portaria": "Portaria n.° 2149, do Ministério da Educação, de 26/12/2023, publicado no D.O.U. em 27/12/2023, Edição 245, Seção 1, pág. 71."
    },
    "MESTRADO EM CIÊNCIA E TECNOLOGIA DE ALIMENTOS": {
        "sigla": "PPGCTAL",
        "area": "Biociência e Tecnologia de Alimentos",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO EM CIÊNCIAS BIOMÉDICAS": {
        "sigla": "PPGCB",
        "area": "Ciências Biomédicas",
        "portaria": "Portaria n.° 540, do Ministério da Educação, de 15/06/2020, publicado no D.O.U. em 17/06/2020, Edição 114, Seção 1, pág. 57."
    },
    "MESTRADO EM DESENVOLVIMENTO E POLÍTICAS PÚBLICAS": {
        "sigla": "PPGDPP",
        "area": "Desenvolvimento e Políticas Públicas",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 129."
    },
    "DOUTORADO EM DESENVOLVIMENTO E POLÍTICAS PÚBLICAS": {
        "sigla": "PPGDPP",
        "area": "Desenvolvimento e Políticas Públicas",
        "portaria": "Portaria n.° 2149, do Ministério da Educação, de 26/12/2023, publicado no D.O.U. em 27/12/2023, Edição 245, Seção 1, pág. 71."
    },
    "MESTRADO EM EDUCAÇÃO": {
        "sigla": "PPGE",
        "area": "Educação",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO PROFISSIONAL EM EDUCAÇÃO": {
        "sigla": "PPGPE",
        "area": "Práticas educativas",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO EM ENSINO DE CIÊNCIAS": {
        "sigla": "PPGEC",
        "area": "Ensino De Ciências",
        "portaria": "Portaria n.° 486, do Ministério da Educação, de 14/05/2020, publicado no D.O.U. em 18/05/2020, Edição 93, Seção 1, pág. 410."
    },
    "MESTRADO EM ESTUDOS LINGUÍSTICOS": {
        "sigla": "PPGEL",
        "area": "Estudos Linguísticos",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, published no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 136."
    },
    "DOUTORADO EM ESTUDOS LINGUÍSTICOS": {
        "sigla": "PPGEL",
        "area": "Estudos Linguísticos",
        "portaria": "Portaria nº 997, do Ministério da Educação, de 23/11/2020, publicado no D.O.U. em 24/11/2020, Edição 224, Seção I, pág. 26."
    },
    "MESTRADO EM FILOSOFIA": {
        "sigla": "PPGFIL",
        "area": "Filosofia",
        "portaria": "Portaria n.° 486, do Ministério da Educação, de 14/05/2020, publicado no D.O.U. em 18/05/2020, Edição 93, Seção 1, pág. 410."
    },
    "MESTRADO EM GEOGRAFIA": {
        "sigla": "PPGGeo",
        "area": "Natureza, Sociedade e espaço Geográfico",
        "portaria": "Portaria n.° 486, do Ministério da Educação, de 14/05/2020, publicado no D.O.U. em 18/05/2020, Edição 93, Seção 1, pág. 410."
    },
    "MESTRADO EM HISTÓRIA": {
        "sigla": "PPGH",
        "area": "Fronteiras, Migrações e Sociedades",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 124."
    },
    "DOUTORADO EM HISTÓRIA": {
        "sigla": "PPGH",
        "area": "Fronteiras, Migrações e Sociedades",
        "portaria": "Portaria n.° 2149, do Ministério da Educação, de 26/12/2023, publicado no D.O.U. em 27/12/2023, Edição 245, Seção 1, pág. 71."
    },
    "MESTRADO INTERDISCIPLINAR EM CIÊNCIAS HUMANAS": {
        "sigla": "PPGICH",
        "area": "Saberes e Identidades",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO PROFISSIONAL EM MATEMÁTICA": {
        "sigla": "PROFMAT",
        "area": "Matemática na Educação Básica",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO PROFISSIONAL EM HISTÓRIA EM REDE NACIONAL": {
        "sigla": "PROF HISTÓRIA",
        "area": "História",
        "portaria": "Portaria n.° 609, do Ministério da Educação, de 14/03/2019, publicado no D.O.U. em 18/03/2019, Edição 52, Seção 1, pág. 101."
    },
    "MESTRADO EM SAÚDE, BEM-ESTAR E PRODUÇÃO ANIMAL SUSTENTÁVEL NA FRONTEIRA SUL": {
        "sigla": "PPGSBPAS",
        "area": "Saúde, Bem-Estar e Produção Animal Sustentável na Fronteira Sul",
        "portaria": "Portaria n.° 129, do Ministério da Educação, de 20/02/2018, publicado no D.O.U. em 21/02/2018, Edição 35, Seção 1, pág. 19."
    },
    "MESTRADO EM ENFERMAGEM": {
        "sigla": "PPGENF",
        "area": "Enfermagem em Saúde Coletiva",
        "portaria": "Portaria n.° 2149, do Ministério da Educação, de 26/12/2023, publicado no D.O.U. em 27/12/2023, Edição 245, Seção 1, pág. 71."
    }
}
