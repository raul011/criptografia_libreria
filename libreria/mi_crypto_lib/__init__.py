"""
mi_crypto_lib — Biblioteca de criptografía educativa
=====================================================

Módulos disponibles:
    - teoria_numeros : Función φ de Euler, CRR, inversos multiplicativos

"""

__version__ = "1.0.5"
__author__ = "Raúl"

# Exponemos las funciones principales
from .teoria_numeros import crr as calcular_crr, phi, inverso_euler, inverso_extendido
from .teoria_numeros.ejercicio_rsa_base import generar_primo_seguro
from .teoria_numeros.ataque_hill import Matriz, CifradoMatriz
from .teoria_numeros.n_generico import factorizar, euler_phi
