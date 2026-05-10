from setuptools import setup, find_packages
from pathlib import Path

# Leer README.md relativo a este archivo
aqui = Path(__file__).parent
long_description = (aqui / "README.md").read_text(encoding="utf-8")

setup(
    name="mi_crypto_lib",
    version="1.0.10",
    author="Raúl",
    description="Biblioteca de criptografía: teoría de números, cifrados clásicos y ataques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    python_requires=">=3.8",
)
