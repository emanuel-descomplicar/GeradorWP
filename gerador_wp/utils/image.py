"""
Utilitários para manipulação de imagens.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import requests
from io import BytesIO
from typing import Dict, List, Optional, Tuple
from PIL import Image
from .dify import DifyClient
from .exceptions import ImageError

class ImageManager:
    """Classe para gerenciamento de imagens."""
    
    def __init__(self):
        """Inicializa o gerenciador de imagens."""
        self.dify = DifyClient()
        
        # Configurações padrão
        self.width = int(os.getenv('IMAGE_WIDTH', 1920))
        self.height = int(os.getenv('IMAGE_HEIGHT', 1080))
        self.quality = int(os.getenv('IMAGE_QUALITY', 90))
        
    def generate_image(
        self,
        prompt: str,
        width: Optional[int] = None,
        height: Optional[int] = None
    ) -> str:
        """
        Gera uma imagem usando a API do Dify.
        
        Args:
            prompt: Descrição da imagem
            width: Largura da imagem
            height: Altura da imagem
            
        Returns:
            URL da imagem gerada
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Gere uma imagem com as seguintes características:
            
            Descrição: {prompt}
            Dimensões: {width or self.width}x{height or self.height}
            
            A imagem deve ser profissional e adequada para um blog corporativo.
            """
            
            # Gera a imagem
            response = self.dify.generate_image(prompt)
            
            # Retorna a URL
            return response["url"]
            
        except Exception as e:
            raise ImageError(f"Erro ao gerar imagem: {str(e)}")
    
    def optimize_image(
        self,
        image_url: str,
        width: Optional[int] = None,
        height: Optional[int] = None,
        quality: Optional[int] = None
    ) -> BytesIO:
        """
        Otimiza uma imagem para web.
        
        Args:
            image_url: URL da imagem
            width: Nova largura
            height: Nova altura
            quality: Qualidade da compressão
            
        Returns:
            Imagem otimizada em formato BytesIO
        """
        try:
            # Faz download da imagem
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Abre a imagem
            img = Image.open(BytesIO(response.content))
            
            # Redimensiona se necessário
            if width or height:
                img = img.resize(
                    (width or self.width, height or self.height),
                    Image.LANCZOS
                )
            
            # Converte para RGB se necessário
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Salva a imagem otimizada
            output = BytesIO()
            img.save(
                output,
                format='JPEG',
                quality=quality or self.quality,
                optimize=True
            )
            output.seek(0)
            
            return output
            
        except Exception as e:
            raise ImageError(f"Erro ao otimizar imagem: {str(e)}")
    
    def get_image_dimensions(self, image_url: str) -> Tuple[int, int]:
        """
        Obtém as dimensões de uma imagem.
        
        Args:
            image_url: URL da imagem
            
        Returns:
            Tupla com largura e altura
        """
        try:
            # Faz download da imagem
            response = requests.get(image_url)
            response.raise_for_status()
            
            # Abre a imagem
            img = Image.open(BytesIO(response.content))
            
            return img.size
            
        except Exception as e:
            raise ImageError(f"Erro ao obter dimensões da imagem: {str(e)}")
    
    def validate_image(
        self,
        image_url: str,
        min_width: int = 800,
        min_height: int = 600
    ) -> bool:
        """
        Valida se uma imagem atende aos requisitos mínimos.
        
        Args:
            image_url: URL da imagem
            min_width: Largura mínima
            min_height: Altura mínima
            
        Returns:
            True se a imagem é válida
        """
        try:
            # Obtém as dimensões
            width, height = self.get_image_dimensions(image_url)
            
            # Valida as dimensões
            return width >= min_width and height >= min_height
            
        except Exception as e:
            return False 