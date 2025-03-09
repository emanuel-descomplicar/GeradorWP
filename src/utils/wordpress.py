"""
WordPress - Cliente WordPress para integração com o CMS

Este módulo fornece uma classe para interagir com o WordPress via XML-RPC,
incluindo publicação de conteúdo, upload de imagens e mais.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
from typing import Dict, List, Any, Optional, Tuple, BinaryIO
from urllib.parse import urlparse
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost, methods
from wordpress_xmlrpc.methods import posts, media
from wordpress_xmlrpc.compat import xmlrpc_client

class WordPress:
    """
    Cliente WordPress para interação com o CMS via XML-RPC.
    
    Esta classe fornece métodos para realizar operações comuns no WordPress,
    como publicar artigos, fazer upload de imagens, e mais.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Inicializa o cliente WordPress.
        
        Args:
            config: Configurações opcionais para o cliente (url, username, password)
        """
        self.logger = logging.getLogger(__name__)
        self.config = config or {}
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Configurações do WordPress
        self.wp_url = self.config.get("wp_url") or os.getenv("WP_URL")
        self.wp_username = self.config.get("wp_username") or os.getenv("WP_USERNAME")
        self.wp_password = self.config.get("wp_password") or os.getenv("WP_PASSWORD") or os.getenv("WP_APP_PASSWORD")
        
        if not all([self.wp_url, self.wp_username, self.wp_password]):
            self.logger.error("Configurações do WordPress incompletas. Verifique as variáveis de ambiente.")
            raise ValueError("Configurações do WordPress incompletas")
        
        # Preparar URL do XML-RPC
        parsed_url = urlparse(self.wp_url)
        self.xmlrpc_url = f"{parsed_url.scheme}://{parsed_url.netloc}/xmlrpc.php"
        
        # Inicializar cliente
        try:
            self.client = Client(self.xmlrpc_url, self.wp_username, self.wp_password)
            self.logger.info(f"Cliente WordPress inicializado para {self.wp_url}")
        except Exception as e:
            self.logger.error(f"Erro ao inicializar cliente WordPress: {str(e)}")
            raise
    
    def publish_post(self, title: str, content: str, excerpt: str = "", 
                    categories: List[str] = None, tags: List[str] = None, 
                    featured_image_id: int = None, status: str = "draft",
                    meta: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Publica um post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo HTML do post
            excerpt: Resumo do post
            categories: Lista de categorias (nomes)
            tags: Lista de tags
            featured_image_id: ID da imagem destacada
            status: Status do post (draft, publish, etc.)
            meta: Metadados personalizados
            
        Returns:
            Um dicionário com o resultado da publicação
        """
        self.logger.info(f"Publicando post: {title}")
        
        try:
            # Criar objeto post
            post = WordPressPost()
            post.title = title
            post.content = content
            post.excerpt = excerpt
            post.terms_names = {
                'category': categories or [],
                'post_tag': tags or []
            }
            post.post_status = status
            
            # Adicionar imagem destacada se fornecida
            if featured_image_id:
                post.thumbnail = featured_image_id
            
            # Adicionar metadados se fornecidos
            if meta:
                post.custom_fields = []
                for key, value in meta.items():
                    post.custom_fields.append({
                        'key': key,
                        'value': value
                    })
            
            # Publicar post
            post_id = self.client.call(posts.NewPost(post))
            
            # Obter URL do post
            post_data = self.client.call(posts.GetPost(post_id))
            
            result = {
                "id": post_id,
                "title": title,
                "status": status,
                "link": getattr(post_data, "link", None)
            }
            
            self.logger.info(f"Post publicado com sucesso. ID: {post_id}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao publicar post: {str(e)}")
            return {"error": str(e)}
    
    def upload_image(self, image_path: str, alt_text: str = "", title: str = None) -> Dict[str, Any]:
        """
        Faz upload de uma imagem para a biblioteca de mídia do WordPress.
        
        Args:
            image_path: Caminho local para a imagem
            alt_text: Texto alternativo da imagem
            title: Título da imagem (se None, usa o nome do arquivo)
            
        Returns:
            Um dicionário com o resultado do upload
        """
        self.logger.info(f"Fazendo upload da imagem: {image_path}")
        
        try:
            # Verificar se o arquivo existe
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Arquivo não encontrado: {image_path}")
            
            # Determinar tipo de imagem
            filename = os.path.basename(image_path)
            title = title or os.path.splitext(filename)[0]
            
            # Preparar dados para upload
            with open(image_path, "rb") as img:
                data = {
                    "name": filename,
                    "type": self._get_mimetype(filename),
                    "bits": xmlrpc_client.Binary(img.read()),
                    "caption": alt_text,
                    "title": title,
                    "alt": alt_text
                }
            
            # Fazer upload
            response = self.client.call(media.UploadFile(data))
            
            result = {
                "id": response["id"],
                "title": title,
                "url": response["url"],
                "alt_text": alt_text
            }
            
            self.logger.info(f"Imagem enviada com sucesso. ID: {response['id']}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao fazer upload da imagem: {str(e)}")
            return {"error": str(e)}
    
    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de categorias disponíveis no WordPress.
        
        Returns:
            Uma lista de dicionários com informações sobre as categorias
        """
        self.logger.info("Obtendo lista de categorias")
        
        try:
            categories = self.client.call(methods.taxonomies.GetTerms('category'))
            
            result = [
                {
                    "id": cat.id,
                    "name": cat.name,
                    "slug": cat.slug,
                    "description": cat.description,
                    "parent": cat.parent
                }
                for cat in categories
            ]
            
            self.logger.info(f"Obtidas {len(result)} categorias")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao obter categorias: {str(e)}")
            return []
    
    def get_post(self, post_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém informações de um post específico.
        
        Args:
            post_id: ID do post
            
        Returns:
            Um dicionário com as informações do post ou None se não encontrado
        """
        self.logger.info(f"Obtendo informações do post ID: {post_id}")
        
        try:
            post = self.client.call(posts.GetPost(post_id))
            
            result = {
                "id": post.id,
                "title": post.title,
                "status": post.post_status,
                "link": post.link,
                "date": post.date,
                "modified": post.modified
            }
            
            self.logger.info(f"Post obtido com sucesso: {post.title}")
            return result
            
        except Exception as e:
            self.logger.error(f"Erro ao obter post {post_id}: {str(e)}")
            return None
    
    def _get_mimetype(self, filename: str) -> str:
        """
        Determina o mimetype de um arquivo baseado em sua extensão.
        
        Args:
            filename: Nome do arquivo
            
        Returns:
            O mimetype correspondente
        """
        ext = os.path.splitext(filename)[1].lower()
        
        mimetypes = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp',
            '.svg': 'image/svg+xml',
            '.pdf': 'application/pdf'
        }
        
        return mimetypes.get(ext, 'application/octet-stream') 