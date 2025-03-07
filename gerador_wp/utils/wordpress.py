"""
Utilitários para integração com o WordPress.
"""

from typing import Dict, List, Optional, Union
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media, taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client
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
        
        # Inicializa o cliente XML-RPC
        self.client = Client(
            f"{WP_URL}/xmlrpc.php",
            WP_USERNAME,
            WP_APP_PASSWORD
        )
    
    def create_post(
        self,
        title: str,
        content: str,
        excerpt: Optional[str] = None,
        status: str = "draft",
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        featured_image: Optional[str] = None
    ) -> Dict:
        """
        Cria um novo post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo do post
            excerpt: Resumo do post
            status: Status do post (draft, publish, private)
            category: Categoria do post
            tags: Lista de tags
            featured_image: URL da imagem destacada
            
        Returns:
            Dados do post criado
        """
        try:
            # Cria o post
            post = WordPressPost()
            post.title = title
            post.content = content
            post.excerpt = excerpt or ""
            post.post_status = status
            
            # Define a categoria
            if category:
                post.terms_names = {
                    "category": [category]
                }
            else:
                post.terms_names = {
                    "category": [DEFAULT_CATEGORY]
                }
            
            # Define as tags
            if tags:
                post.terms_names["post_tag"] = tags
            else:
                post.terms_names["post_tag"] = DEFAULT_TAGS
            
            # Faz upload da imagem destacada
            if featured_image:
                post.thumbnail = self._upload_image(featured_image)
            
            # Publica o post
            post_id = self.client.call(posts.NewPost(post))
            
            # Recupera os dados do post
            post_data = self.client.call(posts.GetPost(post_id))
            
            self.logger.info(f"Post criado com sucesso: {title}")
            return self._format_post_data(post_data)
            
        except WordPressError as e:
            self.logger.log_error(e, f"Erro ao criar post: {title}")
            raise
    
    def update_post(
        self,
        post_id: int,
        title: Optional[str] = None,
        content: Optional[str] = None,
        excerpt: Optional[str] = None,
        status: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        featured_image: Optional[str] = None
    ) -> Dict:
        """
        Atualiza um post existente.
        
        Args:
            post_id: ID do post
            title: Novo título
            content: Novo conteúdo
            excerpt: Novo resumo
            status: Novo status
            category: Nova categoria
            tags: Novas tags
            featured_image: Nova imagem destacada
            
        Returns:
            Dados do post atualizado
        """
        try:
            # Recupera o post
            post = self.client.call(posts.GetPost(post_id))
            
            # Atualiza os campos
            if title:
                post.title = title
            if content:
                post.content = content
            if excerpt:
                post.excerpt = excerpt
            if status:
                post.post_status = status
            
            # Atualiza a categoria
            if category:
                post.terms_names = {
                    "category": [category]
                }
            
            # Atualiza as tags
            if tags:
                post.terms_names["post_tag"] = tags
            
            # Atualiza a imagem destacada
            if featured_image:
                post.thumbnail = self._upload_image(featured_image)
            
            # Atualiza o post
            self.client.call(posts.EditPost(post_id, post))
            
            # Recupera os dados atualizados
            post_data = self.client.call(posts.GetPost(post_id))
            
            self.logger.info(f"Post atualizado com sucesso: {post.title}")
            return self._format_post_data(post_data)
            
        except WordPressError as e:
            self.logger.log_error(e, f"Erro ao atualizar post: {post_id}")
            raise
    
    def delete_post(self, post_id: int) -> bool:
        """
        Remove um post.
        
        Args:
            post_id: ID do post
            
        Returns:
            True se removido com sucesso
        """
        try:
            self.client.call(posts.DeletePost(post_id))
            self.logger.info(f"Post removido com sucesso: {post_id}")
            return True
            
        except WordPressError as e:
            self.logger.log_error(e, f"Erro ao remover post: {post_id}")
            raise
    
    def _upload_image(self, image_url: str) -> int:
        """
        Faz upload de uma imagem.
        
        Args:
            image_url: URL da imagem
            
        Returns:
            ID da imagem no WordPress
        """
        try:
            # Faz download da imagem
            import requests
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Prepara o upload
            filename = image_url.split("/")[-1]
            data = {
                "name": filename,
                "type": response.headers.get("content-type", "image/jpeg"),
                "bits": xmlrpc_client.Binary(response.content)
            }
            
            # Faz o upload
            response = self.client.call(media.UploadFile(data))
            
            return response["id"]
            
        except Exception as e:
            self.logger.log_error(e, f"Erro ao fazer upload da imagem: {image_url}")
            raise
    
    def _format_post_data(self, post: WordPressPost) -> Dict:
        """
        Formata os dados do post.
        
        Args:
            post: Objeto WordPressPost
            
        Returns:
            Dados formatados do post
        """
        return {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "excerpt": post.excerpt,
            "status": post.post_status,
            "date": post.date,
            "modified": post.modified,
            "slug": post.slug,
            "link": post.link,
            "categories": post.terms_names.get("category", []),
            "tags": post.terms_names.get("post_tag", []),
            "thumbnail": post.thumbnail
        } 