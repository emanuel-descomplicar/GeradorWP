#!/usr/bin/env python3
"""
Script para listar categorias do WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import logging
import requests
from dotenv import load_dotenv
from typing import List, Dict, Any
from urllib.parse import urljoin

# Configuração de logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def get_categories() -> List[Dict[str, Any]]:
    """Obtém todas as categorias do WordPress usando a REST API."""
    wp_url = os.getenv("WP_URL")
    wp_username = os.getenv("WP_USERNAME")
    wp_password = os.getenv("WP_APP_PASSWORD")
    
    if not wp_url or not wp_username or not wp_password:
        raise ValueError("Configurações do WordPress não encontradas no arquivo .env")
    
    # Configura a autenticação
    auth = (wp_username, wp_password)
    
    # Faz a requisição para a API REST do WordPress
    api_url = urljoin(wp_url, "/wp-json/wp/v2/categories")
    response = requests.get(api_url, auth=auth, params={"per_page": 100})
    
    if response.status_code != 200:
        raise Exception(f"Erro ao obter categorias: {response.status_code} - {response.text}")
    
    return response.json()

def main():
    """Função principal."""
    try:
        print("Listando categorias do blog...")
        
        # Obtém todas as categorias
        categories = get_categories()
        
        # Filtra apenas categorias que começam com 'blog-'
        blog_categories = [cat for cat in categories if cat['slug'].startswith('blog-')]
        
        if not blog_categories:
            print("\nNenhuma categoria do blog encontrada.")
            return 0
        
        # Imprime as categorias
        print("\nCategorias do blog encontradas:")
        print("-" * 100)
        print(f"{'ID':<6} {'Nome':<30} {'Slug':<25} {'Posts':<6} {'Descrição'}")
        print("-" * 100)
        
        for category in sorted(blog_categories, key=lambda x: x['name']):
            print(f"{category['id']:<6} {category['name'][:30]:<30} {category['slug'][:25]:<25} {category['count']:<6} {category.get('description', '')[:50]}")
        
        print("-" * 100)
        print(f"Total de categorias do blog: {len(blog_categories)}")
        
        # Gera lista de IDs para uso no script de publicação
        category_ids = [cat['id'] for cat in blog_categories]
        print("\nLista de IDs para uso no script de publicação:")
        print(f"category_ids = {category_ids}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Erro ao listar categorias: {str(e)}")
        print(f"Erro ao listar categorias: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 