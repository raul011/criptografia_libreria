
class Matriz:
    filas = 0
    columnas = 0
    datos = None
    
    def __init__(self, filas, columnas): 
        self.filas = filas
        self.columnas = columnas
        self.datos = []
        i = 0
        while i < self.filas:
            fila_temp = []
            j = 0
            while j < self.columnas:
                fila_temp.append(0)
                j += 1
            self.datos.append(fila_temp)
            i += 1

    def obtener(self, fila, columna):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            raise IndexError("Error: índice fuera de rango")
        return self.datos[fila][columna]

    def establecer(self, fila, columna, valor):
        if fila < 0 or fila >= self.filas or columna < 0 or columna >= self.columnas:
            raise IndexError("Error: índice fuera de rango")
        self.datos[fila][columna] = valor

    # ---------------------------------------------------------
    # MÉTODOS AUXILIARES (Privados, para cálculo de determinante)
    def _menor(self, fila_exc, col_exc):
        n = self.filas
        m = Matriz(n-1, n-1)
        mi, mj = 0, 0
        i = 0
        while i < n:
            if i == fila_exc:
                i += 1
                continue
            mj = 0
            j = 0
            while j < n:
                if j == col_exc:
                    j += 1
                    continue
                m.establecer(mi, mj, self.datos[i][j])
                mj += 1
                j += 1
            mi += 1
            i += 1
        return m

    def _determinante(self):
        n = self.filas
        if n == 1: return self.obtener(0, 0)
        if n == 2: return self.obtener(0,0)*self.obtener(1,1) - self.obtener(0,1)*self.obtener(1,0)
        
        det = 0
        c = 0
        while c < n:
            menor = self._menor(0, c)
            signo = 1 if (c % 2 == 0) else -1
            det += signo * self.obtener(0, c) * menor._determinante()
            c += 1
        return det

    def mostrar(self):
        print(self.to_string())
        print("")

    def to_string(self):
        lineas = []
        i = 0
        while i < self.filas:
            linea = "["
            j = 0
            while j < self.columnas:
                valor = self.datos[i][j]
                if valor >= 0:
                    linea += " " + str(valor)
                else:
                    linea += str(valor)
                if j < self.columnas - 1:
                    linea += "  "
                j += 1
            linea += "]"
            lineas.append(linea)
            i += 1
        return "\n".join(lineas)

    # ---------------------------------------------------------
    # GAUSS-JORDAN MODULAR (Inversa en Z_m, solo enteros)
    def inversa_modular_gauss_jordan(self, modulo):
        if self.filas != self.columnas:
            raise ValueError("Error: Solo matrices cuadradas tienen inversa modular.")
        
        n = self.filas
        # 1. Matriz aumentada [A | I]
        aumentada = []
        i = 0
        while i < n:
            fila = []
            j = 0
            while j < n:
                fila.append(self.datos[i][j] % modulo)
                j += 1
            j = 0
            while j < n:
                if i == j: fila.append(1)
                else: fila.append(0)
                j += 1
            aumentada.append(fila)
            i += 1

        # 2. Eliminación Gauss-Jordan modular
        i = 0
        while i < n:
            # 🔍 Buscar pivote: debe ser != 0 Y NO múltiplo de 3 (invertible en Z_27)
            pivote_fila = -1
            k = i
            while k < n:
                val = aumentada[k][i] % modulo
                if val != 0 and val % 3 != 0:
                    pivote_fila = k
                    break
                k += 1
            
            if pivote_fila == -1:
                raise ValueError("Matriz no invertible módulo " + str(modulo))
            
            # Intercambiar filas
            if pivote_fila != i:
                temp = aumentada[i]
                aumentada[i] = aumentada[pivote_fila]
                aumentada[pivote_fila] = temp
            
            # Normalizar pivote a 1 (inverso modular)
            pivote_val = aumentada[i][i]
            inv_pivote = None
            x = 1
            while x < modulo:
                if (pivote_val * x) % modulo == 1:
                    inv_pivote = x
                    break
                x += 1
            if inv_pivote is None:
                raise ValueError("Pivote sin inverso modular.")
            
            j = 0
            while j < 2 * n:
                aumentada[i][j] = (aumentada[i][j] * inv_pivote) % modulo
                j += 1
            
            # Ceros en el resto de la columna
            k = 0
            while k < n:
                if k != i:
                    factor = aumentada[k][i]
                    j = 0
                    while j < 2 * n:
                        aumentada[k][j] = (aumentada[k][j] - factor * aumentada[i][j]) % modulo
                        j += 1
                k += 1
            i += 1

        # 3. Extraer P⁻¹ (mitad derecha)
        inv = Matriz(n, n)
        i = 0
        while i < n:
            j = 0
            while j < n:
                inv.establecer(i, j, aumentada[i][n + j])
                j += 1
            i += 1
        return inv

    def multiplicar(self, otra):
        if self.columnas != otra.filas:
            raise ValueError("Dimensiones incompatibles para producto")
        resultado = Matriz(self.filas, otra.columnas)
        i = 0
        while i < self.filas:
            j = 0
            while j < otra.columnas:
                suma = 0
                k = 0
                while k < self.columnas:
                    suma += self.datos[i][k] * otra.datos[k][j]
                    k += 1
                resultado.establecer(i, j, suma)
                j += 1
            i += 1
        return resultado


# =====================================================================
class CifradoMatriz:
    ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
    MOD = len(ALF)  # 27

    def __init__(self, palabra, mclave):
        if not isinstance(mclave, Matriz):
            raise TypeError("mclave debe ser instancia de Matriz.")
        if mclave.filas != mclave.columnas:
            raise ValueError("mclave debe ser cuadrada.")
        self.ptxt = palabra.upper()
        self.mclave = mclave
        self.n = self.mclave.filas
        # La inversa se calcula con Gauss-Jordan modular
        self.mclave_inv = self.mclave.inversa_modular_gauss_jordan(self.MOD)

    def _txt_nums(self, txt):
        nums = []
        for c in txt:
            if c == ' ': nums.append(26)
            elif c in self.ALF: nums.append(self.ALF.index(c))
        return nums

    def _nums_txt(self, nums):
        return "".join(self.ALF[n % self.MOD] for n in nums)

    def cifrar(self):
        nums = self._txt_nums(self.ptxt)
        while len(nums) % self.n != 0: nums.append(26)
        cnums = []
        i = 0
        while i < len(nums):
            vec = Matriz(self.n, 1)
            r = 0
            while r < self.n:
                vec.establecer(r, 0, nums[i+r])
                r += 1
            res = self.mclave.multiplicar(vec)
            r = 0
            while r < self.n:
                cnums.append(res.obtener(r, 0) % self.MOD)
                r += 1
            i += self.n
        return self._nums_txt(cnums)

    def descifrar(self, tcif):
        nums = self._txt_nums(tcif)
        if len(nums) % self.n != 0:
            raise ValueError("Longitud no múltiplo de n.")
        dnums = []
        i = 0
        while i < len(nums):
            vec = Matriz(self.n, 1)
            r = 0
            while r < self.n:
                vec.establecer(r, 0, nums[i+r])
                r += 1
            res = self.mclave_inv.multiplicar(vec)
            r = 0
            while r < self.n:
                dnums.append(res.obtener(r, 0) % self.MOD)
                r += 1
            i += self.n
        return self._nums_txt(dnums).rstrip('_')

    # ---------------------------------------------------------
    # ATAQUE AUTOMATIZADO: Texto plano conocido
    @staticmethod
    def recuperar_clave(texto_plano, texto_cifrado, n, modulo=27):
        ALF = "ABCDEFGHIJKLMNOPQRSTUVWXYZ_"
        def txt_a_nums(t):
            nums = []
            for c in t.upper():
                if c == ' ': nums.append(26)
                elif c in ALF: nums.append(ALF.index(c))
            return nums

        nums_p = txt_a_nums(texto_plano)
        nums_c = txt_a_nums(texto_cifrado)
        max_len = min(len(nums_p), len(nums_c))

        # Buscar n bloques consecutivos ALINEADOS que formen una P invertible
        offset = 0
        while offset + n*n <= max_len:
            # Extraer n bloques completos (cada uno de n caracteres)
            bloque_p = []
            bloque_c = []
            b = 0
            while b < n:
                inicio = offset + (b * n)
                fin = inicio + n
                i = inicio
                while i < fin:
                    bloque_p.append(nums_p[i])
                    bloque_c.append(nums_c[i])
                    i += 1
                b += 1

            # Construir matrices P y C (cada columna = un bloque)
            P = Matriz(n, n)
            C = Matriz(n, n)
            idx = 0
            col = 0
            while col < n:
                fila = 0
                while fila < n:
                    P.establecer(fila, col, bloque_p[idx])
                    C.establecer(fila, col, bloque_c[idx])
                    idx += 1
                    fila += 1
                col += 1

            # Intentar diagonalizar P con Gauss-Jordan modular
            try:
                P_inv = P.inversa_modular_gauss_jordan(modulo)
                
                # K = C × P⁻¹ (mod m)
                K_temp = C.multiplicar(P_inv)
                K = Matriz(n, n)
                i = 0
                while i < n:
                    j = 0
                    while j < n:
                        K.establecer(i, j, K_temp.obtener(i, j) % modulo)
                        j += 1
                    i += 1
                    
                bloques_txt = texto_plano[offset:offset+n*n]
                print(f"  -> Bloques alineados encontrados desde offset {offset}: '{bloques_txt}'")
                return K
                
            except ValueError:
                # Avanzar al siguiente conjunto de bloques
                offset += n

        raise ValueError("No se encontraron n bloques alineados invertibles módulo 27. Usa un mensaje más largo.")


# =====================================================================
if __name__ == "__main__":

    # 1. ingresar matriz llave
    print("=== Cifrado Hill 3x3 ===")  
    n = 3
    clave = Matriz(3, 3)

    # === OPCIÓN 1 (Determinante = 1) ===
    clave.establecer(0, 0, 1)
    clave.establecer(0, 1, 2)
    clave.establecer(0, 2, 3)
    clave.establecer(1, 0, 0)
    clave.establecer(1, 1, 1)
    clave.establecer(1, 2, 4)
    clave.establecer(2, 0, 5)
    clave.establecer(2, 1, 6)
    clave.establecer(2, 2, 0)

    # === OPCIÓN 2 (Determinante mod 27 = 14) ===
    # clave.establecer(0, 0, 4)
    # clave.establecer(0, 1, 1)
    # clave.establecer(0, 2, 2)
    # clave.establecer(1, 0, 2)
    # clave.establecer(1, 1, 5)
    # clave.establecer(1, 2, 3)
    # clave.establecer(2, 0, 1)
    # clave.establecer(2, 1, 3)
    # clave.establecer(2, 2, 7)

    # === OPCIÓN 3 (Determinante mod 27 = 10) ===
    # clave.establecer(0, 0, 5)
    # clave.establecer(0, 1, 0)
    # clave.establecer(0, 2, 2)
    # clave.establecer(1, 0, 1)
    # clave.establecer(1, 1, 4)
    # clave.establecer(1, 2, 3)
    # clave.establecer(2, 0, 2)
    # clave.establecer(2, 1, 1)
    # clave.establecer(2, 2, 6)

    # === OPCIÓN 4 (Determinante mod 27 = 10) ===
    # clave.establecer(0, 0, 2)
    # clave.establecer(0, 1, 4)
    # clave.establecer(0, 2, 1)
    # clave.establecer(1, 0, 3)
    # clave.establecer(1, 1, 1)
    # clave.establecer(1, 2, 5)
    # clave.establecer(2, 0, 0)
    # clave.establecer(2, 1, 2)
    # clave.establecer(2, 2, 3)

    # === OPCIÓN 5 (Determinante mod 27 = 13) ===
    # clave.establecer(0, 0, 3)
    # clave.establecer(0, 1, 1)
    # clave.establecer(0, 2, 4)
    # clave.establecer(1, 0, 2)
    # clave.establecer(1, 1, 6)
    # clave.establecer(1, 2, 1)
    # clave.establecer(2, 0, 1)
    # clave.establecer(2, 1, 2)
    # clave.establecer(2, 2, 5)

    # === OPCIÓN 6 (Determinante mod 27 = 5) ===
    # clave.establecer(0, 0, 4)
    # clave.establecer(0, 1, 1)
    # clave.establecer(0, 2, 2)
    # clave.establecer(1, 0, 2)
    # clave.establecer(1, 1, 5)
    # clave.establecer(1, 2, 3)
    # clave.establecer(2, 0, 1)
    # clave.establecer(2, 1, 3)
    # clave.establecer(2, 2, 8)

    # === OPCIÓN 7 (Determinante mod 27 = 5) ===
    # clave.establecer(0, 0, 5)
    # clave.establecer(0, 1, 2)
    # clave.establecer(0, 2, 1)
    # clave.establecer(1, 0, 3)
    # clave.establecer(1, 1, 4)
    # clave.establecer(1, 2, 6)
    # clave.establecer(2, 0, 2)
    # clave.establecer(2, 1, 1)
    # clave.establecer(2, 2, 5)

    # === OPCIÓN 8 (Determinante mod 27 = 10) ===
    # clave.establecer(0, 0, 8)
    # clave.establecer(0, 1, 3)
    # clave.establecer(0, 2, 1)
    # clave.establecer(1, 0, 2)
    # clave.establecer(1, 1, 7)
    # clave.establecer(1, 2, 4)
    # clave.establecer(2, 0, 5)
    # clave.establecer(2, 1, 2)
    # clave.establecer(2, 2, 9)

    # === OPCIÓN 9 (Determinante mod 27 = 26) ===
    # clave.establecer(0, 0, 9)
    # clave.establecer(0, 1, 1)
    # clave.establecer(0, 2, 3)
    # clave.establecer(1, 0, 4)
    # clave.establecer(1, 1, 7)
    # clave.establecer(1, 2, 2)
    # clave.establecer(2, 0, 2)
    # clave.establecer(2, 1, 5)
    # clave.establecer(2, 2, 8)

    # === OPCIÓN 10 (Determinante mod 27 = 16) ===
    # clave.establecer(0, 0, 2)
    # clave.establecer(0, 1, 7)
    # clave.establecer(0, 2, 5)
    # clave.establecer(1, 0, 6)
    # clave.establecer(1, 1, 3)
    # clave.establecer(1, 2, 8)
    # clave.establecer(2, 0, 4)
    # clave.establecer(2, 1, 1)
    # clave.establecer(2, 2, 9)

    print(f"Clave manual ({n}x{n}):")
    clave.mostrar()
    
    # 2. cifrar y descifrar mensaje
    mensaje = "LA CRIPTOGRAFIA MODERNA"
    hill = CifradoMatriz(mensaje, clave)
    cifrado = hill.cifrar()
    descifrado = hill.descifrar(cifrado)
    
    print(f"Mensaje:    {mensaje}")
    print(f"Cifrado:    {cifrado}")
    print(f"Descifrado: {descifrado}")
    print("Correcto?", mensaje.replace(" ", "_") == descifrado)
    
    # 3. ataque de texto conocido
    print("\n=== Criptoanalisis (Ataque de texto conocido) ===")
    clave_recuperada = CifradoMatriz.recuperar_clave(mensaje, cifrado, n)
    print("Clave recuperada por ataque:")
    clave_recuperada.mostrar()