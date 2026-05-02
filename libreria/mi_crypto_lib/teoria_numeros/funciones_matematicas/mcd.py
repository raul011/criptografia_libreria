def mcd(a, b):
    """Calcula el máximo común divisor usando el algoritmo de Euclides."""
    while b:
        a, b = b, a % b
    return a
