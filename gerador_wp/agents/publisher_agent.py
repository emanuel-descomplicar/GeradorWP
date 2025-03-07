"""
PublisherAgent - Responsável por publicar o conteúdo no WordPress.
"""

from typing import Dict, List, Optional
from crewai import Agent
from langchain.tools import Tool
import requests
import json
import os
from datetime import datetime
import hashlib
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods import posts, media, taxonomies
from wordpress_xmlrpc.compat import xmlrpc_client

from ..config.config import (
    DIFY_API_KEY,
    DIFY_API_URL,
    WP_URL,
    WP_USERNAME,
    WP_PASSWORD,
    WP_APP_PASSWORD,
    CACHE_TTL,
    CACHE_DIR,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY
)
from ..utils.cache import Cache
from ..utils.logger import Logger
from ..utils.http import HttpClient
from ..utils.dify import DifyClient
from ..utils.wordpress import WordPressClient
from ..utils.image import ImageManager
from ..utils.exceptions import PublishingError

class PublisherAgent:
    """Agente responsável por publicar o conteúdo no WordPress."""
    
    def __init__(self):
        """Inicializa o PublisherAgent."""
        self.logger = Logger(__name__)
        self.cache = Cache()
        self.http = HttpClient()
        self.dify = DifyClient()
        self.wp = WordPressClient()
        self.image = ImageManager()
        
        self.agent = Agent(
            role='Publicador de Conteúdo',
            goal='Publicar conteúdo no WordPress de forma otimizada',
            backstory="""Você é um especialista em publicação de conteúdo no WordPress.
            Sua função é garantir que o conteúdo seja publicado corretamente, com todas
            as otimizações necessárias e metadados apropriados.""",
            verbose=True,
            allow_delegation=False,
            tools=self._get_tools(),
            llm_config={
                "config_list": [{
                    "model": "dify",
                    "api_key": DIFY_API_KEY,
                    "api_base": DIFY_API_URL
                }]
            }
        )
        
        # Cria o diretório de cache se não existir
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
    
    def _get_tools(self) -> List[Tool]:
        """Retorna a lista de ferramentas disponíveis para o agente."""
        return [
            Tool(
                name="format_content",
                func=self._format_content,
                description="Formata o conteúdo para publicação no WordPress"
            ),
            Tool(
                name="upload_media",
                func=self._upload_media,
                description="Faz upload de imagens e outros arquivos de mídia"
            ),
            Tool(
                name="publish_post",
                func=self._publish_post,
                description="Publica o artigo no WordPress"
            )
        ]
    
    def _format_content(self, content: Dict) -> Dict:
        """
        Formata o conteúdo para publicação no WordPress.
        
        Args:
            content: Conteúdo a ser formatado
            
        Returns:
            Dict com o conteúdo formatado
        """
        try:
            # Gera chave de cache
            cache_key = f"format_content_{hashlib.md5(json.dumps(content).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para formatação de conteúdo")
                return cached_result
            
            # Prepara o prompt
            prompt = f"""
            Formate o seguinte conteúdo para publicação no WordPress:
            
            Conteúdo:
            {json.dumps(content, indent=2)}
            
            Retorne o conteúdo formatado como um objeto JSON com:
            - post_title: Título do post
            - post_content: Conteúdo em HTML
            - post_excerpt: Resumo do post
            - post_status: Status (draft/publish)
            - post_type: Tipo (post)
            - comment_status: Status dos comentários (open/closed)
            - ping_status: Status dos pings (open/closed)
            - meta_input: Metadados personalizados
            """
            
            # Faz a formatação
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Processa o resultado
            result = json.loads(response["choices"][0]["text"])
            
            # Armazena no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao formatar conteúdo")
            raise PublishingError(f"Erro ao formatar conteúdo: {str(e)}")
    
    def _upload_media(self, media_data: Dict) -> Dict:
        """
        Faz upload de imagens e outros arquivos de mídia.
        
        Args:
            media_data: Dados da mídia para upload
            
        Returns:
            Dict com os dados da mídia após upload
        """
        try:
            # Gera chave de cache
            cache_key = f"upload_media_{hashlib.md5(json.dumps(media_data).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para upload de mídia")
                return cached_result
            
            # Processa cada imagem
            result = {}
            for key, url in media_data.items():
                # Faz download da imagem
                image_bytes = self.image.download_image(url)
                
                # Otimiza a imagem
                if image_bytes:
                    image_bytes = self.image.optimize_image(image_bytes)
                    
                    # Faz upload para o WordPress
                    attachment_id = self.wp._upload_image(url)
                    
                    # Armazena o resultado
                    result[key] = {
                        "url": url,
                        "attachment_id": attachment_id
                    }
            
            # Armazena no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao fazer upload de mídia")
            raise PublishingError(f"Erro ao fazer upload de mídia: {str(e)}")
    
    def _publish_post(self, post_data: Dict) -> Dict:
        """
        Publica o artigo no WordPress.
        
        Args:
            post_data: Dados do artigo para publicação
            
        Returns:
            Dict com os dados do artigo após publicação
        """
        try:
            # Gera chave de cache
            cache_key = f"publish_post_{hashlib.md5(json.dumps(post_data).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para publicação de post")
                return cached_result
            
            # Cria o post
            result = self.wp.create_post(
                title=post_data["post_title"],
                content=post_data["post_content"],
                excerpt=post_data.get("post_excerpt", ""),
                status=post_data.get("post_status", "draft"),
                category=post_data.get("category", None),
                tags=post_data.get("tags", None),
                featured_image=post_data.get("featured_image", None)
            )
            
            # Armazena no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao publicar post")
            raise PublishingError(f"Erro ao publicar post: {str(e)}")
    
    def publish(self, content: Dict, media_files: List[str]) -> Dict:
        """
        Publica o conteúdo completo no WordPress.
        
        Args:
            content: Conteúdo do artigo
            media_files: Lista de arquivos de mídia
            
        Returns:
            Dict com os dados da publicação
        """
        try:
            self.logger.info("Iniciando publicação de conteúdo")
            
            # Formata o conteúdo
            formatted_content = self._format_content(content)
            
            # Processa arquivos de mídia
            if media_files:
                media_data = {
                    f"media_{i}": url
                    for i, url in enumerate(media_files)
                }
                media_result = self._upload_media(media_data)
                
                # Adiciona IDs das imagens ao conteúdo
                if "featured_image" in media_result:
                    formatted_content["featured_image"] = media_result["featured_image"]["attachment_id"]
            
            # Publica o post
            result = self._publish_post(formatted_content)
            
            # Adiciona metadados
            result.update({
                "timestamp": datetime.now().isoformat(),
                "media_files": media_files,
                "status": "success"
            })
            
            self.logger.info("Conteúdo publicado com sucesso")
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao publicar conteúdo")
            raise PublishingError(f"Erro ao publicar conteúdo: {str(e)}") 