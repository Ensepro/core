"""
@project ensepro
@since 04/01/2018
@author Alencar Rodrigo Hentges <alencarhentges@gmail.com>

"""

from ensepro import sinonimos
from ensepro.sinonimos.sinonimo import Sinonimo
sinonimos_retornados = sinonimos.get_sinonimos("andar", "por")
print(sinonimos_retornados, end='\n\n')

print("teste1:  ", end='')

teste1 = sinonimos_retornados[0]
sinonimo = Sinonimo.from_string(teste1)
print(sinonimo)
