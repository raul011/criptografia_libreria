"""
mi_crypto_lib - Biblioteca de criptografia
"""

__version__ = "1.0.10"
__author__ = "Raúl"

# CRR y phi
from .teoria_numeros import crr as calcular_crr, phi
# RSA
from .teoria_numeros import generar_primo_seguro
# Factorizacion generica
from .teoria_numeros import factorizar, euler_phi
# Inversos
from .teoria_numeros import inverso_euler, inverso_extendido
# Autoclave
from .cifrados_clasicos import cifrar_autoclave, descifrar_autoclave, kasiski
# Hill
from .cifrados_clasicos import Matriz, CifradoMatriz
