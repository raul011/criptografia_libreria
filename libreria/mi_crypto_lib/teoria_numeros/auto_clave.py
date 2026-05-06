
ALFABETO = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"  # 27 letras


# ============================================================
#  UTILIDADES
# ============================================================

def limpiar_texto(texto):
    """Filtra solo letras del alfabeto español de 27 letras."""
    texto = texto.upper()
    resultado = ""
    for caracter in texto:
        if caracter in ALFABETO:
            resultado += caracter
    return resultado


def devolver_indice(letra):
    """Índice de una letra en el alfabeto español (0-26)."""
    for i in range(len(ALFABETO)):
        if ALFABETO[i] == letra:
            return i
    return -1


def devolver_letra(numero):
    """Letra en la posición numero % 27 del alfabeto español."""
    return ALFABETO[numero % 27]


# ============================================================
#  VIGENÈRE CLÁSICO
# ============================================================

def vigenere_clasico(texto, clave, modo="cifrar"):
    """Vigenère clásico con clave repetitiva."""
    texto_limpio = limpiar_texto(texto)
    clave_limpia = limpiar_texto(clave)
    clave_len    = len(clave_limpia)
    resultado    = ""

    for i, char in enumerate(texto_limpio):
        im = devolver_indice(char)
        ic = devolver_indice(clave_limpia[i % clave_len])
        c  = (im + ic) % 27 if modo == "cifrar" else (im - ic) % 27
        resultado += devolver_letra(c)

    return resultado


# ============================================================
#  AUTOCLAVE (VIGENÈRE DE CLAVE CONTINUA)
# ============================================================

def generar_autoclave(mensaje, clave):
    """
    Genera la clave extendida:
        clave_extendida = clave_inicial + mensaje_en_claro
    cortada al tamaño del mensaje.

    Ejemplo:
        mensaje = HOLAMUNDO  (9 letras)
        clave   = KEY        (3 letras)
        result  = KEYHOLAMU  (9 letras)
    """
    mensaje = limpiar_texto(mensaje)
    clave   = limpiar_texto(clave)
    return (clave + mensaje)[:len(mensaje)]


def cifrar_autoclave(mensaje, clave):
    """
    Cifrado Autoclave.
    La clave se extiende con el propio mensaje en claro,
    eliminando la periodicidad del Vigenère clásico.
    """
    mensaje_limpio  = limpiar_texto(mensaje)
    clave_extendida = generar_autoclave(mensaje_limpio, clave)
    resultado = ""

    for i in range(len(mensaje_limpio)):
        im = devolver_indice(mensaje_limpio[i])
        ic = devolver_indice(clave_extendida[i])
        resultado += devolver_letra((im + ic) % 27)

    return resultado


def descifrar_autoclave(mensaje_cifrado, clave):
    """
    Descifrado Autoclave.
    Reconstruye la clave letra a letra usando el texto ya descifrado.

    Posición i < len(clave)  → usa clave_inicial[i]
    Posición i >= len(clave) → usa resultado[i - len(clave)]
    """
    mensaje_cifrado = limpiar_texto(mensaje_cifrado)
    clave_inicial   = limpiar_texto(clave)
    len_clave       = len(clave_inicial)
    resultado       = ""

    for i in range(len(mensaje_cifrado)):
        ic = devolver_indice(clave_inicial[i]) if i < len_clave \
             else devolver_indice(resultado[i - len_clave])
        im = devolver_indice(mensaje_cifrado[i])
        resultado += devolver_letra((im - ic) % 27)

    return resultado


# ============================================================
#  MÉTODO KASISKI (con sistema de votos por divisores)
# ============================================================

def mcd(a, b):
    while b:
        a, b = b, a % b
    return a


def factores(n):
    """Todos los divisores de n mayores que 1."""
    return [i for i in range(2, n + 1) if n % i == 0]


def buscar_repeticiones(texto, tam_min=3, tam_max=5):
    """Busca secuencias repetidas de longitud entre tam_min y tam_max."""
    repeticiones = {}
    n = len(texto)
    for tam in range(tam_min, tam_max + 1):
        for i in range(n - tam):
            seq = texto[i:i + tam]
            if seq in repeticiones:
                continue
            posiciones = []
            inicio = 0
            while True:
                pos = texto.find(seq, inicio)
                if pos == -1:
                    break
                posiciones.append(pos)
                inicio = pos + 1
            if len(posiciones) >= 2:
                repeticiones[seq] = posiciones
    return repeticiones


def calcular_distancias(repeticiones):
    """Distancias entre ocurrencias consecutivas de cada secuencia."""
    distancias = []
    for posiciones in repeticiones.values():
        for i in range(1, len(posiciones)):
            distancias.append(posiciones[i] - posiciones[i - 1])
    return distancias


def contar_votos(distancias, max_longitud=20):
    """
    Por cada distancia saca sus divisores y le da un voto a cada uno.
    El divisor con más votos es la longitud más probable de la clave.
    Mucho más robusto que el MCD directo porque no se rompe si
    una sola distancia no es múltiplo exacto de la longitud.
    """
    votos = {}
    for d in distancias:
        for f in factores(d):
            if 2 <= f <= max_longitud:
                votos[f] = votos.get(f, 0) + 1
    return sorted(votos.items(), key=lambda x: x[1], reverse=True)


def kasiski(texto_cifrado, tam_min=3, tam_max=5, max_longitud=20):
    """
    Aplica Kasiski con sistema de votos por divisores.
    Devuelve repeticiones, distancias y candidatos ordenados por votos.
    """
    texto = limpiar_texto(texto_cifrado)
    reps  = buscar_repeticiones(texto, tam_min, tam_max)

    if not reps:
        return {"repeticiones": 0, "distancias": [], "candidatos": [], "mejor": None}

    distancias = calcular_distancias(reps)
    candidatos = contar_votos(distancias, max_longitud)
    mejor      = candidatos[0][0] if candidatos else None

    return {
        "repeticiones": len(reps),
        "secuencias"  : list(reps.keys())[:5],
        "distancias"  : distancias[:10],
        "candidatos"  : candidatos[:5],   # top 5: (longitud, votos)
        "mejor"       : mejor             # longitud con más votos
    }


# ============================================================
#  COMPARATIVA DE RESISTENCIA FRENTE A KASISKI
# ============================================================

def comparativa_kasiski(mensaje, clave):
    """
    Cifra el mismo mensaje con Vigenère Clásico y con Autoclave,
    luego aplica Kasiski a ambos y muestra los resultados.
    """
    sep = "=" * 62
    clave_len = len(limpiar_texto(clave))

    print(sep)
    print("  PUNTO 5: COMPARATIVA DE RESISTENCIA FRENTE A KASISKI")
    print(sep)
    print(f"  Mensaje : {limpiar_texto(mensaje)[:55]}...")
    print(f"  Clave   : {clave}  (longitud real = {clave_len})")
    print()

    # ── 1. Cifrar con ambos métodos ──────────────────────────
    cifrado_clasico   = vigenere_clasico(mensaje, clave, "cifrar")
    cifrado_autoclave = cifrar_autoclave(mensaje, clave)

    print(f"  Cifrado Clásico   : {cifrado_clasico[:55]}...")
    print(f"  Cifrado Autoclave : {cifrado_autoclave[:55]}...")
    print()

    # ── 2. Kasiski sobre Vigenère Clásico ───────────────────
    print("-" * 62)
    print("  KASISKI sobre VIGENÈRE CLÁSICO")
    print("-" * 62)
    res = kasiski(cifrado_clasico)

    print(f"  Repeticiones encontradas : {res['repeticiones']}")
    if res['repeticiones'] > 0:
        print(f"  Secuencias (muestra)     : {res['secuencias']}")
        print(f"  Distancias (muestra)     : {res['distancias']}")
        print(f"  Top candidatos (long,votos): {res['candidatos']}")
        print(f"  Longitud más probable    : {res['mejor']}")
        acierto = any(l == clave_len for l, _ in res['candidatos'])
        print(f"  ¿Longitud correcta?      : {'✓ SÍ' if acierto else '✗ NO'}")
        print(f"  → Kasiski FUNCIONA: puede estimar la longitud de la clave.")
    else:
        print("  → Sin repeticiones. Kasiski no puede actuar.")
    print()

    # ── 3. Kasiski sobre Autoclave ───────────────────────────
    print("-" * 62)
    print("  KASISKI sobre AUTOCLAVE (Clave Continua)")
    print("-" * 62)
    res2 = kasiski(cifrado_autoclave)

    print(f"  Repeticiones encontradas : {res2['repeticiones']}")
    if res2['repeticiones'] > 0:
        print(f"  Secuencias (muestra)     : {res2['secuencias']}")
        print(f"  Distancias (muestra)     : {res2['distancias']}")
        print(f"  Top candidatos (long,votos): {res2['candidatos']}")
        print(f"  Longitud más probable    : {res2['mejor']}")
        acierto = res2['mejor'] == clave_len
        print(f"  ¿Coincide con clave real?: {'(coincidencia casual)' if acierto else '✗ NO — es ruido estadístico'}")
        print(f"  → Kasiski encuentra repeticiones pero sin patrón real.")
    else:
        print(f"  → SIN repeticiones útiles.")
        print(f"  → Kasiski FALLA: no puede estimar la longitud de la clave.")
    print()

    # ── 4. Conclusión ────────────────────────────────────────
    print("=" * 62)
    print("  CONCLUSIÓN")
    print("=" * 62)
    print("""
  Vigenère Clásico:
    • La clave se REPITE cada N posiciones (N = longitud clave).
    • Esa periodicidad genera secuencias repetidas en el cifrado.
    • Kasiski detecta esas repeticiones, vota por divisores comunes
      y estima N → clave vulnerable.

  Autoclave (Clave Continua):
    • La clave se extiende con el propio mensaje en claro.
    • Cada letra se cifra con una clave DIFERENTE → sin periodo.
    • Sin periodicidad no hay secuencias repetidas predecibles.
    • Los votos se dispersan sin ganador claro → INEFICAZ.

  Resumen:
    Kasiski explota la PERIODICIDAD. Autoclave la elimina.
    Por eso el ataque por búsqueda de cadenas repetidas y
    cálculo del MCD se vuelve ineficaz contra Autoclave.
    """)
    print("=" * 62)


# ============================================================
#  DEMO COMPLETA
# ============================================================

if __name__ == "__main__":

    mensaje = (
         """Estaba en la biblioteca; mis pasos me llevaron entre largos pasillos. Los libros 
        despertaban mi interés por indagar en sus páginas. Aquel librito del campo, sembrado
        de unas flores silvestres en su portada, descendió entre mis brazos y lo cubrí con mi 
        abrigo de paño. Me dejé llevar y, sentada frente al portón, las campanas se oyeron 
        anunciar la hora del ángelus. Caí rendida en un profundo sueño; recuerdo las hojas 
        pasar. Me hablaron de cánticos populares, hombres y mujeres con sus ropajes empapados 
        de lluvia. Los niños corrían por el sembrado y el sol ligeramente se dejó ver."""
    )
    clave = "SECRETO"

    # --- Demo cifrado/descifrado autoclave ---
    print("=" * 62)
    print("  DEMO: CIFRADO AUTOCLAVE")
    print("=" * 62)
    msg_limpio      = limpiar_texto(mensaje)
    clave_extendida = generar_autoclave(msg_limpio, clave)
    cifrado         = cifrar_autoclave(msg_limpio, clave)
    descifrado      = descifrar_autoclave(cifrado, clave)

    print(f"  Mensaje original : {msg_limpio[:55]}...")
    print(f"  Clave inicial    : {clave}")
    print(f"  Clave extendida  : {clave_extendida[:55]}...")
    print(f"  Texto cifrado    : {cifrado[:55]}...")
    print(f"  Texto descifrado : {descifrado[:55]}...")
    print(f"  ¿Correcto?       : {'✓ SÍ' if msg_limpio == descifrado else '✗ NO'}")
    print()

    # --- Comparativa frente a Kasiski ---
    comparativa_kasiski(mensaje, clave)
