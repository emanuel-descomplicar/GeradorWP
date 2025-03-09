#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de geração de artigo com publicação opcional no WordPress.

Este script demonstra como gerar um artigo utilizando o ContentGenerator e
opcionalmente publicá-lo diretamente no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging
import argparse

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.config.content_config import WP_CATEGORIES
from src.generators.content_generator import ContentGenerator
from src.integrations.dify_client import DifyClient

# Importar o cliente WordPress apenas se a opção de publicação estiver ativada
PUBLISH_TO_WORDPRESS = os.getenv('PUBLISH_TO_WORDPRESS', 'false').lower() in ('true', '1', 't', 'yes')
if PUBLISH_TO_WORDPRESS:
    try:
        from src.integrations.wordpress_client import WordPressClient
    except ImportError as e:
        logger.error(f"Erro ao importar módulos WordPress: {e}")
        PUBLISH_TO_WORDPRESS = False

def print_available_categories():
    """Imprime as categorias disponíveis para o artigo."""
    logger.info("Categorias disponíveis para o artigo:")
    for slug, info in WP_CATEGORIES.items():
        logger.info(f"  - {info['name']} ({slug})")

def generate_article(topic, category, output_dir='output', validate_content=True, publish=False):
    """
    Gera um artigo sobre o tópico especificado na categoria selecionada.
    
    Args:
        topic: Tópico do artigo
        category: Categoria para o artigo
        output_dir: Diretório para salvar o artigo
        validate_content: Se True, valida o conteúdo antes de salvar
        publish: Se True, publica no WordPress após gerar
        
    Returns:
        Tuple com (status, caminho_do_arquivo)
    """
    try:
        # Validar categoria
        if category not in WP_CATEGORIES:
            logger.error(f"Categoria inválida: {category}")
            logger.info("Categorias disponíveis:")
            for cat_slug, cat_info in WP_CATEGORIES.items():
                logger.info(f"  - {cat_info['name']} ({cat_slug})")
            return False, None
        
        # Inicializar o gerador de conteúdo
        logger.info(f"Gerando artigo sobre: {topic}")
        logger.info(f"Categoria: {category} ({WP_CATEGORIES[category]['name']})")
        
        # Criar instância do DifyClient usando as variáveis de ambiente
        dify_client = DifyClient()
        
        # Criar instância do ContentGenerator
        content_generator = ContentGenerator(dify_client)
        
        # Gerar o artigo
        article = content_generator.generate_article(topic, category)
        
        # Validar o artigo
        if validate_content and not article.is_valid():
            logger.error("Artigo gerado é inválido:")
            for section_name, errors in article.validation_errors.items():
                logger.error(f"  - {section_name}: {', '.join(errors)}")
            return False, None
        
        # Criar o diretório de saída se não existir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Criar um nome de arquivo baseado na categoria e no tópico
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        sanitized_topic = topic.lower().replace(' ', '-').replace('/', '-')
        output_file = os.path.join(
            output_dir, 
            f"{category}_{sanitized_topic}_{timestamp}.html"
        )
        
        # Salvar o artigo
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(article.to_html())
        
        logger.info(f"Artigo salvo em: {output_file}")
        
        # Publicar no WordPress se solicitado
        if publish and PUBLISH_TO_WORDPRESS:
            logger.info("Publicando artigo no WordPress...")
            try:
                # Inicializar cliente WordPress
                wp_client = WordPressClient()
                
                # Ler o conteúdo HTML
                with open(output_file, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                
                # Publicar o artigo
                result = wp_client.publish_article_from_html(
                    html_content=html_content,
                    category_slug=category,
                    featured_image_path=os.getenv('WP_FEATURED_IMAGE_PATH'),
                    title=article.title
                )
                
                if result:
                    logger.info(f"Artigo publicado com sucesso: {result.get('link')}")
                    return True, output_file
                else:
                    logger.error("Falha ao publicar o artigo no WordPress")
                    return False, output_file
                    
            except Exception as e:
                logger.error(f"Erro ao publicar artigo: {str(e)}")
                import traceback
                traceback.print_exc()
                return False, output_file
        
        return True, output_file
        
    except Exception as e:
        logger.error(f"Erro ao gerar artigo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Listar categorias disponíveis
    print_available_categories()
    
    # Configurações padrão para o artigo
    DEFAULT_TOPIC = "Inteligência Artificial para PMEs"
    DEFAULT_CATEGORY = "blog-inteligencia-artificial"  # Utilizando a nova categoria do WordPress
    
    # Verificar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Gerar um artigo para WordPress')
    parser.add_argument('--topic', default=DEFAULT_TOPIC, help='Tópico do artigo')
    parser.add_argument('--category', default=DEFAULT_CATEGORY, help='Categoria do artigo')
    parser.add_argument('--output-dir', default='output', help='Diretório de saída')
    parser.add_argument('--publish', action='store_true', help='Publicar no WordPress após gerar')
    
    args = parser.parse_args()
    
    # Gerar o artigo
    success, file_path = generate_article(
        topic=args.topic,
        category=args.category,
        output_dir=args.output_dir,
        publish=args.publish or PUBLISH_TO_WORDPRESS
    )
    
    # Sair com código apropriado
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 