# mi_crypto_lib 🔐

Biblioteca educativa de criptografía desarrollada en Python puro (sin dependencias externas).

## Estructura

```
mi_crypto_lib/
├── teoria_numeros/          # Herramientas de teoría de números
│   ├── phi.py               # Función indicatriz de Euler φ(n)
│   ├── crr.py               # Conjunto Reducido de Residuos
│   └── inversos.py          # Inversos multiplicativos (Euler, Euclides extendido)
│
├── cifrados_clasicos/       # Cifrados clásicos
│   ├── vigenere_autoclave.py  # Vigenère Autoclave (texto plano / criptograma)
│   └── hill.py                # Cifrado Hill (matricial)
│
├── ataques/                 # Criptoanálisis
│   └── gauss_jordan.py      # Ataque al cifrado Hill con Gauss-Jordan
│
├── ejemplos/                # Demostraciones
│   └── rsa_demo.py          # Demo completa de RSA con n = p·q
│
├── setup.py
├── README.md
└── LICENSE
```

## Instalación

```bash
# Desde el directorio raíz del proyecto:
pip install -e .
```

## Uso rápido

### Teoría de números

```python
from mi_crypto_lib.teoria_numeros import phi, crr, inverso_euler

# Función φ de Euler
print(phi(36))        # 12

# Conjunto Reducido de Residuos
print(crr(10))        # [1, 3, 7, 9]

# Inverso multiplicativo
print(inverso_euler(3, 26))  # 9  →  3 × 9 ≡ 1 (mod 26)
```



## Requisitos

- Python ≥ 3.8
- Sin dependencias externas (solo librería estándar)

## Licencia

MIT License — ver [LICENSE](LICENSE)
