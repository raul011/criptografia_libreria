# mi_crypto_lib

Biblioteca de criptografía en Python puro para el proyecto 1 de la materia.

## Estructura

```
mi_crypto_lib/
├── __init__.py
├── teoria_numeros/
│   ├── utilidades.py            # mcd, es_primo, phi
│   ├── crr.py                   # Conjunto Reducido de Residuos
│   ├── ejercicio_rsa_base.py    # Primos seguros (RSA)
│   ├── n_generico.py            # Factorizacion y phi(n) generico
│   └── inversos.py              # Inversos multiplicativos
└── cifrados_clasicos/
    ├── auto_clave.py            # Cifrado Autoclave + Kasiski
    └── ataque_hill.py           # Cifrado Hill + ataque Gauss-Jordan
```

## Instalacion

```bash
pip install -e .
```

## Uso

```python
import mi_crypto_lib as cripto

cripto.calcular_crr(10)              # [1, 3, 7, 9]
cripto.phi(10)                       # 4
cripto.generar_primo_seguro(10)      # 11
cripto.factorizar(60)                # {2: 2, 3: 1, 5: 1}
cripto.euler_phi(60)                 # 16
cripto.inverso_euler(3, 26)          # {'inverso': 9, ...}
cripto.inverso_extendido(3, 26)      # {'inverso': 9, ...}
cripto.cifrar_autoclave("HOLA", "KEY")
cripto.descifrar_autoclave("...", "KEY")
cripto.kasiski("...")
cripto.CifradoMatriz.recuperar_clave("TEXTO", "CIFRA", 2)
```

## Requisitos

- Python >= 3.8
- Sin dependencias externas
