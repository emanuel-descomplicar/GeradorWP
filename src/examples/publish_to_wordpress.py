#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de publicação de artigo no WordPress.

Este script demonstra como utilizar o WordPressClient para publicar
um artigo HTML para o WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import glob
from pathlib import Path
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar o diretório pai ao path para importar o módulo wordpress_client
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.integrations.wordpress_client import WordPressClient

def load_environment_variables():
    """Carrega as variáveis de ambiente do arquivo .env"""
    dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env')
    load_dotenv(dotenv_path)
    
    required_vars = ['WP_URL', 'WP_USERNAME', 'WP_PASSWORD']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Variáveis de ambiente não definidas: {', '.join(missing_vars)}")
        logger.error("Por favor, crie um arquivo .env com as configurações necessárias.")
        sys.exit(1)
    
    logger.info("Variáveis de ambiente carregadas com sucesso.")

def get_latest_html_file(output_dir='output'):
    """
    Obtém o caminho para o arquivo HTML mais recente.
    
    Args:
        output_dir: Diretório onde os arquivos HTML estão armazenados
        
    Returns:
        Tuple com (caminho do arquivo, categoria extraída do nome)
    """
    # Criar o diretório output se não existir
    if not os.path.exists(output_dir):
        logger.warning(f"Diretório '{output_dir}' não encontrado. Criando...")
        os.makedirs(output_dir)
        return None, None
    
    # Buscar todos os arquivos HTML
    html_files = glob.glob(os.path.join(output_dir, '*.html'))
    
    if not html_files:
        logger.warning(f"Nenhum arquivo HTML encontrado em '{output_dir}'")
        return None, None
    
    # Ordenar por data de modificação, mais recente primeiro
    latest_file = max(html_files, key=os.path.getmtime)
    
    # Extrair categoria do nome do arquivo (formato: categoria_topic.html)
    filename = os.path.basename(latest_file)
    category_slug = None
    
    if '_' in filename:
        category_slug = filename.split('_')[0]
    
    logger.info(f"Arquivo HTML mais recente: {latest_file}")
    return latest_file, category_slug

def publish_article(html_file=None, category=None, featured_image=None, status=None):
    """
    Publica um artigo HTML no WordPress.
    
    Args:
        html_file: Caminho para o arquivo HTML (se None, usa o mais recente)
        category: Slug da categoria (se None, extrai do nome do arquivo)
        featured_image: Caminho para a imagem destacada (opcional)
        status: Status do post (draft, publish, pending)
        
    Returns:
        Dados do post publicado ou None se falhar
    """
    # Obter o arquivo HTML mais recente se não especificado
    if html_file is None:
        html_file, file_category = get_latest_html_file()
        if not html_file:
            logger.error("Nenhum arquivo HTML encontrado para publicação")
            return None
        
        # Usar categoria do arquivo se não especificada
        if not category and file_category:
            category = file_category
    
    # Verificar arquivo HTML
    if not os.path.exists(html_file):
        logger.error(f"Arquivo HTML não encontrado: {html_file}")
        return None
    
    # Verificar categoria
    if not category:
        logger.error("Categoria não especificada e não foi possível extrair do nome do arquivo")
        return None
    
    # Verificar imagem destacada
    if not featured_image:
        featured_image = os.getenv('WP_FEATURED_IMAGE_PATH')
        if featured_image and os.path.exists(featured_image):
            logger.info(f"Usando imagem destacada do .env: {featured_image}")
        else:
            featured_image = None
            logger.info("Nenhuma imagem destacada será utilizada")
    
    # Carregar conteúdo HTML
    try:
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        logger.error(f"Erro ao ler arquivo HTML: {str(e)}")
        return None
    
    # Inicializar cliente WordPress
    try:
        wp_client = WordPressClient()
    except Exception as e:
        logger.error(f"Erro ao inicializar cliente WordPress: {str(e)}")
        return None
    
    # Publicar artigo
    try:
        result = wp_client.publish_article_from_html(
            html_content=html_content,
            category_slug=category,
            featured_image_path=featured_image,
            status=status
        )
        
        if result:
            logger.info(f"Artigo publicado com sucesso: {result.get('link')}")
            if result.get('status') == 'draft':
                logger.info(f"O artigo foi salvo como rascunho. Acesse o painel WordPress para revisá-lo e publicá-lo.")
        else:
            logger.error("Falha ao publicar o artigo")
        
        return result
    except Exception as e:
        logger.error(f"Erro ao publicar artigo: {str(e)}")
        return None

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_environment_variables()
    
    # Obter argumentos da linha de comando
    import argparse
    parser = argparse.ArgumentParser(description='Publica um artigo HTML no WordPress')
    parser.add_argument('--file', help='Caminho para o arquivo HTML (opcional)')
    parser.add_argument('--category', help='Slug da categoria (opcional)')
    parser.add_argument('--image', help='Caminho para a imagem destacada (opcional)')
    parser.add_argument('--status', choices=['draft', 'publish', 'pending'], 
                       default=os.getenv('WP_POST_STATUS', 'draft'),
                       help='Status do post (default: valor de WP_POST_STATUS ou "draft")')
    
    args = parser.parse_args()
    
    # Publicar o artigo
    result = publish_article(
        html_file=args.file,
        category=args.category,
        featured_image=args.image,
        status=args.status
    )
    
    # Sair com código de erro se falhar
    if not result:
        sys.exit(1)
    
    sys.exit(0)

if __name__ == "__main__":
    main() 