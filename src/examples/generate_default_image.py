#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Gerador de imagem padrão.

Este script gera uma imagem padrão que será usada como fallback
quando não houver uma imagem específica para a categoria.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
from src.utils.image_generator import ImageGenerator
from dotenv import load_dotenv

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Função principal."""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Inicializar gerador de imagens
    generator = ImageGenerator()
    
    # Criar diretório de imagens se não existir
    os.makedirs("assets/images", exist_ok=True)
    
    # Gerar imagem padrão
    logger.info("Gerando imagem padrão...")
    
    output_path = generator.generate_image(
        title="Descomplicar Blog",
        category="default",
        category_name="Blog",
        output_path="assets/images/default.jpg"
    )
    
    if output_path:
        logger.info(f"✓ Imagem padrão gerada com sucesso: {output_path}")
    else:
        logger.error("✗ Falha ao gerar imagem padrão")

if __name__ == "__main__":
    main() 