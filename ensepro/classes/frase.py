# -*- coding: utf-8 -*-
"""
@project ensepro
@since 25/02/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable


class Frase:
    def __init__(self, id=None, frase=None, palavras=None):
        self.id = id
        self.palavras = palavras
        self.frase_original = frase
        self.__arvore = None
        self.__tipo = None
        self.__locucao_verbal = None
        self.__termos_relevantes = None
        self.__voz = None
        self.__complementos_nominais = None
        self.__resposta = None

    @property
    def arvore(self):
        if self.__arvore:
            return self.__arvore

        from ensepro.conversores import arvore_conversor
        self.__arvore = arvore_conversor.from_frase(self)
        return self.__arvore

    @property
    def tipo(self):
        if self.__tipo:
            return self.__tipo

        from ensepro.cln import tipo_frases
        self.__tipo = tipo_frases.get_tipo(self)
        return self.__tipo

    @property
    def locucao_verbal(self):
        if self.__locucao_verbal:
            return self.__locucao_verbal

        from ensepro.cln import locucao_verbal
        self.__locucao_verbal = locucao_verbal.get(self)
        return self.__locucao_verbal

    @property
    def termos_relevantes(self):
        if self.__termos_relevantes:
            return self.__termos_relevantes

        from ensepro.cln import termos_relevantes
        self.__termos_relevantes = termos_relevantes.get(self)
        return self.__termos_relevantes

    @property
    def voz(self):
        if self.__voz:
            return self.__voz

        from ensepro.cln import voz
        self.__voz = voz.get(self)
        return self.__voz

    @property
    def complementos_nominais(self):
        if self.__complementos_nominais:
            return self.__complementos_nominais

        from ensepro.cln import complementos_nominais
        self.__complementos_nominais = complementos_nominais.get(self)
        return self.__complementos_nominais

    def set_resposta(self, resposta):
        self.__resposta = resposta

    @property
    def resposta(self):
        return self.__resposta

    def get_palavras(self, condicao, **args):
        """
        Percorre a lista de palavras da frase validando a condicao passada.

        :param condicao: deve ser um função que recebe a frase e uma de suas palavras por parametro e retorna uma valor booleano
        ex: def condicao(frase, palavra, *args) -> bool
        :return: lista de palavras das quais a função 'condicao' retornou True
        """
        if (callable(condicao)):
            return [palavra for palavra in self.palavras if condicao(self, palavra, args)]

        raise TypeError("Parametro 'condição' deve ser uma função.")

    def __to_json__(self):
        return {
            "id": self.id,
            "palavras": [palavra.__to_json__() for palavra in self.palavras],
            "arvore": str(self.__arvore),
            "tipo": self.__tipo,
            "locucao_verbal": self.__locucao_verbal,
            "termos_relevantes": [palavra.__to_json__() for palavra in
                                  self.__termos_relevantes] if self.__termos_relevantes else None,
            "voz": str(self.__voz),
            "complementos_nominais": self.__complementos_nominais,
            "resposta": self.__resposta
        }

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        return str(self) == str(other)

    def __str__(self):
        return \
            "Frase={{id={0}, palavras={1}, tipo={2}, locucao_verbal={3}, voz={4}}}" \
            "".format(
                str(self.id),
                str(self.palavras),
                str(self.__tipo),
                str(self.__locucao_verbal),
                str(self.__voz)
            )

    def __repr__(self):
        return self.__str__
