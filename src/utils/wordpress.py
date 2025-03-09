"""
Utilitários para integração com o WordPress.
"""

import os
import json
import requests
from typing import Dict, List, Optional, Union
from pathlib import Path
from .exceptions import WordPressError
from .logger import Logger
from ..config.config import (
    WP_URL,
    WP_USERNAME,
    WP_APP_PASSWORD,
    DEFAULT_CATEGORY,
    DEFAULT_TAGS
)

class WordPressClient:
    """Cliente para integração com o WordPress."""
    
    def __init__(self):
        """Inicializa o cliente WordPress."""
        self.logger = Logger(__name__)
        
        # Configurar URL base da API
        self.api_url = f"{WP_URL}/wp-json/wp/v2"
        
        # Configurar autenticação
        self.auth = (WP_USERNAME, WP_APP_PASSWORD)
        
        # Cache de categorias
        self._categories = {}
        
        # Cache de tags
        self._tags = {}
    
    def get_category_id(self, category_name: str) -> int:
        """
        Obtém o ID de uma categoria pelo nome.
        Se a categoria não existir, ela será criada.
        
        Args:
            category_name: Nome da categoria
            
        Returns:
            ID da categoria
        """
        try:
            # Verificar cache
            if category_name in self._categories:
                return self._categories[category_name]
            
            # Buscar todas as categorias
            response = requests.get(f"{self.api_url}/categories", auth=self.auth)
            response.raise_for_status()
            
            # Atualizar cache
            categories = response.json()
            for category in categories:
                self._categories[category['name']] = category['id']
            
            # Retornar ID da categoria se existir
            if category_name in self._categories:
                return self._categories[category_name]
            
            # Criar categoria se não existir
            response = requests.post(
                f"{self.api_url}/categories",
                auth=self.auth,
                json={
                    'name': category_name,
                    'slug': category_name.lower().replace(' ', '-')
                }
            )
            response.raise_for_status()
            
            # Atualizar cache
            category = response.json()
            self._categories[category['name']] = category['id']
            
            return category['id']
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao buscar/criar categoria: {category_name}")
            raise
    
    def get_category_name(self, category_id: int) -> str:
        """
        Obtém o nome de uma categoria pelo ID.
        
        Args:
            category_id: ID da categoria
            
        Returns:
            Nome da categoria
        """
        try:
            # Buscar categoria
            response = requests.get(f"{self.api_url}/categories/{category_id}", auth=self.auth)
            response.raise_for_status()
            
            # Retornar nome
            category = response.json()
            return category['name']
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao buscar nome da categoria: {category_id}")
            raise
    
    def get_tag_name(self, tag_id: int) -> str:
        """
        Obtém o nome de uma tag pelo ID.
        
        Args:
            tag_id: ID da tag
            
        Returns:
            Nome da tag
        """
        try:
            # Buscar tag
            response = requests.get(f"{self.api_url}/tags/{tag_id}", auth=self.auth)
            response.raise_for_status()
            
            # Retornar nome
            tag = response.json()
            return tag['name']
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao buscar nome da tag: {tag_id}")
            raise
    
    def create_post(
        self,
        title: str,
        content: str,
        excerpt: Optional[str] = None,
        status: str = "draft",
        category: Optional[str] = None,
        category_id: Optional[int] = None,
        tags: Optional[List[str]] = None,
        featured_image: Optional[Union[str, Path]] = None
    ) -> Dict:
        """
        Cria um novo post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo do post
            excerpt: Resumo do post
            status: Status do post (draft, publish, private)
            category: Nome da categoria do post
            category_id: ID da categoria do post
            tags: Lista de tags
            featured_image: URL ou caminho da imagem destacada
            
        Returns:
            Dados do post criado
        """
        try:
            # Preparar dados do post
            post_data = {
                'title': title,
                'content': content,
                'excerpt': excerpt or "",
                'status': status,
                'categories': []
            }
            
            # Define a categoria
            if category_id:
                post_data['categories'].append(category_id)
            elif category:
                category_id = self.get_category_id(category)
                post_data['categories'].append(category_id)
            else:
                category_id = self.get_category_id(DEFAULT_CATEGORY)
                post_data['categories'].append(category_id)
            
            # Define as tags
            if tags:
                post_data['tags'] = self._create_tags(tags)
            else:
                post_data['tags'] = self._create_tags(DEFAULT_TAGS)
            
            # Faz upload da imagem destacada
            if featured_image:
                post_data['featured_media'] = self._upload_image(featured_image)
            
            # Publica o post
            response = requests.post(
                f"{self.api_url}/posts",
                auth=self.auth,
                json=post_data
            )
            response.raise_for_status()
            
            # Recupera os dados do post
            post_data = response.json()
            
            self.logger.info(f"Post criado com sucesso: {title}")
            return self._format_post_data(post_data)
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao criar post: {title}")
            raise
    
    def _create_tags(self, tags: List[str]) -> List[int]:
        """
        Cria ou obtém IDs das tags.
        
        Args:
            tags: Lista de nomes de tags
            
        Returns:
            Lista de IDs das tags
        """
        try:
            tag_ids = []
            
            for tag_name in tags:
                # Criar tag
                response = requests.post(
                    f"{self.api_url}/tags",
                    auth=self.auth,
                    json={'name': tag_name}
                )
                
                # Se a tag já existe, usar o ID existente
                if response.status_code == 400:
                    # Buscar tag existente
                    response = requests.get(
                        f"{self.api_url}/tags",
                        auth=self.auth,
                        params={'search': tag_name}
                    )
                    response.raise_for_status()
                    
                    tags = response.json()
                    if tags:
                        tag_ids.append(tags[0]['id'])
                else:
                    response.raise_for_status()
                    tag_ids.append(response.json()['id'])
            
            return tag_ids
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao criar tags: {tags}")
            raise
    
    def _upload_image(self, image_path: Union[str, Path]) -> int:
        """
        Faz upload de uma imagem.
        
        Args:
            image_path: Caminho da imagem
            
        Returns:
            ID da imagem no WordPress
        """
        try:
            # Converter para Path
            image_path = Path(image_path)
            
            # Verificar se o arquivo existe
            if not image_path.exists():
                raise FileNotFoundError(f"Imagem não encontrada: {image_path}")
            
            # Fazer upload
            with open(image_path, 'rb') as img:
                files = {
                    'file': (image_path.name, img, 'image/webp')
                }
                
                response = requests.post(
                    f"{self.api_url}/media",
                    auth=self.auth,
                    files=files
                )
                response.raise_for_status()
            
            return response.json()['id']
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao fazer upload da imagem: {image_path}")
            raise
    
    def _format_post_data(self, post_data: Dict) -> Dict:
        """
        Formata os dados do post.
        
        Args:
            post_data: Dados do post
            
        Returns:
            Dados formatados do post
        """
        data = {
            'id': post_data.get('id'),
            'title': post_data.get('title', {}).get('rendered', ''),
            'content': post_data.get('content', {}).get('rendered', ''),
            'excerpt': post_data.get('excerpt', {}).get('rendered', ''),
            'status': post_data.get('status', ''),
            'date': post_data.get('date'),
            'modified': post_data.get('modified'),
            'slug': post_data.get('slug', ''),
            'link': post_data.get('link', ''),
            'categories': post_data.get('categories', []),
            'tags': post_data.get('tags', []),
            'thumbnail': post_data.get('featured_media')
        }
        
        # Adicionar nomes das categorias e tags
        if data['categories']:
            data['category_name'] = self.get_category_name(data['categories'][0])
        
        if data['tags']:
            data['tag_names'] = [self.get_tag_name(tag_id) for tag_id in data['tags']]
        
        # Remover campos None
        return {k: v for k, v in data.items() if v is not None} 