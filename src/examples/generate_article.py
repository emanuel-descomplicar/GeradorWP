#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de exemplo para geração de artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import logging
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Adicionar diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.generators.content_generator import ContentGenerator
from src.integrations.dify_client import DifyClient
from src.integrations.wordpress_client import WordPressClient

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.getenv('LOG_FILE', 'gerador-wp.log'))
    ]
)

# Logger para este módulo
logger = logging.getLogger(__name__)

# Categorias disponíveis
CATEGORIES = [
    'blog-e-commerce',
    'blog-empreendedorismo',
    'blog-gestao-pmes',
    'blog-inteligencia-artificial',
    'blog-marketing-digital',
    'blog-tecnologia',
    'blog-transformacao-digital',
    'blog-vendas'
]

def main():
    """Função principal."""
    # Configurar argumentos
    parser = argparse.ArgumentParser(description='Gerador de artigos para WordPress')
    parser.add_argument('--topic', required=True, help='Tópico do artigo')
    parser.add_argument('--category', required=True, choices=CATEGORIES, help='Categoria do artigo')
    parser.add_argument('--publish', action='store_true', help='Publicar no WordPress')
    args = parser.parse_args()
    
    # Mostrar categorias disponíveis
    logger.info("Categorias disponíveis:")
    for category in CATEGORIES:
        logger.info(f"- {category}")
    
    # Inicializar cliente Dify
    dify_client = DifyClient()
    
    # Inicializar gerador de conteúdo
    content_generator = ContentGenerator(dify_client)
    
    # Gerar artigo
    logger.info(f"Gerando artigo sobre '{args.topic}' na categoria '{args.category}'")
    article = content_generator.generate_article(args.topic, args.category)
    
    # Converter para HTML
    html = article.to_html()
    print(html)

if __name__ == '__main__':
    main()