#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente para integração com WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
from typing import Dict, List, Optional
import requests
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import media, posts, taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logging
logger = logging.getLogger(__name__)

class WordPressClient:
    """Cliente para interação com WordPress via XML-RPC."""
    
    def __init__(self, url: str = None, username: str = None, password: str = None):
        """Inicializa o cliente WordPress.
        
        Args:
            url: URL do WordPress (se None, usa WP_URL do .env)
            username: Nome de utilizador (se None, usa WP_USERNAME do .env)
            password: Senha (se None, usa WP_PASSWORD do .env)
        """
        self.url = url or os.getenv('WP_URL')
        self.username = username or os.getenv('WP_USERNAME')
        self.password = password or os.getenv('WP_PASSWORD')
        
        if not all([self.url, self.username, self.password]):
            raise ValueError("Credenciais WordPress incompletas. Verifique as variáveis de ambiente.")
        
        # Garantir que a URL termina com /xmlrpc.php
        if not self.url.endswith('/xmlrpc.php'):
            self.url = f"{self.url.rstrip('/')}/xmlrpc.php"
        
        self.client = Client(self.url, self.username, self.password)
        logger.info(f"WordPressClient inicializado para {self.url}")
    
    def create_post(self, title: str, content: str, status: str = 'draft',
                   category_ids: List[int] = None, tag_ids: List[int] = None,
                   featured_media_id: Optional[int] = None) -> int:
        """Cria um novo post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo em HTML
            status: Estado do post ('draft', 'publish', etc.)
            category_ids: IDs das categorias
            tag_ids: IDs das tags
            featured_media_id: ID da imagem destacada
        
        Returns:
            ID do post criado
        """
        post = WordPressPost()
        post.title = title
        post.content = content
        post.post_status = status
        
        if category_ids:
            post.terms_names = {'category': category_ids}
        
        if tag_ids:
            post.terms_names = {'post_tag': tag_ids}
        
        if featured_media_id:
            post.thumbnail = featured_media_id
        
        try:
            post_id = self.client.call(posts.NewPost(post))
            logger.info(f"Post criado com ID: {post_id}")
            return post_id
        except Exception as e:
            logger.error(f"Erro ao criar post: {str(e)}")
            raise
    
    def upload_media(self, file_path: str, title: Optional[str] = None) -> int:
        """Faz upload de um ficheiro de media para o WordPress.
        
        Args:
            file_path: Caminho do ficheiro
            title: Título do media (opcional)
        
        Returns:
            ID do media no WordPress
        """
        # Preparar dados do ficheiro
        with open(file_path, 'rb') as img:
            data = {
                'name': os.path.basename(file_path),
                'type': 'image/jpeg',  # Ajustar conforme necessário
                'bits': xmlrpc_client.Binary(img.read()),
                'overwrite': True
            }
            
            if title:
                data['title'] = title
        
        try:
            response = self.client.call(media.UploadFile(data))
            media_id = response['id']
            logger.info(f"Media enviado com ID: {media_id}")
            return media_id
        except Exception as e:
            logger.error(f"Erro ao enviar media: {str(e)}")
            raise
    
    def get_categories(self) -> List[Dict]:
        """Obtém lista de categorias do WordPress.
        
        Returns:
            Lista de categorias com seus IDs e nomes
        """
        try:
            categories = self.client.call(taxonomies.GetTerms('category'))
            return [{'id': cat.id, 'name': cat.name, 'slug': cat.slug} for cat in categories]
        except Exception as e:
            logger.error(f"Erro ao obter categorias: {str(e)}")
            raise
    
    def get_tags(self) -> List[Dict]:
        """Obtém lista de tags do WordPress.
        
        Returns:
            Lista de tags com seus IDs e nomes
        """
        try:
            tags = self.client.call(taxonomies.GetTerms('post_tag'))
            return [{'id': tag.id, 'name': tag.name, 'slug': tag.slug} for tag in tags]
        except Exception as e:
            logger.error(f"Erro ao obter tags: {str(e)}")
            raise
    
    def create_tag(self, name: str, slug: Optional[str] = None) -> int:
        """Cria uma nova tag no WordPress.
        
        Args:
            name: Nome da tag
            slug: Slug da tag (opcional)
        
        Returns:
            ID da tag criada
        """
        tag_data = {
            'name': name
        }
        
        if slug:
            tag_data['slug'] = slug
        
        try:
            tag = self.client.call(taxonomies.NewTerm({
                'taxonomy': 'post_tag',
                'name': name,
                'slug': slug
            }))
            logger.info(f"Tag criada com ID: {tag.id}")
            return tag.id
        except Exception as e:
            logger.error(f"Erro ao criar tag: {str(e)}")
            raise
    
    def update_post(self, post_id: int, title: Optional[str] = None,
                   content: Optional[str] = None, status: Optional[str] = None,
                   category_ids: Optional[List[int]] = None,
                   tag_ids: Optional[List[int]] = None,
                   featured_media_id: Optional[int] = None) -> bool:
        """Atualiza um post existente.
        
        Args:
            post_id: ID do post
            title: Novo título (opcional)
            content: Novo conteúdo (opcional)
            status: Novo estado (opcional)
            category_ids: Novos IDs de categorias (opcional)
            tag_ids: Novos IDs de tags (opcional)
            featured_media_id: Novo ID de imagem destacada (opcional)
        
        Returns:
            True se atualizado com sucesso
        """
        post = WordPressPost()
        post.id = post_id
        
        if title is not None:
            post.title = title
        if content is not None:
            post.content = content
        if status is not None:
            post.post_status = status
        if category_ids is not None:
            post.terms_names = {'category': category_ids}
        if tag_ids is not None:
            post.terms_names = {'post_tag': tag_ids}
        if featured_media_id is not None:
            post.thumbnail = featured_media_id
        
        try:
            result = self.client.call(posts.EditPost(post_id, post))
            logger.info(f"Post {post_id} atualizado: {result}")
            return result
        except Exception as e:
            logger.error(f"Erro ao atualizar post: {str(e)}")
            raise