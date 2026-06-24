# config.py

# Dicionário de Ouro: Mapeia o texto limpo do PDF para a versão oficial com acentuação perfeita
CURSOS_OFICIAIS = {
    "mestrado em agroecologia e desenvolvimento rural sustentavel": "MESTRADO EM AGROECOLOGIA E DESENVOLVIMENTO RURAL SUSTENTÁVEL",
    "mestrado em ambiente e tecnologias sustentaveis": "MESTRADO EM AMBIENTE E TECNOLOGIAS SUSTENTÁVEIS",
    "mestrado em ciencia e tecnologia ambiental": "MESTRADO EM CIÊNCIA E TECNOLOGIA AMBIENTAL",
    "doutorado em ciencia e tecnologia ambiental": "DOUTORADO EM CIÊNCIA E TECNOLOGIA AMBIENTAL",
    "mestrado em ciencia e tecnologia de alimentos": "MESTRADO EM CIÊNCIA E TECNOLOGIA DE ALIMENTOS",
    "mestrado em ciencias biomedicas": "MESTRADO EM CIÊNCIAS BIOMÉDICAS",
    "mestrado em desenvolvimento e politicas publicas": "MESTRADO EM DESENVOLVIMENTO E POLÍTICAS PÚBLICAS",
    "doutorado em desenvolvimento e politicas publicas": "DOUTORADO EM DESENVOLVIMENTO E POLÍTICAS PÚBLICAS",
    "mestrado em educacao": "MESTRADO EM EDUCAÇÃO",
    "mestrado profissional em educacao": "MESTRADO PROFISSIONAL EM EDUCAÇÃO",
    "mestrado em ensino de ciencias": "MESTRADO EM ENSINO DE CIÊNCIAS",
    "mestrado em estudos linguisticos": "MESTRADO EM ESTUDOS LINGUÍSTICOS",
    "doutorado em estudos linguisticos": "DOUTORADO EM ESTUDOS LINGUÍSTICOS",
    "mestrado em filosofia": "MESTRADO EM FILOSOFIA",
    "mestrado em geografia": "MESTRADO EM GEOGRAFIA",
    "mestrado em historia": "MESTRADO EM HISTÓRIA",
    "doutorado em historia": "DOUTORADO EM HISTÓRIA",
    "mestrado interdisciplinar em ciencias humanas": "MESTRADO INTERDISCIPLINAR EM CIÊNCIAS HUMANAS",
    "mestrado profissional em matematica": "MESTRADO PROFISSIONAL EM MATEMÁTICA",
    "mestrado profissional em historia em rede nacional": "MESTRADO PROFISSIONAL EM HISTÓRIA EM REDE NACIONAL",
    "mestrado em saude, bem-estar e producao animal sustentavel na fronteira sul": "MESTRADO EM SAÚDE, BEM-ESTAR E PRODUÇÃO ANIMAL SUSTENTÁVEL NA FRONTEIRA SUL",
    "mestrado em enfermagem": "MESTRADO EM ENFERMAGEM"
}

MAPA_MESES = {
    'janeiro': '1', 'fevereiro': '2', 'marco': '3', 'abril': '4',
    'maio': '5', 'junho': '6', 'julho': '7', 'agosto': '8',
    'setembro': '9', 'outubro': '10', 'novembro': '11', 'dezembro': '12'
}

COLUNAS_AUDITORIA = [
    'n_registro', 'n_processo', 'nome_aluno', 'n_rg', 'emissor_rg', 
    'dia_nasc', 'mes_nasc', 'ano_nasc', 'cidade_natural', 'uf_natural', 
    'curso_conclusao', 'gen_titulo', 'dia_defesa', 'mes_defesa', 'ano_defesa', 'n_folha'
]