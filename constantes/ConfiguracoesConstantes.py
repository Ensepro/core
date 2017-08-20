"""
@project ensepro
@since 20/07/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

# Caminho do arquivo de configuração
ARQUIVO_CONFIGURACAO = "../configuracoes/configuracoes.json"

# Servidores
SERVIDOR_VIRTUOSO = "virtuoso"
SERVIDOR_PALAVRAS = "palavras"

# Chaves de valores do arquivo de configuração
CONFIG_FRASES = "frases"
CONFIG_ARQUIVO_FRASES = CONFIG_FRASES + "/arquivo_frases"
CONFIG_REGEX_PALAVRA_RELEVENTE = CONFIG_FRASES + "/regex_palavra_relevante"
CONFIG_REGEX_PALAVRA_VERBO = CONFIG_FRASES + "/regex_palavra_verbo"
CONFIG_REGEX_VOZ_PASSIVA = CONFIG_FRASES + "/regex_voz_passiva"

CONFIG_TIPO_FRASES = "tipos_frases"
CONFIG_SERVIDORES = "servidores"

CONFIG_ENDPOINT = CONFIG_SERVIDORES + "/{nome_servidor}/endpoint"
CONFIG_SERVICOS = CONFIG_SERVIDORES + "/{nome_servidor}/servicos"
CONFIG_SERVICO = CONFIG_SERVICOS + "/{nome_servico}"
CONFIG_QUERIES_SPARQL = CONFIG_SERVIDORES + "/{nome_servidor}/queries"

# Mensagens
MENSAGEM_CARREGANDO = "Carregando configurações [{fromFile}]."
MENSAGEM_CARREGAMENTO_SUCESSO = "Configurações carregadas com sucesso."
MENSAGEM_CARREGAMENTO_ERRO = "Não foi possível carregar as configurações do arquivo json[{fromFile}]."
