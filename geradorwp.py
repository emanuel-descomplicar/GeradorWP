#!/usr/bin/env python3
"""
GeradorWP - Script de Entrada Principal

Este script é um ponto de entrada simplificado para o GeradorWP,
invocando o módulo principal em src/main.py.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
from pathlib import Path

# Adicionar diretório pai ao sys.path para permitir importações
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """
    Função principal que importa e executa o módulo principal.
    """
    try:
        print("GeradorWP - Sistema de Geração de Conteúdo WordPress")
        print("Descomplicar - Agência de Aceleração Digital")
        print("https://descomplicar.pt")
        print("-" * 60)
        
        # Importar o módulo main do src e executar
        from src.main import main as src_main
        sys.exit(src_main())
    except ImportError as e:
        print(f"Erro ao importar módulo principal: {str(e)}")
        print("Verifique se a estrutura do projeto está intacta.")
        return 1
    except Exception as e:
        print(f"Erro ao executar GeradorWP: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 