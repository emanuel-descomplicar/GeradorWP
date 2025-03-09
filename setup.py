"""
Configuração do pacote GeradorWP.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

from setuptools import setup, find_packages
from pathlib import Path

# Ler README.md
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="geradorwp",
    version="1.1.0",
    description="Gerador de conteúdo para WordPress",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Descomplicar",
    author_email="info@descomplicar.pt",
    url="https://descomplicar.pt",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests>=2.31.0",
        "python-wordpress-xmlrpc>=2.3",
        "Pillow>=10.0.0",
        "python-dotenv>=1.0.0",
        "beautifulsoup4>=4.12.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "black>=23.7.0",
            "isort>=5.12.0",
            "flake8>=6.1.0",
            "mypy>=1.5.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "geradorwp=src.main:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Text Processing :: Markup :: HTML",
    ],
) 