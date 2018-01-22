"""
@project ensepro
@since 18/12/2017
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro.arvore.arvore import Arvore
from ensepro.classes.palavra import Palavra
import os

scriptDirectory = os.path.dirname(os.path.realpath(__file__))
print(scriptDirectory)
dados_palavra = {
    "tags": ["tag1", "tag2", "tag3"],
    "nivel": "2",
    "tag_inicial": "DN:adj",
    "palavra_original": "estar",
    "palavra_canonica": "estar"

}

palavra = Palavra(id=123, dados_palavra=dados_palavra)
arvore = Arvore()
arvore.adicionar_node("a", "aa")
arvore.adicionar_node("z", "zz")
arvore.adicionar_node("b", "bb", "a")
arvore.adicionar_node("c", "cc", "a")
arvore.adicionar_node("d", "(dd)", "c")
arvore.adicionar_node("f", "((ff", "b")
arvore.adicionar_node("g", "gg", "a")
arvore.adicionar_node("h", "hh", "c")
arvore.adicionar_node("teste", palavra, "z")

print([str(node.valor) for node in arvore.roots])
print(palavra.as_text)
arvore.to_nltk_tree().pretty_print()
