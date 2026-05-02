"""
Funcion indicatriz de Euler phi(n)
Calcula la cantidad de enteros positivos menores que n
que son coprimos con n.
"""

def es_primo(n):
    """Verifica si un número es primo."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

def factorizar_entero(n):
    """Factoriza un número entero en sus primos."""
    factores = []
    divisor = 2
    temp = n
    while divisor * divisor <= temp:
        while temp % divisor == 0:
            factores.append(divisor)
            temp //= divisor
        divisor += 1
    if temp > 1:
        factores.append(temp)
    return factores

def phi(n):
    """
    Calcula phi(n) usando la formula:
        phi(n) = n * prod(1 - 1/p) para cada primo p que divide a n
    """
    if n <= 0:
        return 0
    if n == 1:
        return 1

    if es_primo(n):
        return n - 1

    factores = factorizar_entero(n)
    primos_unicos = list(set(factores))

    resultado = n
    for p in primos_unicos:
        resultado = resultado * (p - 1) // p

    return resultado

def phi_dos_primos(p, q):
    """
    Calcula phi(n) cuando n = p * q (caso RSA).
        phi(n) = (p - 1) * (q - 1)
    """
    if not es_primo(p) or not es_primo(q):
        raise ValueError("Ambos valores deben ser primos")

    n = p * q
    resultado = (p - 1) * (q - 1)

    return {
        "n": n,
        "phi_n": resultado,
        "explicacion": "phi(" + str(n) + ") = (" + str(p) + "-1)(" + str(q) + "-1) = " + str(resultado),
        "aplicacion": "Esta formula es fundamental en RSA"
    }