"""
teoria_numeros — Herramientas de teoría de números para criptografía
====================================================================

Funciones principales:
    - phi(n)                : Función indicatriz de Euler φ(n)
    - crr(n)                : Conjunto Reducido de Residuos módulo n
    - inverso_euler(a, n)   : Inverso multiplicativo usando el teorema de Euler
    - inverso_extendido(a, n) : Inverso multiplicativo usando Euclides extendido
"""

from .phi import phi, factorizar
from .crr import crr
from .inversos import inverso_euler, inverso_extendido, mcd
