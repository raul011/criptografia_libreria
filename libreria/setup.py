from setuptools import setup, find_packages
from pathlib import Path

# Leer README.md relativo a este archivo
aqui = Path(__file__).parent
long_description = (aqui / "README.md").read_text(encoding="utf-8")

setup(
    name="mi_crypto_lib",
    version="1.0.1",
    author="Raúl",
    description="Biblioteca de criptografía: teoría de números, cifrados clásicos y ataques",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raul/mi_crypto_lib",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security :: Cryptography",
        "Intended Audience :: Education",
    ],
)
