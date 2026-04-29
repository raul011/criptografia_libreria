"""
Ejercicio Práctico: Cálculo de phi(n) usando primos seguros
===========================================================
"""

def es_primo(n):
    """Verifica si un número n es primo."""
    if n < 2: return False
    if n in (2, 3): return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generar_primo_seguro(inicio):
    """
    Busca un primo seguro a partir de 'inicio'.
    Un primo p es seguro si (p-1)/2 también es primo.
    """
    p = inicio
    while True:
        if es_primo(p):
            q_sg = (p - 1) // 2
            if es_primo(q_sg):
                return p
        p += 1

def ejercicio_primos_seguros():
    print("=" * 60)
    print(" CÁLCULO DE phi(n) USANDO PRIMOS SEGUROS")
    print("=" * 60)
    
    # 1. Generar dos primos seguros
    p = generar_primo_seguro(10)
    q = generar_primo_seguro(30)
    
    print(f"Primer primo seguro (p) = {p}")
    print(f"Segundo primo seguro (q) = {q}")
    
    # 2. Calcular n = p * q
    n = p * q
    print(f"\nMódulo n = p * q = {p} * {q} = {n}")
    
    # 3. Calcular phi(n)
    phi_n = (p - 1) * (q - 1)
    print(f"\nCálculo de phi(n) = (p - 1) * (q - 1)")
    print(f"phi({n}) = ({p} - 1) * ({q} - 1) = {p-1} * {q-1} = {phi_n}")
    print("=" * 60)

if __name__ == '__main__':
    ejercicio_primos_seguros()
