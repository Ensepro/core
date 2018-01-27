"""
@project ensepro
@since 19/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""
from ensepro.conversores import make_json_serializable
import re
from ensepro import configuracoes
from ensepro.constantes import ConfiguracoesConstantes

regex_palavra_verbo = re.compile(configuracoes.get_config(ConfiguracoesConstantes.REGEX_PALAVRA_VERBO))


class Palavra:

    def __init__(self, id=None, dados_palavra=None):
        self.id = id
        self.tags = dados_palavra["tags"] if dados_palavra else None
        self.nivel = int(dados_palavra["nivel"]) if dados_palavra else None
        self.tag_inicial = dados_palavra["tag_inicial"] if dados_palavra else None
        self.palavra_original = dados_palavra["palavra_original"] if dados_palavra else None
        self.palavra_canonica = dados_palavra["palavra_canonica"] if dados_palavra else None
        self.__sinonimos = None

    @property
    def sinonimos(self):
        if self.__sinonimos:
            return self.__sinonimos

        from ensepro import sinonimos, configuracoes
        from ensepro.sinonimos import Sinonimo
        from ensepro.constantes import ConfiguracoesConstantes
        linguagens = configuracoes.get_config(ConfiguracoesConstantes.SINONIMOS_LINGUAGENS)
        self.__sinonimos = {}

        for linguagem in linguagens:
            lista_sinonimo_string = sinonimos.get_sinonimos(self.palavra_canonica, linguagem)
            lista_sinonimos = [Sinonimo.from_string(sinonimo_string) for sinonimo_string in lista_sinonimo_string]
            self.__sinonimos[linguagem] = lista_sinonimos

        return self.__sinonimos

    def is_verbo(self):
        if regex_palavra_verbo.search(self.tag_inicial):
            return True
        return False

    def __to_json__(self):
        return {
            "id": self.id,
            "tag_inicial": self.tag_inicial,
            "palavra_original": self.palavra_original,
            "palavra_canonica": self.palavra_canonica,
            "tags": self.tags,
            "nivel": self.nivel,
            "sinonimos": self.__sinonimos
        }

    def __hash__(self):
        return hash(str(self.as_text))

    def __eq__(self, other):
        return str(self.as_text) == str(other.as_text)

    def __str__(self):
        if self.palavra_original:
            return "[{0}|{1}| {2}]".format(self.tag_inicial, self.id, self.palavra_original)
        return "{0}|{1}|".format(self.tag_inicial, self.id)

    def __repr__(self):
        return self.palavra_original

    @property
    def as_text(self) -> str:
        return \
            "Palavra={{id={0}, tags={1}, nivel={2}, tag_inicial={3}, palavra_original={4}, palavra_canonica={5}}}" \
            "".format(
                    str(self.id),
                    str(self.tags),
                    str(self.nivel),
                    str(self.tag_inicial),
                    str(self.palavra_original),
                    str(self.palavra_canonica)
            )