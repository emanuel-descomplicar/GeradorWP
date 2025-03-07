"""
Utilitários para validação de dados.
"""

from typing import Dict, List, Optional, Union
import re
from urllib.parse import urlparse

from .logger import Logger
from ..config.config import (
    MIN_CONTENT_LENGTH,
    MAX_CONTENT_LENGTH
)

class Validator:
    """Classe para validação de dados."""
    
    def __init__(self):
        """Inicializa o validador."""
        self.logger = Logger(__name__)
    
    def validate_url(self, url: str) -> bool:
        """
        Valida uma URL.
        
        Args:
            url: URL a ser validada
            
        Returns:
            True se a URL for válida
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception as e:
            self.logger.log_error(e, f"Erro ao validar URL: {url}")
            return False
    
    def validate_email(self, email: str) -> bool:
        """
        Valida um endereço de e-mail.
        
        Args:
            email: E-mail a ser validado
            
        Returns:
            True se o e-mail for válido
        """
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return bool(re.match(pattern, email))
        except Exception as e:
            self.logger.log_error(e, f"Erro ao validar e-mail: {email}")
            return False
    
    def validate_content_length(
        self,
        content: str,
        min_length: int = MIN_CONTENT_LENGTH,
        max_length: int = MAX_CONTENT_LENGTH
    ) -> bool:
        """
        Valida o comprimento do conteúdo.
        
        Args:
            content: Conteúdo a ser validado
            min_length: Comprimento mínimo
            max_length: Comprimento máximo
            
        Returns:
            True se o comprimento for válido
        """
        try:
            length = len(content)
            return min_length <= length <= max_length
        except Exception as e:
            self.logger.log_error(e, "Erro ao validar comprimento do conteúdo")
            return False
    
    def validate_keywords(
        self,
        keywords: List[str],
        max_keywords: int = 10
    ) -> bool:
        """
        Valida uma lista de palavras-chave.
        
        Args:
            keywords: Lista de palavras-chave
            max_keywords: Número máximo de palavras-chave
            
        Returns:
            True se as palavras-chave forem válidas
        """
        try:
            # Verifica se a lista está vazia
            if not keywords:
                return False
            
            # Verifica o número máximo
            if len(keywords) > max_keywords:
                return False
            
            # Verifica cada palavra-chave
            for keyword in keywords:
                if not keyword or len(keyword) > 50:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao validar palavras-chave")
            return False
    
    def validate_image(
        self,
        image_bytes: bytes,
        max_size: int = 5 * 1024 * 1024,  # 5MB
        allowed_formats: List[str] = ["JPEG", "PNG", "GIF"]
    ) -> bool:
        """
        Valida uma imagem.
        
        Args:
            image_bytes: Bytes da imagem
            max_size: Tamanho máximo em bytes
            allowed_formats: Formatos permitidos
            
        Returns:
            True se a imagem for válida
        """
        try:
            # Verifica o tamanho
            if len(image_bytes) > max_size:
                return False
            
            # Verifica o formato
            from PIL import Image
            image = Image.open(io.BytesIO(image_bytes))
            if image.format not in allowed_formats:
                return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao validar imagem")
            return False
    
    def validate_wordpress_post(
        self,
        post_data: Dict[str, Union[str, List[str], Optional[str]]]
    ) -> bool:
        """
        Valida os dados de um post do WordPress.
        
        Args:
            post_data: Dados do post
            
        Returns:
            True se os dados forem válidos
        """
        try:
            # Verifica campos obrigatórios
            required_fields = ["title", "content"]
            for field in required_fields:
                if field not in post_data or not post_data[field]:
                    return False
            
            # Valida o título
            if not isinstance(post_data["title"], str) or len(post_data["title"]) > 100:
                return False
            
            # Valida o conteúdo
            if not isinstance(post_data["content"], str):
                return False
            if not self.validate_content_length(post_data["content"]):
                return False
            
            # Valida o excerpt se existir
            if "excerpt" in post_data and post_data["excerpt"]:
                if not isinstance(post_data["excerpt"], str):
                    return False
                if len(post_data["excerpt"]) > 160:
                    return False
            
            # Valida as tags se existirem
            if "tags" in post_data and post_data["tags"]:
                if not isinstance(post_data["tags"], list):
                    return False
                if not self.validate_keywords(post_data["tags"]):
                    return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao validar dados do post")
            return False
    
    def validate_dify_response(
        self,
        response: Dict[str, Any]
    ) -> bool:
        """
        Valida uma resposta da API do Dify.
        
        Args:
            response: Resposta da API
            
        Returns:
            True se a resposta for válida
        """
        try:
            # Verifica campos obrigatórios
            required_fields = ["choices"]
            for field in required_fields:
                if field not in response:
                    return False
            
            # Verifica a estrutura das choices
            if not isinstance(response["choices"], list):
                return False
            if not response["choices"]:
                return False
            
            # Verifica cada choice
            for choice in response["choices"]:
                if not isinstance(choice, dict):
                    return False
                if "text" not in choice:
                    return False
            
            return True
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao validar resposta do Dify")
            return False 