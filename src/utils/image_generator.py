#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de imagens para artigos do blog.
Usa templates existentes e adiciona texto.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import re
from PIL import Image, ImageDraw, ImageFont
import logging
from pathlib import Path

# Especificações de Design da Descomplicar
TITLE_FONT_SIZE = 70  # Montserrat Bold
SUBTITLE_FONT_SIZE = 50  # Montserrat Italic
TITLE_MARGIN_TOP = 400  # pixels do topo
TITLE_MARGIN_LEFT = 100  # pixels da esquerda
TITLE_MAX_WIDTH = 900  # largura máxima do texto
TITLE_LINE_SPACING = 15  # espaçamento entre linhas
SUBTITLE_LINE_SPACING = 20  # espaçamento extra para subtítulo
TITLE_COLOR = "#333333"  # cinza escuro
OUTPUT_QUALITY = 90  # qualidade da imagem WebP
OUTPUT_METHOD = 6  # método de compressão WebP

# Mapeamento de categorias para templates
TEMPLATE_MAPPING = {
    "blog-e-commerce": "ecommerce-bg.png",
    "blog-empreendedorismo": "empreendedorismo-bg.png",
    "blog-gestao-pmes": "gestao-pmes-bg.png",
    "blog-inteligencia-artificial": "ia-bg.png",
    "blog-marketing-digital": "marketing-digital-bg.png",
    "blog-tecnologia": "tecnologia-bg.png",
    "blog-transformacao-digital": "transformacao-digital-bg.png",
    "blog-vendas": "vendas-bg.png",
    "default": "default-bg.png"
}

class ImageGenerator:
    def __init__(self):
        self.templates_dir = "assets/templates"
        self.output_dir = "output/images"
        self.fonts_dir = "assets/fonts"
        
        # Criar diretórios necessários
        for directory in [self.templates_dir, self.output_dir, self.fonts_dir]:
            os.makedirs(directory, exist_ok=True)
            
        # Configurar fontes
        self.title_font = ImageFont.truetype(f"{self.fonts_dir}/Montserrat-Bold.ttf", TITLE_FONT_SIZE)
        self.subtitle_font = ImageFont.truetype(f"{self.fonts_dir}/Montserrat-Italic.ttf", SUBTITLE_FONT_SIZE)
        
    def process_title(self, title: str) -> tuple:
        """
        Processa o título para remover anos e estruturar no formato desejado.
        
        Args:
            title: Título original do artigo
            
        Returns:
            Tupla com (título principal, subtítulo)
        """
        # Remover anos (4 dígitos começando com 19 ou 20)
        title = re.sub(r'\b(19|20)\d{2}\b', '', title)
        
        # Remover espaços extras
        title = ' '.join(title.split())
        
        # Se não tiver dois pontos, retornar como título principal apenas
        if ':' not in title:
            return title, None
            
        # Separar em título principal e subtítulo
        main_title, subtitle = title.split(':', 1)
        
        # Garantir que ambas as partes começam com maiúscula
        main_title = main_title.strip()
        subtitle = subtitle.strip()
        
        if subtitle:
            # Se o subtítulo não começar com artigo/preposição, capitalizar
            subtitle_words = subtitle.split()
            ignore_words = ['o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 
                          'de', 'do', 'da', 'dos', 'das', 'em', 'no', 'na', 
                          'nos', 'nas', 'por', 'para']
            
            if subtitle_words[0].lower() not in ignore_words:
                subtitle = subtitle.capitalize()
            
            return main_title, subtitle
            
        return main_title, None
        
    def create_featured_image(self, title: str, category: str) -> str:
        """
        Cria uma imagem destacada usando o template da categoria.
        
        Args:
            title: Título do artigo
            category: Categoria do artigo (slug)
            
        Returns:
            Caminho para a imagem gerada
        """
        try:
            # Processar título
            main_title, subtitle = self.process_title(title)
            
            # Carregar template
            template_name = TEMPLATE_MAPPING.get(category, TEMPLATE_MAPPING["default"])
            template_path = os.path.join(self.templates_dir, template_name)
            
            if not os.path.exists(template_path):
                print(f"✗ Template não encontrado: {template_path}")
                return None
                
            img = Image.open(template_path)
            draw = ImageDraw.Draw(img)
            
            # Quebrar título principal em linhas
            title_lines = []
            words = main_title.split()
            current_line = []
            
            for word in words:
                test_line = " ".join(current_line + [word])
                width = self.title_font.getlength(test_line)
                
                if width <= TITLE_MAX_WIDTH:
                    current_line.append(word)
                else:
                    title_lines.append(" ".join(current_line))
                    current_line = [word]
            
            if current_line:
                title_lines.append(" ".join(current_line))
            
            # Quebrar subtítulo em linhas se existir
            subtitle_lines = []
            if subtitle:
                words = subtitle.split()
                current_line = []
                
                for word in words:
                    test_line = " ".join(current_line + [word])
                    width = self.subtitle_font.getlength(test_line)
                    
                    if width <= TITLE_MAX_WIDTH:
                        current_line.append(word)
                    else:
                        subtitle_lines.append(" ".join(current_line))
                        current_line = [word]
                
                if current_line:
                    subtitle_lines.append(" ".join(current_line))
            
            # Desenhar título principal
            y_pos = TITLE_MARGIN_TOP
            for line in title_lines:
                draw.text((TITLE_MARGIN_LEFT, y_pos), line, 
                         font=self.title_font, fill=TITLE_COLOR)
                y_pos += self.title_font.size + TITLE_LINE_SPACING
            
            # Adicionar espaço extra antes do subtítulo
            if subtitle_lines:
                y_pos += SUBTITLE_LINE_SPACING
                
                # Desenhar subtítulo
                for line in subtitle_lines:
                    draw.text((TITLE_MARGIN_LEFT, y_pos), line, 
                             font=self.subtitle_font, fill=TITLE_COLOR)
                    y_pos += self.subtitle_font.size + TITLE_LINE_SPACING
            
            # Gerar nome do arquivo
            safe_title = "".join(c if c.isalnum() else "-" for c in main_title.lower())
            output_path = f"{self.output_dir}/{category}_{safe_title[:50]}.webp"
            
            # Salvar imagem
            img.save(output_path, "WEBP", quality=OUTPUT_QUALITY, method=OUTPUT_METHOD)
            print(f"✓ Imagem gerada: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"✗ Erro ao gerar imagem: {str(e)}")
            return None

if __name__ == "__main__":
    generator = ImageGenerator()
    
    # Testar com diferentes formatos de título
    titles = [
        "Como Criar SEO: Guia Completo",
        "Como Investir em Anúncios: 7 Passos Práticos",
        "Inteligência Artificial no Marketing: Tudo o que Precisa de Saber",
        "Marketing Digital em 2024: Tendências e Estratégias",  # Ano será removido
        "Estratégias de Vendas"  # Sem subtítulo
    ]
    
    for title in titles:
        generator.create_featured_image(title, "blog-marketing-digital") 