"""
Gerenciador de imagens e infográficos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageColor
from datetime import datetime

class ImageManager:
    """Gerenciador de imagens e infográficos."""

    def __init__(self):
        """Inicializa o gerenciador de imagens."""
        self.base_dir = Path("/mnt/dados/Cloud/Dev/Scripts/GeradorWP")
        self.templates_dir = self.base_dir / "assets" / "templates" / "infographics"
        self.fonts_dir = self.base_dir / "assets" / "fonts"
        self.icons_dir = self.base_dir / "assets" / "icons"
        self.cache_dir = self.base_dir / "cache" / "images"
        self.logger = logging.getLogger(__name__)
        
        # Criar diretórios se não existirem
        for directory in [self.templates_dir, self.icons_dir, self.cache_dir]:
            directory.mkdir(parents=True, exist_ok=True)
        
        # Configurações de imagem
        self.width = 1200
        self.height = 800
        self.quality = 90
        self.dpi = 300
        
        # Cores
        self.colors = {
            'primary': '#1a73e8',
            'secondary': '#34a853',
            'accent': '#fbbc04',
            'text': '#202124',
            'background': '#ffffff',
            'grid': '#f1f3f4'
        }
        
        # Carregar fontes
        self.fonts = {
            'title': ImageFont.truetype(str(self.fonts_dir / "Montserrat-Bold.ttf"), size=40),
            'subtitle': ImageFont.truetype(str(self.fonts_dir / "Montserrat-SemiBold.ttf"), size=32),
            'heading': ImageFont.truetype(str(self.fonts_dir / "Montserrat-Bold.ttf"), size=28),
            'body': ImageFont.truetype(str(self.fonts_dir / "Montserrat-Regular.ttf"), size=24),
            'caption': ImageFont.truetype(str(self.fonts_dir / "Montserrat-Regular.ttf"), size=18)
        }

    async def generate_infographics(self, topic: str, knowledge: Dict) -> Dict:
        """
        Gera infográficos para o artigo.
        
        Args:
            topic: Tema do artigo
            knowledge: Conhecimento obtido da Dify
            
        Returns:
            Dict com os infográficos gerados
        """
        try:
            # Gerar infográfico de estatísticas
            stats_image = await self._generate_stats_infographic(
                topic,
                knowledge['statistics']
            )
            
            # Gerar infográfico de processo
            process_image = await self._generate_process_infographic(
                topic,
                knowledge['best_practices']
            )
            
            return {
                'stats': stats_image,
                'process': process_image
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar infográficos: {str(e)}")
            raise

    async def _generate_stats_infographic(
        self,
        topic: str,
        statistics: Dict
    ) -> Dict:
        """
        Gera um infográfico com estatísticas em formato dashboard.
        
        Args:
            topic: Tema do artigo
            statistics: Estatísticas a serem exibidas
            
        Returns:
            Dict com informações do infográfico gerado
        """
        try:
            # Criar imagem base com grid
            image = self._create_base_image()
            draw = ImageDraw.Draw(image)
            
            # Desenhar título
            title = f"Panorama: {topic} em Portugal"
            title_width = draw.textlength(title, font=self.fonts['title'])
            draw.text(
                ((self.width - title_width) / 2, 40),
                title,
                font=self.fonts['title'],
                fill=self.colors['text']
            )
            
            # Desenhar grid de estatísticas
            stats_per_row = 3
            margin = 60
            stat_width = (self.width - (margin * (stats_per_row + 1))) / stats_per_row
            stat_height = 200
            current_y = 120
            
            for i, (key, value) in enumerate(statistics.items()):
                row = i // stats_per_row
                col = i % stats_per_row
                x = margin + (col * (stat_width + margin))
                y = current_y + (row * (stat_height + margin))
                
                # Desenhar card de estatística
                self._draw_stat_card(
                    draw,
                    (x, y, x + stat_width, y + stat_height),
                    key,
                    str(value)
                )
            
            # Adicionar fonte e data
            self._add_footer(draw, "Fontes: INE, PORDATA, Eurostat")
            
            # Salvar imagem
            return self._save_infographic(image, f"stats-{topic.lower().replace(' ', '-')}")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar infográfico de estatísticas: {str(e)}")
            raise

    async def _generate_process_infographic(
        self,
        topic: str,
        best_practices: List[Dict]
    ) -> Dict:
        """
        Gera um infográfico com processo/fluxo em formato timeline.
        
        Args:
            topic: Tema do artigo
            best_practices: Melhores práticas a serem exibidas
            
        Returns:
            Dict com informações do infográfico gerado
        """
        try:
            # Criar imagem base
            image = self._create_base_image()
            draw = ImageDraw.Draw(image)
            
            # Desenhar título
            title = f"Como Implementar: {topic}"
            title_width = draw.textlength(title, font=self.fonts['title'])
            draw.text(
                ((self.width - title_width) / 2, 40),
                title,
                font=self.fonts['title'],
                fill=self.colors['text']
            )
            
            # Desenhar timeline
            timeline_start = 120
            step_height = 140
            connector_width = 4
            
            for i, practice in enumerate(best_practices):
                y = timeline_start + (i * step_height)
                
                # Desenhar conector
                if i > 0:
                    draw.rectangle(
                        [40, y - step_height + 30, 40 + connector_width, y + 30],
                        fill=self.colors['primary']
                    )
                
                # Desenhar círculo numerado
                self._draw_numbered_circle(draw, (40, y + 30), i + 1)
                
                # Desenhar conteúdo do passo
                self._draw_process_step(
                    draw,
                    (100, y),
                    practice['title'],
                    practice['description']
                )
            
            # Adicionar footer
            self._add_footer(draw, "© Descomplicar")
            
            # Salvar imagem
            return self._save_infographic(image, f"process-{topic.lower().replace(' ', '-')}")
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar infográfico de processo: {str(e)}")
            raise

    def _create_base_image(self) -> Image:
        """Cria uma imagem base com grid suave."""
        image = Image.new('RGB', (self.width, self.height), color=self.colors['background'])
        draw = ImageDraw.Draw(image)
        
        # Desenhar grid
        grid_spacing = 40
        grid_color = ImageColor.getrgb(self.colors['grid'])
        
        for x in range(0, self.width, grid_spacing):
            draw.line([(x, 0), (x, self.height)], fill=grid_color, width=1)
        
        for y in range(0, self.height, grid_spacing):
            draw.line([(0, y), (self.width, y)], fill=grid_color, width=1)
        
        return image

    def _draw_stat_card(
        self,
        draw: ImageDraw,
        bounds: Tuple[int, int, int, int],
        title: str,
        value: str
    ):
        """Desenha um card de estatística com sombra e gradiente."""
        x1, y1, x2, y2 = bounds
        
        # Desenhar sombra
        shadow_offset = 4
        draw.rectangle(
            [x1 + shadow_offset, y1 + shadow_offset, x2 + shadow_offset, y2 + shadow_offset],
            fill='#00000022'
        )
        
        # Desenhar card
        draw.rectangle(bounds, fill=self.colors['background'])
        
        # Desenhar borda superior colorida
        draw.rectangle(
            [x1, y1, x2, y1 + 4],
            fill=self.colors['primary']
        )
        
        # Desenhar título
        draw.text(
            (x1 + 20, y1 + 20),
            title,
            font=self.fonts['heading'],
            fill=self.colors['text']
        )
        
        # Desenhar valor
        value_width = draw.textlength(value, font=self.fonts['title'])
        draw.text(
            (x1 + ((x2 - x1) - value_width) / 2, y1 + 80),
            value,
            font=self.fonts['title'],
            fill=self.colors['primary']
        )

    def _draw_numbered_circle(
        self,
        draw: ImageDraw,
        center: Tuple[int, int],
        number: int
    ):
        """Desenha um círculo numerado."""
        x, y = center
        radius = 25
        
        # Desenhar círculo
        draw.ellipse(
            [x - radius, y - radius, x + radius, y + radius],
            fill=self.colors['primary']
        )
        
        # Desenhar número
        number_text = str(number)
        number_width = draw.textlength(number_text, font=self.fonts['heading'])
        draw.text(
            (x - number_width/2, y - 15),
            number_text,
            font=self.fonts['heading'],
            fill=self.colors['background']
        )

    def _draw_process_step(
        self,
        draw: ImageDraw,
        position: Tuple[int, int],
        title: str,
        description: str
    ):
        """Desenha um passo do processo."""
        x, y = position
        
        # Desenhar título
        draw.text(
            (x, y),
            title,
            font=self.fonts['subtitle'],
            fill=self.colors['primary']
        )
        
        # Quebrar descrição em linhas
        words = description.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_text = ' '.join(current_line)
            if draw.textlength(line_text, font=self.fonts['body']) > (self.width - x - 100):
                lines.append(' '.join(current_line[:-1]))
                current_line = [word]
        
        if current_line:
            lines.append(' '.join(current_line))
        
        # Desenhar descrição
        for i, line in enumerate(lines):
            draw.text(
                (x, y + 40 + (i * 30)),
                line,
                font=self.fonts['body'],
                fill=self.colors['text']
            )

    def _add_footer(self, draw: ImageDraw, text: str):
        """Adiciona um footer à imagem."""
        footer_text = f"{text} • {datetime.now().strftime('%d/%m/%Y')}"
        footer_width = draw.textlength(footer_text, font=self.fonts['caption'])
        
        draw.text(
            (self.width - footer_width - 20, self.height - 30),
            footer_text,
            font=self.fonts['caption'],
            fill=self.colors['text']
        )

    def _save_infographic(self, image: Image, name: str) -> Dict:
        """Salva o infográfico e retorna suas informações."""
        filename = f"{name}.webp"
        path = self.cache_dir / filename
        
        image.save(
            str(path),
            'WEBP',
            quality=self.quality,
            dpi=(self.dpi, self.dpi)
        )
        
        return {
            'id': hash(str(path)),
            'url': str(path),
            'source': 'Descomplicar'
        }

    def optimize_image(self, image_path: Path) -> Path:
        """
        Otimiza uma imagem para web.
        
        Args:
            image_path: Caminho da imagem a ser otimizada
            
        Returns:
            Path da imagem otimizada
        """
        try:
            # Abrir imagem
            with Image.open(image_path) as img:
                # Redimensionar se necessário
                if img.width > self.width or img.height > self.height:
                    img.thumbnail((self.width, self.height))
                
                # Salvar versão otimizada
                optimized_path = self.cache_dir / f"opt-{image_path.name}"
                img.save(
                    str(optimized_path),
                    'WEBP',
                    quality=self.quality,
                    dpi=(self.dpi, self.dpi)
                )
                
                return optimized_path
                
        except Exception as e:
            self.logger.error(f"Erro ao otimizar imagem: {str(e)}")
            raise 