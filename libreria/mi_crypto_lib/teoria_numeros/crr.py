

def mcd(a, b):
    """Calcula el máximo común divisor usando el algoritmo de Euclides."""
    while b:
        a, b = b, a % b
    return a


def crr(n):
    if n < 2:
        raise ValueError("n debe ser un entero ≥ 2")

    return [a for a in range(1, n) if mcd(a, n) == 1]


def verificar_crr_phi(n):
    # Importación local para evitar posibles ciclos de importación
    from .phi import phi
    
    elementos_crr = crr(n)
    valor_phi = phi(n)
    
    coincide = len(elementos_crr) == valor_phi
    
    print(f"Módulo n = {n}")
    print(f"Elementos del CRR(n): {elementos_crr}")
    print(f"Cantidad de elementos (len): {len(elementos_crr)}")
    print(f"Valor teórico de phi(n): {valor_phi}")
    print(f"¿Coinciden? {'Si' if coincide else 'No'}")
    
    return coincide
