#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cliente para integração com a API REST do WordPress.

Este módulo fornece funcionalidades para publicar artigos no WordPress
através da API REST.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import mimetypes
import requests
from typing import Dict, List, Optional, Any, Tuple
from bs4 import BeautifulSoup
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WordPressClient:
    """Cliente para interagir com a API REST do WordPress."""

    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        """
        Inicializa o cliente WordPress com as credenciais.
        
        Args:
            base_url: URL base do site WordPress (ex: https://exemplo.com)
            username: Nome de utilizador para autenticação
            password: Senha do utilizador
        """
        self.base_url = base_url or os.getenv('WP_URL')
        self.username = username or os.getenv('WP_USERNAME')
        self.password = password or os.getenv('WP_PASSWORD')
        self.post_status = os.getenv('WP_POST_STATUS', 'draft')
        
        if not self.base_url or not self.username or not self.password:
            raise ValueError("WordPress URL, username e password são necessários. "
                          "Defina as variáveis de ambiente WP_URL, WP_USERNAME e WP_PASSWORD.")
        
        # Remover a barra final se existir
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        self.auth = (self.username, self.password)
        
        logger.info(f"Cliente WordPress inicializado para {self.base_url}")

    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de categorias disponíveis no WordPress.
        
        Returns:
            Lista de categorias com seus IDs e nomes
        """
        try:
            response = requests.get(f"{self.api_url}/categories?per_page=100", auth=self.auth)
            response.raise_for_status()
            categories = response.json()
            logger.info(f"Obtidas {len(categories)} categorias")
            return categories
        except requests.RequestException as e:
            logger.error(f"Erro ao obter categorias: {str(e)}")
            return []

    def get_category_id(self, slug: str) -> Optional[int]:
        """
        Obtém o ID de uma categoria pelo seu slug.
        
        Args:
            slug: Slug da categoria (ex: 'blog-tecnologia')
            
        Returns:
            ID da categoria ou None se não encontrada
        """
        try:
            response = requests.get(f"{self.api_url}/categories?slug={slug}", auth=self.auth)
            response.raise_for_status()
            categories = response.json()
            
            if categories:
                category_id = categories[0]['id']
                logger.info(f"Categoria '{slug}' encontrada com ID {category_id}")
                return category_id
            else:
                logger.warning(f"Categoria com slug '{slug}' não encontrada")
                return None
        except requests.RequestException as e:
            logger.error(f"Erro ao obter categoria por slug: {str(e)}")
            return None

    def upload_media(self, file_path: str) -> Optional[int]:
        """
        Faz upload de um arquivo de mídia para o WordPress.
        
        Args:
            file_path: Caminho para o arquivo a ser enviado
            
        Returns:
            ID da mídia ou None se o upload falhar
        """
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            return None
            
        try:
            filename = os.path.basename(file_path)
            mimetype = mimetypes.guess_type(file_path)[0]
            
            with open(file_path, 'rb') as file:
                media_data = file.read()
                
            headers = {
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': mimetype,
            }
            
            response = requests.post(
                f"{self.api_url}/media",
                auth=self.auth,
                headers=headers,
                data=media_data
            )
            response.raise_for_status()
            media_id = response.json()['id']
            logger.info(f"Mídia '{filename}' enviada com ID {media_id}")
            return media_id
        except requests.RequestException as e:
            logger.error(f"Erro ao fazer upload da mídia: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao fazer upload da mídia: {str(e)}")
            return None

    def create_post(self, 
                   title: str, 
                   content: str, 
                   category_id: Optional[int] = None,
                   featured_media_id: Optional[int] = None,
                   status: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Cria um novo post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo do post (HTML)
            category_id: ID da categoria (opcional)
            featured_media_id: ID da imagem destacada (opcional)
            status: Status do post ('draft', 'publish', 'pending')
            
        Returns:
            Dados do post criado ou None se falhar
        """
        status = status or self.post_status
        
        post_data = {
            'title': title,
            'content': content,
            'status': status,
        }
        
        if category_id:
            post_data['categories'] = [category_id]
            
        if featured_media_id:
            post_data['featured_media'] = featured_media_id
        
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                auth=self.auth,
                json=post_data
            )
            response.raise_for_status()
            post = response.json()
            logger.info(f"Post criado com ID {post['id']} e status '{status}'")
            return post
        except requests.RequestException as e:
            error_message = f"Erro ao criar post: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_message += f" - Resposta: {e.response.text}"
            logger.error(error_message)
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao criar post: {str(e)}")
            return None

    def html_to_wordpress(self, html_content: str, title: Optional[str] = None) -> Tuple[str, str]:
        """
        Processa o conteúdo HTML para publicação no WordPress.
        
        Args:
            html_content: Conteúdo HTML do artigo
            title: Título do artigo (se não fornecido, extrai do HTML)
            
        Returns:
            Tupla com (título, conteúdo formatado)
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extrair o título se não fornecido
        if not title:
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.text.strip()
                h1_tag.decompose()  # Remove o h1 do conteúdo para evitar duplicação
        
        # Processar o conteúdo para WordPress
        # Pode ser expandido para adicionar classes, formatar elementos específicos, etc.
        
        # Converter o conteúdo de volta para HTML
        content = str(soup)
        
        logger.info(f"HTML processado para WordPress. Título: {title}")
        return title, content

    def publish_article_from_html(self, 
                                 html_content: str, 
                                 category_slug: str, 
                                 featured_image_path: Optional[str] = None,
                                 title: Optional[str] = None,
                                 status: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Publica um artigo a partir de conteúdo HTML.
        
        Args:
            html_content: Conteúdo HTML do artigo
            category_slug: Slug da categoria
            featured_image_path: Caminho para a imagem destacada (opcional)
            title: Título do artigo (se None, será extraído do HTML)
            status: Status do post ('draft', 'publish', 'pending')
            
        Returns:
            Dados do post publicado ou None se falhar
        """
        # Processar HTML para WordPress
        extracted_title, processed_content = self.html_to_wordpress(html_content, title)
        
        # Obter ID da categoria
        category_id = self.get_category_id(category_slug)
        if not category_id:
            logger.warning(f"Categoria '{category_slug}' não encontrada. Post será publicado sem categoria.")
        
        # Upload da imagem destacada
        featured_media_id = None
        if featured_image_path:
            featured_media_id = self.upload_media(featured_image_path)
            if not featured_media_id:
                logger.warning("Não foi possível fazer upload da imagem destacada.")
        
        # Criar o post
        result = self.create_post(
            title=extracted_title,
            content=processed_content,
            category_id=category_id,
            featured_media_id=featured_media_id,
            status=status
        )
        
        if result:
            logger.info(f"Artigo publicado com sucesso: {result['link']}")
        else:
            logger.error("Falha ao publicar o artigo")
            
        return result 