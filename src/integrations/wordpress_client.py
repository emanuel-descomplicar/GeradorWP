#!/usr/bin/env python3
"""
Cliente WordPress para publicação de artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
import xmlrpc.client
import json
import requests
import base64
from typing import Dict, Any, Optional, List, Union
from pathlib import Path
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, GetPost
from wordpress_xmlrpc.methods.media import UploadFile
from wordpress_xmlrpc.methods.taxonomies import GetTerms

# Carrega variáveis de ambiente
load_dotenv()

class WordPressClient:
    """Cliente para publicação de artigos no WordPress."""
    
    def __init__(self):
        """Inicializa o cliente WordPress."""
        self.wp_url = os.getenv("WP_URL", "")
        self.wp_username = os.getenv("WP_USERNAME", "")
        self.wp_password = os.getenv("WP_PASSWORD", "")
        self.wp_rest_url = f"{self.wp_url}/wp-json/wp/v2"
        
        if not self.wp_url or not self.wp_username or not self.wp_password:
            logging.warning("Credenciais do WordPress não configuradas. Usando modo de simulação.")
            self.simulation_mode = True
        else:
            self.simulation_mode = False
            self.client = Client(f'{self.wp_url}/xmlrpc.php', self.wp_username, self.wp_password)
    
    def upload_image(self, image_path: str, title: str = "") -> Dict[str, Any]:
        """
        Carrega uma imagem para a biblioteca de mídia do WordPress.
        
        Args:
            image_path (str): Caminho para o arquivo de imagem.
            title (str, optional): Título da imagem. Defaults to "".
            
        Returns:
            Dict[str, Any]: Dados da imagem carregada, incluindo ID e URL.
        """
        # Converte Path para string, se necessário
        image_path = str(image_path)
        
        if self.simulation_mode:
            logging.info(f"Simulação: Imagem {image_path} seria carregada como {title}")
            return {
                "id": 999,
                "url": f"https://example.com/simulated-{Path(image_path).name}"
            }
        
        # Preparar dados do arquivo
        with open(image_path, 'rb') as img:
            image_data = {
                'name': Path(image_path).name,
                'type': 'image/jpeg' if image_path.endswith('.jpg') or image_path.endswith('.jpeg') else 'image/webp',
                'bits': xmlrpc.client.Binary(img.read()),
                'title': title or Path(image_path).stem,
                'overwrite': True
            }
        
        try:
            # Upload da imagem
            response = self.client.call(UploadFile(image_data))
            image_id = response.get('id', 0)
            image_url = response.get('url', '')
            
            logging.info(f"Imagem carregada com sucesso. ID: {image_id}, URL: {image_url}")
            
            return {
                "id": image_id,
                "url": image_url
            }
        except Exception as e:
            logging.error(f"Erro ao carregar imagem: {str(e)}")
            return {
                "id": 0,
                "url": ""
            }
    
    def get_category_id(self, category_name: str) -> int:
        """
        Obtém o ID de uma categoria pelo nome.
        
        Args:
            category_name (str): Nome da categoria.
            
        Returns:
            int: ID da categoria, ou 1 se não encontrada.
        """
        if self.simulation_mode:
            logging.info(f"Simulação: Buscando ID para categoria '{category_name}'")
            return 1
        
        try:
            # Buscar todas as categorias
            categories = self.client.call(GetTerms('category'))
            
            # Converter para minúsculas para comparação case-insensitive
            category_name_lower = category_name.lower().strip()
            
            # Buscar a categoria pelo nome exato primeiro
            for category in categories:
                cat_name = getattr(category, 'name', '')
                cat_id = getattr(category, 'id', 0)
                if cat_name.lower().strip() == category_name_lower:
                    logging.info(f"Categoria '{category_name}' encontrada com ID {cat_id}")
                    return cat_id
            
            # Se não encontrar pelo nome exato, tentar buscar por correspondência parcial
            for category in categories:
                cat_name = getattr(category, 'name', '')
                cat_id = getattr(category, 'id', 0)
                if category_name_lower in cat_name.lower():
                    logging.info(f"Categoria parcial '{category_name}' encontrada como '{cat_name}' com ID {cat_id}")
                    return cat_id
            
            # Se ainda não encontrar, usar a primeira categoria ou a categoria padrão (1)
            if categories and len(categories) > 0:
                default_id = getattr(categories[0], 'id', 1)
                logging.warning(f"Categoria '{category_name}' não encontrada, usando primeira categoria disponível (ID {default_id})")
                return default_id
            
            logging.warning(f"Categoria '{category_name}' não encontrada e nenhuma categoria disponível. Usando ID padrão 1")
            return 1
        except Exception as e:
            logging.error(f"Erro ao buscar categoria '{category_name}': {str(e)}")
            return 1
    
    def publish_article(self, 
                        title: str, 
                        content: str, 
                        category: int, 
                        featured_image: Optional[int] = None,
                        status: str = 'publish',
                        tags: Optional[list] = None) -> Dict[str, Any]:
        """
        Publica um artigo no WordPress usando a REST API.
        
        Args:
            title (str): Título do artigo.
            content (str): Conteúdo HTML do artigo.
            category (int): ID da categoria do artigo.
            featured_image (Optional[int], optional): ID da imagem destacada. Defaults to None.
            status (str, optional): Status da publicação ('draft', 'publish', etc.). Defaults to 'publish'.
            tags (Optional[list], optional): Lista de tags para o artigo. Defaults to None.
            
        Returns:
            Dict[str, Any]: Dados do artigo publicado, incluindo ID e URL.
        """
        if self.simulation_mode:
            logging.info(f"Simulação: Artigo '{title}' seria publicado na categoria ID {category}")
            logging.info(f"Conteúdo do artigo (primeiros 100 caracteres): {content[:100]}...")
            if tags:
                logging.info(f"Tags: {', '.join(tags)}")
            
            # Simulando publicação bem-sucedida
            return {
                "id": 12345,
                "link": f"https://example.com/simulated-post/{title.lower().replace(' ', '-')}",
                "status": status,
                "categories": [category],
                "tags": [1, 2, 3] if tags else []
            }
        
        try:
            # Usar a WordPress REST API em vez da biblioteca XMLRPC
            endpoint = f"{self.wp_rest_url}/posts"
            credentials = f"{self.wp_username}:{self.wp_password}"
            token = base64.b64encode(credentials.encode()).decode()
            headers = {
                'Authorization': f'Basic {token}',
                'Content-Type': 'application/json'
            }
            
            # Criar dados do post
            post_data = {
                'title': title,
                'content': content,
                'status': status,
                'categories': [category]
            }
            
            # Adicionar imagem destacada, se disponível
            if featured_image and isinstance(featured_image, int) and featured_image > 0:
                post_data['featured_media'] = featured_image
            
            # Adicionar tags, se fornecidas
            if tags and isinstance(tags, list) and len(tags) > 0:
                # Remover tags vazias ou muito curtas
                valid_tags = [tag for tag in tags if tag and len(tag) > 2]
                if valid_tags:
                    # Criar tags no WordPress se não existirem
                    tag_ids = []
                    for tag_name in valid_tags:
                        try:
                            # Verificar se a tag já existe
                            tag_endpoint = f"{self.wp_rest_url}/tags?search={tag_name}"
                            tag_response = requests.get(tag_endpoint, headers=headers)
                            
                            if tag_response.status_code == 200:
                                existing_tags = tag_response.json()
                                
                                # Se a tag existe, use seu ID
                                if existing_tags and len(existing_tags) > 0:
                                    tag_id = existing_tags[0]['id']
                                    tag_ids.append(tag_id)
                                else:
                                    # Criar a tag
                                    create_tag_endpoint = f"{self.wp_rest_url}/tags"
                                    tag_data = {'name': tag_name}
                                    create_response = requests.post(create_tag_endpoint, json=tag_data, headers=headers)
                                    
                                    if create_response.status_code in [200, 201]:
                                        new_tag = create_response.json()
                                        tag_ids.append(new_tag['id'])
                        except Exception as e:
                            logging.warning(f"Erro ao processar tag '{tag_name}': {str(e)}")
                    
                    # Adicionar as tags ao post
                    if tag_ids:
                        post_data['tags'] = tag_ids
            
            # Fazer a requisição para criar o post
            logging.info(f"Enviando requisição REST para criar artigo: {title}")
            response = requests.post(endpoint, json=post_data, headers=headers)
            
            # Verificar resposta
            if response.status_code in [200, 201]:
                post_data = response.json()
                post_id = post_data.get('id', 0)
                post_url = post_data.get('link', '')
                
                logging.info(f"Artigo publicado com sucesso via REST API. ID: {post_id}, URL: {post_url}")
                
                return {
                    "id": post_id,
                    "link": post_url,
                    "status": post_data.get('status', status),
                    "categories": post_data.get('categories', [category]),
                    "tags": post_data.get('tags', [])
                }
            else:
                error_message = f"Erro na API: {response.status_code} - {response.text}"
                logging.error(error_message)
                return {
                    "id": 0,
                    "link": "",
                    "status": "error",
                    "error": error_message
                }
                
        except Exception as e:
            error_message = str(e)
            logging.error(f"Erro ao publicar artigo: {error_message}")
            
            return {
                "id": 0,
                "link": "",
                "status": "error",
                "error": error_message
            } 