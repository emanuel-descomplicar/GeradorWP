"""
Setup file for GeradorWP project.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="gerador-wp",
    version="0.1.0",
    author="Descomplicar - Agência de Aceleração Digital",
    author_email="info@descomplicar.pt",
    description="Gerador de conteúdo para WordPress usando CrewAI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://descomplicar.pt",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "gerador-wp=src.main:main",
        ],
    },
) 