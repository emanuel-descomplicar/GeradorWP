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

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Função principal do script."""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Configurar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Gera e publica um artigo no WordPress.')
    parser.add_argument('--topic', required=True, help='Tópico do artigo')
    parser.add_argument('--category', required=True, help='Categoria do artigo')
    parser.add_argument('--publish', action='store_true', help='Publicar imediatamente')
    args = parser.parse_args()
    
    try:
        # Inicializar clientes
        dify_client = DifyClient()
        content_generator = ContentGenerator(dify_client)
        
        # Listar categorias disponíveis
        logger.info("Categorias disponíveis:")
        for category in ['blog-e-commerce', 'blog-empreendedorismo', 'blog-gestao-pmes',
                        'blog-inteligencia-artificial', 'blog-marketing-digital',
                        'blog-tecnologia', 'blog-transformacao-digital', 'blog-vendas']:
            logger.info(f"- {category}")
        
        # Validar categoria
        if args.category not in ['blog-e-commerce', 'blog-empreendedorismo', 'blog-gestao-pmes',
                               'blog-inteligencia-artificial', 'blog-marketing-digital',
                               'blog-tecnologia', 'blog-transformacao-digital', 'blog-vendas']:
            raise ValueError(f"Categoria inválida: {args.category}")
        
        # Gerar artigo
        logger.info(f"Gerando artigo sobre '{args.topic}' na categoria '{args.category}'")
        article = content_generator.generate_article(args.topic, args.category)
        
        if args.publish:
            # Inicializar cliente WordPress
            wp_client = WordPressClient()
            
            # Processar artigo para WordPress
            html = article.to_html()
            
            # Encontrar categoria no WordPress
            categories = wp_client.get_categories()
            category_id = None
            for cat in categories:
                if cat['slug'] == args.category:
                    category_id = cat['id']
                    break
            
            if not category_id:
                raise ValueError(f"Categoria não encontrada no WordPress: {args.category}")
            
            # Criar tags
            tag_ids = []
            for tag_name in article.meta['tags']:
                try:
                    tag = wp_client.create_tag(tag_name)
                    tag_ids.append(tag)
                except Exception as e:
                    logger.warning(f"Erro ao criar tag '{tag_name}': {str(e)}")
            
            # Criar post
            status = 'publish' if args.publish else 'draft'
            post_id = wp_client.create_post(
                title=article.title,
                content=html,
                status=status,
                category_ids=[category_id],
                tag_ids=tag_ids,
                featured_media_id=article.meta.get('featured_image')
            )
            
            logger.info(f"Artigo publicado com sucesso: https://descomplicar.pt/?p={post_id}")
        else:
            # Apenas mostrar o HTML
            print(article.to_html())
    
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()