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
from typing import Optional, Dict, Any
from PIL import Image, ImageDraw, ImageFont
from ..config.settings import SETTINGS

class ImageGenerator:
    """Gerador de imagens para artigos do WordPress."""
    
    def __init__(self):
        """Inicializa o gerador de imagens."""
        self.logger = logging.getLogger(__name__)
        
        # Configurações de texto
        self.font_size = 65
        self.font_color = (0, 0, 0)
        self.text_max_width = 850
        self.text_position = (100, 500)
        self.line_spacing = 15
        self.max_lines = 5
        
        # Configurar diretórios
        self.base_dir = Path(__file__).parent.parent.parent
        self.templates_dir = self.base_dir / 'src' / 'templates'
        self.cache_dir = SETTINGS['cache']['dir']
        
        # Carregar fonte
        self.fonts_dir = self.base_dir / 'src' / 'fonts'
        self.font_path = self.fonts_dir / 'Montserrat-Bold.ttf'
        self.font = ImageFont.truetype(str(self.font_path), self.font_size)
        
        # Mapeamento de templates
        self.template_files = {
            'Marketing Digital': 'blog-marketing-digital.png',
            'E-commerce': 'blog-e-commerce.png',
            'Gestão de PMEs': 'blog-gestao-pmes.png',
            'Inteligência Artificial': 'blog-inteligencia-artificial.png',
            'Transformação Digital': 'blog-transformacao-digital.png',
            'Vendas': 'blog-vendas.png',
            'Empreendedorismo': 'blog-empreendedorismo.png',
            'Tecnologia': 'blog-tecnologia.png',
            'default': 'blog-marketing-digital.png'  # Template padrão
        }
        
        # Carregar templates
        self.templates = {}
        for category, filename in self.template_files.items():
            template_path = self.templates_dir / filename
            if template_path.exists():
                self.templates[category] = template_path
            else:
                logging.warning(f"Template não encontrado para categoria {category}: {template_path}")
        
        # Garantir que temos pelo menos o template padrão
        if not self.templates:
            raise ValueError("Nenhum template disponível")

    def _wrap_text(self, text: str, draw: ImageDraw) -> list:
        """
        Quebra o texto em linhas que se ajustam à largura máxima.
        
        Args:
            text: Texto a ser quebrado
            draw: Objeto ImageDraw para calcular larguras
            
        Returns:
            Lista de linhas de texto
        """
        # Limitar o título a 800 caracteres
        if len(text) > 800:
            text = text[:797] + "..."
            
        # Dividir o texto em palavras
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            test_line = current_line + [word]
            width = draw.textlength(' '.join(test_line), font=self.font)
            
            if width <= self.text_max_width:
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

    def _calculate_text_position(self, text_lines: list) -> tuple:
        """
        Calcula a posição vertical do texto.
        
        Args:
            text_lines: Lista de linhas de texto
            
        Returns:
            Tupla com posição x, y do texto
        """
        x, _ = self.text_position
        y = 500  # Posição vertical fixa
        self.logger.info(f"Posição vertical: y={y} para {len(text_lines)} linhas")
        return x, y

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
            # Verificar se a categoria tem um template
            if category not in self.templates:
                # Tentar encontrar uma correspondência parcial
                found = False
                for cat in self.templates.keys():
                    if cat.lower() in category.lower() or category.lower() in cat.lower():
                        category = cat
                        self.logger.info(f"Correspondência parcial encontrada: {category}")
                        found = True
                        break
                
                # Se ainda não encontrou, usar o template padrão
                if not found:
                    category = 'default'
                    self.logger.warning(f"Template não encontrado para {category}, usando template padrão")
            
            # Gerar nome do arquivo
            seo_title = title.lower().replace(' ', '-').replace('ã', 'a').replace('ç', 'c')
            if len(seo_title) > 50:
                seo_title = seo_title[:47] + '...'
                
            cache_filename = f"{seo_title}-{category.lower().replace(' ', '-')[:15]}-2025.webp"
            cache_path = self.cache_dir / cache_filename
            
            # Verificar cache
            if cache_path.exists():
                self.logger.info(f"Imagem encontrada no cache: {cache_path}")
                return cache_path
            
            # Carregar template
            template = Image.open(self.templates[category])
            draw = ImageDraw.Draw(template)
            
            # Preparar texto
            text_lines = self._wrap_text(title, draw)
            self.logger.info(f"Linhas de texto: {text_lines}")
            
            # Calcular posição do texto
            x, y = self._calculate_text_position(text_lines)
            
            # Desenhar texto
            for i, line in enumerate(text_lines):
                line_y = y + i * (self.font_size + self.line_spacing)
                draw.text((x, line_y), line, font=self.font, fill=self.font_color)
            
            # Salvar imagem
            template.save(cache_path, 'WEBP', quality=90)
            
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