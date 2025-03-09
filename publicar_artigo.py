#!/usr/bin/env python3
"""
Script de Entrada: Publicação de Artigos no WordPress

Este é um script de entrada (wrapper) que invoca o módulo principal de publicação
localizado em src/publicar_artigo.py. Esta separação permite manter a lógica principal
na pasta src/ enquanto oferece um ponto de entrada simples na raiz do projeto.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import importlib.util
from pathlib import Path

def main():
    """
    Função principal que carrega e executa o módulo de publicação de artigos.
    Esta função é apenas um wrapper que invoca o script real em src/publicar_artigo.py
    """
    print("GeradorWP - Sistema de Publicação de Artigos")
    print("Descomplicar - Agência de Aceleração Digital")
    print("https://descomplicar.pt")
    print("-" * 50)
    
    # Obter caminho do script em src/
    script_path = Path(__file__).parent / "src" / "publicar_artigo.py"
    
    if not script_path.exists():
        print(f"ERRO: O módulo principal {script_path} não foi encontrado!")
        print("Este script é apenas um wrapper e requer o módulo principal.")
        return 1
    
    # Executar o script usando importlib
    try:
        # Configurar o path para incluir a pasta src/
        sys.path.insert(0, str(Path(__file__).parent))
        
        # Carregar o módulo
        spec = importlib.util.spec_from_file_location("publicar_artigo", script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Se chegarmos aqui, significa que o script foi executado com sucesso
        return 0
    except Exception as e:
        print(f"Erro ao executar o módulo principal: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 