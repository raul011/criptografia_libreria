from .utilidades import mcd


def factorizar(n: int) -> dict:
    factores = {}
    temp = n
    
    # Extraer factores 2
    exponente = 0
    while temp % 2 == 0:
        exponente += 1
        temp //= 2
    if exponente > 0:
        factores[2] = exponente
    
    # Buscar factores impares
    p = 3
    while p * p <= temp:
        if temp % p == 0:
            exponente = 0
            while temp % p == 0:
                exponente += 1
                temp //= p
            factores[p] = exponente
        p += 2
    
    if temp > 1:
        factores[temp] = 1
    
    return factores


def euler_phi(n: int) -> int:
    if n <= 0:
        raise ValueError("n debe ser un entero positivo")
    if n == 1:
        return 1
    
    factores = factorizar(n)
    phi = n
    for p in factores.keys():
        phi = phi // p * (p - 1)
    return phi

def main():
    while True:
        try:
            entrada = input("\nIngrese un entero n (o 'salir' para terminar): ").strip()
            if entrada.lower() in ('salir', 'exit', 'q'):
                print("¡Hasta luego!")
                break
            n = int(entrada)
            if n <= 0:
                print("Por favor, ingrese un número entero positivo.")
                continue
            
            # Factorización
            factores = factorizar(n)
            if factores:
                print(f"\nFactorización de {n}: " + " × ".join([f"{p}^{e}" for p, e in factores.items()]))
            else:
                print(f"\n{n} es 1 (no tiene factores primos)")
            
            # Cálculo de φ(n)
            phi = euler_phi(n)
            print(f"φ({n}) = {phi}")
            
        except ValueError:
            print("Entrada inválida. Ingrese un número entero o 'salir'.")

if __name__ == "__main__":
    main()