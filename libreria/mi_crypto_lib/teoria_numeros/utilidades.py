# Funciones matematicas compartidas

def mcd(a, b):
    """Maximo comun divisor (Euclides)."""
    while b:
        a, b = b, a % b
    return a


def es_primo(n):
    """Verifica si n es primo."""
    if n < 2:
        return False
    if n in (2, 3):
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def factorizar_entero(n):
    """Devuelve lista con los factores primos de n."""
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
    """Funcion indicatriz de Euler phi(n)."""
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
    """phi(n) para n = p*q (caso RSA)."""
    if not es_primo(p) or not es_primo(q):
        raise ValueError("Ambos valores deben ser primos")

    n = p * q
    resultado = (p - 1) * (q - 1)

    return {
        "n": n,
        "phi_n": resultado,
        "explicacion": "phi(" + str(n) + ") = (" + str(p) + "-1)(" + str(q) + "-1) = " + str(resultado),
    }
