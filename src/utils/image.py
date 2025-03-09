"""
Gerador de imagens para artigos do WordPress.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any, Tuple
from PIL import Image, ImageDraw, ImageFont
from ..config.settings import SETTINGS

class ImageGenerator:
    """Gerador de imagens para artigos do WordPress."""
    
    def __init__(self):
        """Inicializa o gerador de imagens."""
        self.logger = logging.getLogger(__name__)
        
        # Configurações de texto
        self.title_font_size = 65  # Tamanho exato
        self.font_color = "#000000"  # Preto
        self.text_max_width = 950  # Largura máxima
        self.text_position = (100, 350)  # Margens exatas
        self.line_spacing = 15
        self.max_lines = 3
        
        # Configurar diretórios
        self.base_dir = Path(__file__).parent.parent.parent
        self.templates_dir = self.base_dir / 'assets' / 'templates'
        self.cache_dir = Path(SETTINGS['cache']['dir'])
        
        # Criar diretório de cache se não existir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Carregar fonte
        self.fonts_dir = self.base_dir / 'assets' / 'fonts'
        self.title_font_path = self.fonts_dir / 'Montserrat-Bold.ttf'
        
        # Verificar fonte
        if not self.title_font_path.exists():
            raise FileNotFoundError(f"Fonte não encontrada: {self.title_font_path}")
            
        self.title_font = ImageFont.truetype(str(self.title_font_path), self.title_font_size)
        
        # Templates por categoria
        self.template_files = {
            'Marketing Digital': 'marketing-digital-bg.png',
            'E-commerce': 'ecommerce-bg.png',
            'Gestão de PMEs': 'gestao-pmes-bg.png',
            'Inteligência Artificial': 'ia-bg.png',
            'Transformação Digital': 'transformacao-digital-bg.png',
            'Vendas': 'vendas-bg.png',
            'Empreendedorismo': 'empreendedorismo-bg.png',
            'Tecnologia': 'tecnologia-bg.png',
            'default': 'default-bg.png'
        }

    def _wrap_text(self, text: str, font: ImageFont, max_width: int) -> list:
        """
        Quebra o texto em linhas que se ajustam à largura máxima.
        
        Args:
            text: Texto a ser quebrado
            font: Fonte a ser usada
            max_width: Largura máxima em pixels
            
        Returns:
            Lista de linhas de texto
        """
        # Dividir o texto em palavras
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = current_line + [word]
            width = font.getlength(' '.join(test_line))
            
            if width <= max_width:
                current_line.append(word)
            else:
                if current_line:
                    lines.append(' '.join(current_line))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Limitar ao número máximo de linhas
        if len(lines) > self.max_lines:
            lines = lines[:self.max_lines-1]
            last_line = lines[-1]
            if len(last_line) > 40:
                last_line = last_line[:37] + "..."
            else:
                last_line = last_line + " ..."
            lines[-1] = last_line
            
        self.logger.info(f"Texto quebrado em {len(lines)} linhas: {lines}")
        return lines

    def create_featured_image(self, title: str, category: str) -> Optional[Path]:
        """
        Cria uma imagem destacada para o artigo.
        
        Args:
            title: Título do artigo
            category: Categoria do artigo
            
        Returns:
            Caminho da imagem gerada ou None em caso de erro
        """
        try:
            # Carregar template
            template_file = self.template_files.get(category, self.template_files['default'])
            template_path = self.templates_dir / template_file
            
            if not template_path.exists():
                self.logger.error(f"Template não encontrado: {template_path}")
                return None
            
            # Abrir template
            image = Image.open(template_path)
            draw = ImageDraw.Draw(image)
            
            # Desenhar título
            title_lines = self._wrap_text(title, self.title_font, self.text_max_width)
            title_y = self.text_position[1]
            
            for i, line in enumerate(title_lines):
                line_y = title_y + i * (self.title_font_size + self.line_spacing)
                draw.text(
                    (self.text_position[0], line_y),
                    line,
                    font=self.title_font,
                    fill=self.font_color
                )
            
            # Gerar nome do arquivo
            seo_title = title.lower().replace(' ', '-').replace('ã', 'a').replace('ç', 'c')
            if len(seo_title) > 50:
                seo_title = seo_title[:47] + '...'
                
            cache_filename = f"{seo_title}.webp"
            cache_path = self.cache_dir / cache_filename
            
            # Salvar imagem com alta qualidade
            image.save(cache_path, 'WEBP', quality=95, method=6)
            
            # Verificar tamanho
            size_kb = cache_path.stat().st_size / 1024
            self.logger.info(f"✓ Imagem gerada com sucesso: {cache_path}")
            self.logger.info(f"Nome SEO: {cache_path.name}")
            self.logger.info(f"Caminho absoluto: {cache_path.absolute()}")
            self.logger.info(f"Tamanho: {size_kb:.2f} KB")
            
            return cache_path
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar imagem: {str(e)}")
            return None

    async def generate_image(self, prompt: str, title: str = None, section: str = None) -> Optional[Dict[str, Any]]:
        """
        Gera uma imagem com base no prompt fornecido.
        
        Args:
            prompt: Descrição da imagem a ser gerada
            title: Título do artigo (opcional)
            section: Seção do artigo (opcional)
            
        Returns:
            Dicionário com informações da imagem gerada ou None em caso de erro
        """
        try:
            self.logger.info(f"Gerando imagem para prompt: {prompt}")
            
            # Simulação de geração de imagem
            # Em uma implementação real, aqui seria feita uma chamada à API de geração de imagens
            
            return {
                "url": "https://via.placeholder.com/800x450?text=Imagem+Gerada",
                "alt_text": prompt,
                "width": 800,
                "height": 450,
                "prompt": prompt
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar imagem: {str(e)}")
            return None 