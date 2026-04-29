"""
crr.py — Conjunto Reducido de Residuos (CRR)
=============================================

El Conjunto Reducido de Residuos módulo n es el conjunto de todos
los enteros en [1, n) que son coprimos con n.

Propiedades clave:
    - |CRR(n)| = φ(n)
    - Para todo a ∈ CRR(n): mcd(a, n) = 1
    - Todo elemento de CRR(n) tiene inverso multiplicativo módulo n
"""

from math import gcd


def crr(n):
    """
    Calcula el Conjunto Reducido de Residuos módulo n.

    Retorna la lista de enteros en {1, 2, ..., n-1} que son
    coprimos con n (es decir, mcd(a, n) = 1).

    Parámetros
    ----------
    n : int
        Módulo (entero positivo ≥ 2).

    Retorna
    -------
    list[int]
        Lista ordenada de enteros coprimos con n en [1, n).

    Ejemplo
    -------
    >>> crr(10)
    [1, 3, 7, 9]
    >>> crr(12)
    [1, 5, 7, 11]
    >>> len(crr(10))  # Debe ser φ(10) = 4
    4
    """
    if n < 2:
        raise ValueError("n debe ser un entero ≥ 2")

    return [a for a in range(1, n) if gcd(a, n) == 1]


def es_generador(g, n):
    """
    Verifica si g es un generador del grupo multiplicativo (Z/nZ)*.

    Un elemento g genera el grupo si las potencias sucesivas de g
    módulo n producen todos los elementos del CRR(n).

    Parámetros
    ----------
    g : int
        Candidato a generador.
    n : int
        Módulo.

    Retorna
    -------
    bool
        True si g genera todo el grupo (Z/nZ)*.

    Ejemplo
    -------
    >>> es_generador(3, 7)
    True
    >>> es_generador(2, 7)
    False
    """
    conjunto = crr(n)
    generados = set()
    potencia = 1
    for _ in range(len(conjunto)):
        potencia = (potencia * g) % n
        generados.add(potencia)

    return generados == set(conjunto)


def encontrar_generadores(n):
    """
    Encuentra todos los generadores del grupo (Z/nZ)* si existen.

    No todos los grupos tienen generadores (solo los cíclicos).

    Retorna
    -------
    list[int]
        Lista de generadores, puede estar vacía.

    Ejemplo
    -------
    >>> encontrar_generadores(7)
    [3, 5]
    """
    return [g for g in crr(n) if es_generador(g, n)]
