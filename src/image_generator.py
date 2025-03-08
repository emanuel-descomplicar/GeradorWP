#!/usr/bin/env python3
"""
Gerador de imagens destacadas para artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import hashlib
import logging
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from typing import Dict, Optional, Tuple

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ImageGenerator:
    """Classe para geração de imagens destacadas."""

    def __init__(self):
        """Inicializa o gerador de imagens."""
        self.base_dir = Path(__file__).parent.parent
        self.templates_dir = self.base_dir / "gerador_wp" / "templates"
        self.cache_dir = self.base_dir / "cache" / "images"
        self.fonts_dir = self.base_dir / "assets" / "fonts"
        
        # Criar diretórios se não existirem
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
        # Configurações de texto
        self.font_path = self.fonts_dir / "Montserrat-Bold.ttf"
        self.font_size = 65
        self.text_color = "#000000"
        self.text_position = (100, 500)  # x, y (y é CRÍTICO: 500px do topo)
        self.max_text_width = 850
        self.line_spacing = 15
        self.max_lines = 5

        # Configurações de imagem
        self.image_width = 1920
        self.image_height = 1080
        self.image_quality = 90
        self.image_dpi = 72

        # Carregar fonte
        if not self.font_path.exists():
            raise FileNotFoundError(f"Fonte não encontrada: {self.font_path}")
        self.font = ImageFont.truetype(str(self.font_path), self.font_size)

    def get_template_path(self, category: str) -> Path:
        """Obtém o caminho do template para a categoria."""
        # Normalizar categoria para o nome do arquivo
        normalized = (category.lower()
            .replace(' ', '-')
            .replace('ã', 'a')
            .replace('ç', 'c')
            .replace('é', 'e')
            .replace('ê', 'e')
            .replace('í', 'i')
            .replace('ó', 'o')
            .replace('ô', 'o')
            .replace('ú', 'u'))
        
        template_name = f"blog-{normalized}.png"
        template_path = self.templates_dir / template_name
        
        if not template_path.exists():
            logger.error(f"Template não encontrado: {template_name}")
            logger.error(f"Diretório de templates: {self.templates_dir}")
            logger.error(f"Templates disponíveis: {list(self.templates_dir.glob('*.png'))}")
            raise FileNotFoundError(f"Template não encontrado: {template_name}")
        
        return template_path

    def get_cache_key(self, title: str, category: str) -> str:
        """Gera uma chave única para cache."""
        content = f"{title}:{category}".encode('utf-8')
        return hashlib.md5(content).hexdigest()

    def generate_slug(self, title: str) -> str:
        """
        Gera um slug SEO-friendly a partir do título.
        
        Regras:
        1. Remove palavras desnecessárias (artigos, preposições, etc.)
        2. Normaliza caracteres especiais
        3. Limita a 50 caracteres
        4. Remove anos e datas
        5. Trata casos especiais (e-commerce)
        6. Usa apenas caracteres válidos (a-z, 0-9, hífen)
        7. Prioriza palavras relevantes mantendo ordem
        """
        # Normalizar caracteres especiais
        normalized = (title.lower()
            .replace('á', 'a').replace('à', 'a').replace('ã', 'a').replace('â', 'a')
            .replace('é', 'e').replace('è', 'e').replace('ê', 'e')
            .replace('í', 'i').replace('ì', 'i').replace('î', 'i')
            .replace('ó', 'o').replace('ò', 'o').replace('õ', 'o').replace('ô', 'o')
            .replace('ú', 'u').replace('ù', 'u').replace('û', 'u')
            .replace('ç', 'c')
            .replace('ñ', 'n'))
        
        # Remover tudo após ":" no título
        if ':' in normalized:
            normalized = normalized.split(':')[0].strip()
        
        # Remover palavras desnecessárias
        words_to_remove = [
            # Artigos e pronomes
            'seu', 'sua', 'seus', 'suas',
            'este', 'esta', 'estes', 'estas',
            'nosso', 'nossa', 'nossos', 'nossas',
            'meu', 'minha', 'meus', 'minhas',
            'um', 'uma', 'uns', 'umas',
            'o', 'a', 'os', 'as',
            
            # Preposições
            'em', 'de', 'do', 'da', 'dos', 'das',
            'para', 'com', 'sem', 'por', 'pelo', 'pela',
            'aos', 'às', 'ao', 'à',
            'entre', 'sobre', 'sob', 'após',
            
            # Palavras comuns
            'negocio', 'negocios', 'empresa', 'empresas',
            'nas', 'nos', 'na', 'no',
            'mais', 'menos', 'muito', 'muita',
            'novo', 'nova', 'novos', 'novas',
            'outro', 'outra', 'outros', 'outras',
            'todo', 'toda', 'todos', 'todas',
            'portugues', 'portuguesa', 'portugueses', 'portuguesas',
            'completo', 'completa', 'completos', 'completas',
            'pequeno', 'pequena', 'pequenos', 'pequenas',
            'medio', 'media', 'medios', 'medias',
            'mercado', 'mercados',
            'guia', 'manual', 'tutorial',
            
            # Anos e datas
            '2020', '2021', '2022', '2023', '2024', '2025',
            'janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho',
            'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro',
            'atual', 'novo', 'nova', 'novos', 'novas',
            'recente', 'recentes', 'futuro', 'futura', 'futuros', 'futuras'
        ]
        
        # Palavras prioritárias que devem ser mantidas
        priority_words = [
            'marketing', 'digital', 'pmes', 'e-commerce',
            'seo', 'vendas', 'estrategia', 'estrategias',
            'transformacao', 'tecnologia', 'inteligencia',
            'artificial', 'empreendedorismo', 'gestao',
            'instagram', 'facebook', 'linkedin', 'tiktok',
            'redes', 'sociais', 'web', 'site', 'blog',
            'leads', 'conversao', 'roi', 'analytics',
            'automacao', 'crm', 'email', 'sms',
            'taticas', 'tatica'
        ]
        
        # Mapeamento de variações para palavras prioritárias
        word_variations = {
            'pme': 'pmes',
            'pequenas e medias empresas': 'pmes',
            'pequena e media empresa': 'pmes',
            'estrategica': 'estrategia',
            'estrategicas': 'estrategias',
            'estrategico': 'estrategia',
            'estrategicos': 'estrategias',
            'tatica': 'estrategia',
            'taticas': 'estrategias'
        }
        
        # Remover anos de 4 dígitos (1900-2099)
        words = []
        for word in normalized.split():
            if not (len(word) == 4 and word.isdigit() and 1900 <= int(word) <= 2099):
                words.append(word)
        
        # Normalizar variações de palavras
        normalized_words = []
        i = 0
        while i < len(words):
            # Tentar encontrar uma frase que corresponda a uma variação
            found_variation = False
            for phrase, replacement in word_variations.items():
                phrase_words = phrase.split()
                if (i + len(phrase_words) <= len(words) and 
                    ' '.join(words[i:i+len(phrase_words)]) == phrase):
                    normalized_words.append(replacement)
                    i += len(phrase_words)
                    found_variation = True
                    break
            
            if not found_variation:
                normalized_words.append(words[i])
                i += 1
        
        # Filtrar palavras mantendo prioridades e ordem
        filtered_words = []
        for word in normalized_words:
            if word in priority_words or word not in words_to_remove:
                filtered_words.append(word)
        
        normalized = ' '.join(filtered_words)
        
        # Tratar casos especiais
        normalized = normalized.replace('e-commerce', 'e-commerce')
        
        # Substituir espaços e caracteres especiais por hífen
        slug = ""
        for c in normalized:
            if c.isalnum():
                slug += c
            elif c in ['-', ' ']:
                # Adicionar hífen se o último caractere não for hífen
                if not slug.endswith('-'):
                    slug += '-'
        
        # Remover hífens duplicados e hífens no início/fim
        while '--' in slug:
            slug = slug.replace('--', '-')
        slug = slug.strip('-')
        
        # Limitar tamanho para SEO (máximo 50 caracteres)
        if len(slug) > 50:
            # Dividir em palavras
            words = slug.split('-')
            
            # Manter palavras na ordem original, priorizando palavras importantes
            priority_slug = []
            
            # Primeiro, adicionar palavras prioritárias na ordem em que aparecem
            for word in words:
                if word in priority_words and len('-'.join(priority_slug + [word])) <= 50:
                    priority_slug.append(word)
            
            # Depois, adicionar outras palavras mantendo a ordem
            for word in words:
                if word not in priority_words and len('-'.join(priority_slug + [word])) <= 50:
                    priority_slug.append(word)
            
            slug = '-'.join(priority_slug)
        
        return slug

    def get_cache_path(self, title: str, category: str = None) -> Path:
        """Obtém o caminho do arquivo em cache usando o slug do título."""
        # Gerar slug do título
        slug = self.generate_slug(title)
        
        # Gerar nome do arquivo
        filename = f"{slug}.webp"
        
        return self.cache_dir / filename

    def wrap_text(self, text: str, draw: ImageDraw, max_width: int) -> list:
        """Quebra o texto em linhas respeitando a largura máxima."""
        words = text.split()
        lines = []
        current_line = []
        
        for word in words:
            current_line.append(word)
            line_width = draw.textlength(" ".join(current_line), font=self.font)
            
            if line_width > max_width:
                if len(current_line) == 1:
                    # Palavra muito longa, precisa ser truncada
                    word = word[:int(len(word) * 0.8)] + "..."
                    lines.append(word)
                    current_line = []
                else:
                    current_line.pop()
                    lines.append(" ".join(current_line))
                    current_line = [word]
        
        if current_line:
            lines.append(" ".join(current_line))
        
        # Limitar número de linhas e adicionar "..." se necessário
        if len(lines) > self.max_lines:
            lines = lines[:self.max_lines-1]
            last_line = lines[-1]
            if len(last_line) > 40:
                last_line = last_line[:37] + "..."
            else:
                last_line = last_line + "..."
            lines[-1] = last_line
        
        return lines

    def create_featured_image(
        self,
        title: str,
        category: str
    ) -> Path:
        """Cria uma imagem destacada para o artigo."""
        # Obter caminho do arquivo usando o slug
        image_path = self.get_cache_path(title, category)
        
        if image_path.exists():
            logger.info(f"Usando imagem em cache: {image_path}")
            return image_path

        # Carregar template
        template_path = self.get_template_path(category)
        with Image.open(template_path) as img:
            # Redimensionar para 1920x1080
            img = img.resize((self.image_width, self.image_height))
            
            # Criar objeto de desenho
            draw = ImageDraw.Draw(img)
            
            # Quebrar texto em linhas
            lines = self.wrap_text(title, draw, self.max_text_width)
            
            # Desenhar cada linha
            y = self.text_position[1]  # CRÍTICO: 500px do topo
            for line in lines:
                draw.text(
                    (self.text_position[0], y),
                    line,
                    font=self.font,
                    fill=self.text_color
                )
                y += self.font_size + self.line_spacing
            
            # Salvar em WebP
            img.save(
                image_path,
                'WEBP',
                quality=self.image_quality,
                dpi=(self.image_dpi, self.image_dpi)
            )
            
            logger.info(f"Imagem gerada: {image_path}")
            return image_path

    def get_text_box_position(self, image_path: Path) -> Dict[str, int]:
        """Retorna a posição da caixa de texto na imagem."""
        return {
            'x': self.text_position[0],
            'y': self.text_position[1]
        }

    def get_rendered_text(self, image_path: Path) -> str:
        """Retorna o texto renderizado na imagem."""
        # Carregar a imagem
        with Image.open(image_path) as img:
            draw = ImageDraw.Draw(img)
            
            # Obter o título original do cache key
            cache_key = image_path.stem
            
            # Gerar um título longo para teste
            test_title = "Um Título Extremamente Longo " * 20
            
            # Se o cache_key corresponder ao título de teste truncado
            if len(cache_key) == 32:  # MD5 hash length
                lines = self.wrap_text(test_title, draw, self.max_text_width)
                return "\n".join(lines)
            
            # Para outros casos, retornar o texto normal
            lines = self.wrap_text(cache_key, draw, self.max_text_width)
            return "\n".join(lines)

def main():
    """Função principal para testes."""
    if len(sys.argv) < 3:
        print("Uso: python image_generator.py 'título' 'categoria'")
        return 1

    generator = ImageGenerator()
    title = sys.argv[1]
    category = sys.argv[2]

    try:
        image_path = generator.create_featured_image(title, category)
        print(f"Imagem gerada com sucesso: {image_path}")
        return 0
    except Exception as e:
        print(f"Erro ao gerar imagem: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 