#!/usr/bin/env python3
"""
Cliente WordPress para publicação de artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
import xmlrpc.client
from typing import Dict, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost, EditPost, GetPost
from wordpress_xmlrpc.methods.media import UploadFile

# Carrega variáveis de ambiente
load_dotenv()

class WordPressClient:
    """Cliente para publicação de artigos no WordPress."""
    
    def __init__(self):
        """Inicializa o cliente WordPress."""
        self.wp_url = os.getenv("WP_URL", "")
        self.wp_username = os.getenv("WP_USERNAME", "")
        self.wp_password = os.getenv("WP_PASSWORD", "")
        
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
    
    def publish_article(self, 
                        title: str, 
                        content: str, 
                        category: str, 
                        featured_image: Optional[Dict[str, Any]] = None,
                        status: str = 'publish') -> Dict[str, Any]:
        """
        Publica um artigo no WordPress.
        
        Args:
            title (str): Título do artigo.
            content (str): Conteúdo HTML do artigo.
            category (str): Categoria do artigo.
            featured_image (Optional[Dict[str, Any]], optional): Dados da imagem destacada. Defaults to None.
            status (str, optional): Status da publicação ('draft', 'publish', etc.). Defaults to 'publish'.
            
        Returns:
            Dict[str, Any]: Dados do artigo publicado, incluindo ID e URL.
        """
        if self.simulation_mode:
            logging.info(f"Simulação: Artigo '{title}' seria publicado na categoria '{category}'")
            logging.info(f"Conteúdo do artigo (primeiros 100 caracteres): {content[:100]}...")
            
            # Simulando publicação bem-sucedida
            return {
                "id": 12345,
                "url": f"https://example.com/simulated-post/{title.lower().replace(' ', '-')}",
                "status": status
            }
        
        # Criar post
        post = WordPressPost()
        post.title = title
        post.content = content
        post.terms_names = {
            'category': [category]
        }
        post.post_status = status
        
        # Adicionar imagem destacada, se disponível
        if featured_image and featured_image.get('id'):
            post.thumbnail = featured_image.get('id')
        
        try:
            # Publicar o post
            post_id = self.client.call(NewPost(post))
            
            # Obter detalhes do post publicado
            published_post = self.client.call(GetPost(post_id))
            
            logging.info(f"Artigo publicado com sucesso. ID: {post_id}, URL: {published_post.link}")
            
            return {
                "id": post_id,
                "url": published_post.link,
                "status": status
            }
        except Exception as e:
            logging.error(f"Erro ao publicar artigo: {str(e)}")
            return {
                "id": 0,
                "url": "",
                "status": "error"
            } 