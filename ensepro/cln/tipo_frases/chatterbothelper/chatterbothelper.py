# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from string import Template
from chatterbot import ChatBot
from ensepro import configuracoes
from ensepro.cln.tipo_frases import TipoFrase
from ensepro.constantes import ChaterbotConstantes, LoggerConstantes

logger = LoggerConstantes.get_logger(LoggerConstantes.MODULO_CHATTERBOT_HELPER)

chatter_bot = None
# termos_relevantes = Lista de palavras que devem ser consideradas para obtenção do tipo da frase
termos_relevantes = {}

PALAVRAS_CHAVE = {
    "termo_relevante": "#"
}


def get_tipo(frase):
    if not chatter_bot:
        criar_chatterbot()
        iniciar_treinamento()
        logger.debug("termos_relevantes: %s", termos_relevantes)

    logger.info("Obtendo tipo da frase: %s", frase)
    frase_termos_relevantes = __get_termos_relevantes(frase)

    frase_string = frase_termos_relevantes["termos"]
    ids = frase_termos_relevantes["ids"]

    st = chatter_bot.get_response(frase_string)
    tipo = TipoFrase(st, ids)

    logger.debug("Retorno do chatter_bot: [%s]", st)
    logger.info("Tipo obtido: [%s]", tipo)
    return tipo


def criar_chatterbot():
    logger.info("Criando Chatterbot.")

    nome = configuracoes.get_config(ChaterbotConstantes.NOME)
    storage_adapter = configuracoes.get_config(ChaterbotConstantes.STORAGE_ADAPTER)
    logic_adapters = configuracoes.get_config(ChaterbotConstantes.LOGIC_ADAPTERS)
    trainer = configuracoes.get_config(ChaterbotConstantes.TRAINER)
    show_training_progress = configuracoes.get_config(ChaterbotConstantes.SHOW_TRAINING_PROGRESS)

    logger.debug("Configurações carregadas para criação do Chatterbot: "
                 "[name=%s, storage_adapter=%s, logic_adapters=%s, trainer=%s]",
                 nome, storage_adapter, logic_adapters, trainer)

    global chatter_bot
    chatter_bot = ChatBot(
            name=nome,
            storage_adapter=storage_adapter,
            logic_adapters=logic_adapters,
            trainer=trainer,
            show_training_progress=show_training_progress
    )

    logger.info("Chatterbot criado.")


def iniciar_treinamento():
    if not chatter_bot:
        raise Exception("Chatterbot deve ser criado antes do treinamento!")

    logger.info("Iniciando treinamento chatterbot")

    treinamento_carregado = configuracoes.get_config(ChaterbotConstantes.TREINAMENTO)
    read_only = configuracoes.get_config(ChaterbotConstantes.READ_ONLY)
    logger.debug("Treinamento carregado: [%s]", treinamento_carregado)

    dicionario = treinamento_carregado["dicionario"]
    mapeamento = treinamento_carregado["mapeamento"]

    treinamento_normalizado = __normalizar_treinamento(dicionario, mapeamento)
    logger.debug("Treinamento normalizado: [%s]", treinamento_normalizado)

    logger.info("Treinando....")
    chatter_bot.train(treinamento_normalizado)
    chatter_bot.read_only = read_only

    logger.info("Treinamento executado")


def __normalizar_treinamento(dicionario, mapeamento):
    """
    Cria a lista de treinamento do chatterbot.
    Formato da lista: [padrão, tipo, padrão, tipo, ...]
                      [entrada do usuário, resposta do chatterbot, ....]
    :param dicionario:
    :param mapeamento:
    :return:
    """
    treinamento_normalizado = []
    for tipo in mapeamento:
        for padrao in mapeamento[tipo]:
            padrao_normalizado = __normalizar_padrao(padrao, dicionario)
            treinamento_normalizado.append(padrao_normalizado)
            treinamento_normalizado.append(tipo)

    return treinamento_normalizado


def __normalizar_padrao(padrao, dicionario):
    """
    Troca as variáveis do padrão pelo seu respectivo valor do dicionário.
    Exemplo:
        dicionario: { "quando": "#quando <clb> <interr>" }
        padrão: "$quando"
        padrão normalizado: "#quando <clb> <interr>"

    :param padrao: padrão que indica um tipo
    :param dicionario:
    :return:
    """
    padrao_normalizado = Template(padrao).substitute(dicionario)
    logger.debug("Padrão'%s' normalizado: '%s'", padrao, padrao_normalizado)
    __extrair_termos_relevantes(padrao_normalizado)
    return __remover_palavras_chaves(padrao_normalizado)


def __extrair_termos_relevantes(padrao):
    """
    Extrai os termos relevantes do padrão dos tipos
    padrão 1:
        map: $quanto
        normalizado: "#quanto <clb> <interr> <quant> DET F P"
        termos_relevantes = { "quanto": {"fim": True} }

    padrão 2:
        map: "$quanto $vez"
        normalizado: "#quanto <clb> <interr> <quant> DET F P #vez <temp> F P"
        termos_relevantes = { "quanto": { "fim": False, "vez": { "fim": True } } }

    padrão 3:
        map: "$em $que $dia"
        normalizado: "#em <clb> <*> #que <clb> <interr> DET #dia <temp> <dur> <per> <unit> M S"
        termos_relevantes:  { "em": { "fim": False, "que": { "fim": False, "dia": { "fim": True } } } }

    padrão 1 + padrão 2:
        termos_relevantes = { "quanto": { "fim": True, "vez": { "fim": True } } }

    :param padrao: padrão que indica um tipo
    """
    termos_relevantes_temp = termos_relevantes
    for trecho in padrao.split():
        if trecho[0] == PALAVRAS_CHAVE["termo_relevante"]:
            termo = trecho[1:]
            logger.debug("Termo relevante: %s", termo)

            if termo not in termos_relevantes_temp:
                termos_relevantes_temp[termo] = {}

            termos_relevantes_temp = termos_relevantes_temp[termo]
            termos_relevantes_temp["fim"] = termos_relevantes_temp.get("fim", False)

    termos_relevantes_temp["fim"] = True


def __remover_palavras_chaves(padrao):
    for nome, palavra_chave in PALAVRAS_CHAVE.items():
        padrao = padrao.replace(palavra_chave, "")
    return padrao


# TODO revisar e verificar alguma possível otimização...
def __get_termos_relevantes(frase):
    logger.debug("Montando frase em texto com apenas termos relevantes")
    termos_relevantes_temp = termos_relevantes
    frase_string = ""
    frase_string_temp = ""
    ids = []
    ids_temp = []

    for palavra in frase.get_palavras(__possui_palavra_original):
        if palavra.palavra_canonica in termos_relevantes_temp:
            termos_relevantes_temp = termos_relevantes_temp[palavra.palavra_canonica]

            frase_string_temp = ' '.join([frase_string_temp.strip(), palavra.palavra_canonica, ' '.join(palavra.tags), ''])
            ids_temp.append(palavra.id)

            if termos_relevantes_temp["fim"]:
                frase_string = str(frase_string_temp)
                ids = list(ids_temp)

        else:
            # Se achou partes de um tipo mas não foi um tipo completo
            if (len(ids_temp) > 0):
                break

    logger.debug("String da frase criada: [frase_string='%s', ids=%s]", frase_string, ids)
    return {
        "termos": frase_string,
        "ids": ids
    }


def __possui_palavra_original(frase, palavra, *args):
    return bool(palavra.palavra_original)
