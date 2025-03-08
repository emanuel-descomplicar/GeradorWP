#!/usr/bin/env python3
"""
Script de teste para o gerador de imagens destacadas.

Este módulo contém testes unitários para validar o funcionamento do gerador
de imagens destacadas, incluindo:

1. Geração de Slugs:
   - Remoção de palavras desnecessárias (artigos, preposições, etc.)
   - Normalização de caracteres especiais
   - Limitação de comprimento (máx. 50 caracteres)
   - Tratamento de casos especiais (e-commerce)
   - Validação de formato SEO-friendly

2. Nomes de Arquivos:
   - Baseados no slug do título
   - Formato WebP otimizado
   - Comprimento máximo de 50 caracteres
   - Caracteres válidos apenas (a-z, 0-9, hífen)

3. Qualidade de Imagem:
   - Dimensões Full HD (1920x1080px)
   - Posicionamento de texto (500px do topo)
   - Formato WebP com qualidade 90%
   - DPI fixo em 72
   - Cache eficiente

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import unittest
from PIL import Image
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from image_generator import ImageGenerator

class TestImageGenerator(unittest.TestCase):
    """Classe de testes para o gerador de imagens destacadas."""

    def setUp(self):
        """
        Configuração inicial dos testes.
        Define variáveis comuns usadas em múltiplos testes.
        """
        self.generator = ImageGenerator()
        self.test_title = "Como Implementar Marketing Digital para PMEs: Guia Completo"
        self.categories = [
            "Marketing Digital",
            "E-commerce",
            "Gestao PMEs",
            "Inteligencia Artificial",
            "Transformacao Digital",
            "Vendas",
            "Empreendedorismo",
            "Tecnologia"
        ]
        self.templates_dir = Path(__file__).parent.parent.parent / "gerador_wp" / "templates"

    def test_template_files_exist(self):
        """Verifica se todos os templates existem no diretório correto."""
        for category in self.categories:
            template_name = f"blog-{category.lower().replace(' ', '-')}.png"
            template_path = self.templates_dir / template_name
            self.assertTrue(
                template_path.exists(),
                f"Template não encontrado: {template_name}"
            )

    def test_image_dimensions(self):
        """Verifica se as imagens geradas têm as dimensões Full HD (1920x1080)."""
        for category in self.categories:
            image_path = self.generator.create_featured_image(
                title=self.test_title,
                category=category
            )
            with Image.open(image_path) as img:
                self.assertEqual(img.size, (1920, 1080))

    def test_text_positioning(self):
        """
        Verifica se o texto está posicionado corretamente na imagem.
        O texto deve estar a 500px do topo (CRÍTICO) e 100px da margem esquerda.
        """
        image_path = self.generator.create_featured_image(
            title=self.test_title,
            category="Marketing Digital"
        )
        text_box = self.generator.get_text_box_position(image_path)
        self.assertEqual(text_box['y'], 500)  # Margem superior crítica
        self.assertEqual(text_box['x'], 100)  # Margem esquerda

    def test_title_truncation(self):
        """
        Verifica se títulos longos são truncados corretamente.
        - Máximo de 5 linhas de texto
        - Truncamento com "..." quando necessário
        - Nome do arquivo limitado a 50 caracteres
        """
        long_title = "Um Título Extremamente Longo que Certamente Vai Precisar Ser Truncado " * 10
        
        image_path = self.generator.create_featured_image(
            title=long_title,
            category="Marketing Digital"
        )
        
        # Verificar nome do arquivo
        filename = image_path.name
        self.assertLessEqual(
            len(filename[:-5]),  # Remover .webp
            50,
            f"Nome do arquivo muito longo: {filename}"
        )
        
        # Verificar texto renderizado
        text = self.generator.get_rendered_text(image_path)
        self.assertLessEqual(len(text.split('\n')), 5)  # Máximo 5 linhas
        self.assertTrue(
            text.endswith('...') or '...' in text,
            f"Texto não foi truncado corretamente: {text}"
        )

    def test_image_quality(self):
        """
        Verifica a qualidade da imagem gerada.
        - Formato WebP
        - DPI fixo em 72
        - Qualidade de 90%
        """
        image_path = self.generator.create_featured_image(
            title=self.test_title,
            category="Marketing Digital"
        )
        with Image.open(image_path) as img:
            self.assertEqual(img.format, "WEBP")
            self.assertEqual(img.info.get("dpi", (72, 72))[0], 72)

    def test_file_naming(self):
        """
        Verifica se os nomes dos arquivos são válidos.
        - Máximo de 50 caracteres
        - Extensão .webp
        - Baseado no slug do título
        """
        image_path = self.generator.create_featured_image(
            title=self.test_title,
            category="Marketing Digital"
        )
        filename = os.path.basename(image_path)
        self.assertLessEqual(len(filename), 50)
        self.assertTrue(filename.endswith(".webp"))

    def test_cache_functionality(self):
        """
        Verifica se o cache está funcionando corretamente.
        - Mesma imagem não deve ser regerada
        - Mesmo caminho deve ser retornado
        - Data de modificação deve ser igual
        """
        first_path = self.generator.create_featured_image(
            title=self.test_title,
            category="Marketing Digital"
        )
        first_mtime = os.path.getmtime(first_path)

        second_path = self.generator.create_featured_image(
            title=self.test_title,
            category="Marketing Digital"
        )
        second_mtime = os.path.getmtime(second_path)

        self.assertEqual(first_mtime, second_mtime)
        self.assertEqual(first_path, second_path)

    def test_comprehensive_slug_generation(self):
        """
        Teste abrangente para validar a geração de slugs.
        Verifica múltiplos casos incluindo:
        - Remoção de palavras desnecessárias
        - Normalização de caracteres especiais
        - Tratamento de casos especiais
        - Limitação de comprimento
        - Formato SEO-friendly
        """
        test_cases = [
            # Títulos básicos
            (
                "Como Implementar Marketing Digital para PMEs: Guia Completo",
                "como-implementar-marketing-digital-pmes"
            ),
            # Caracteres especiais e acentos
            (
                "A Importância do E-commerce nas Empresas Portuguesas",
                "importancia-e-commerce"
            ),
            # Palavras desnecessárias
            (
                "Como Usar o Instagram para Impulsionar seu Negócio",
                "como-usar-instagram-impulsionar"
            ),
            # Números e caracteres especiais
            (
                "10 Dicas Práticas de Marketing Digital para PMEs em 2024",
                "10-dicas-praticas-marketing-digital-pmes"
            ),
            # Título longo que precisa ser truncado
            (
                "Como Desenvolver uma Estratégia Completa de Marketing Digital para Pequenas e Médias Empresas no Mercado Português",
                "como-desenvolver-estrategia-marketing-digital-pmes"
            ),
            # Casos especiais de formatação
            (
                "E-commerce vs. Loja Física: O Que é Melhor para seu Negócio?",
                "e-commerce-vs-loja-fisica"
            ),
            # Remoção de artigos e preposições
            (
                "A Transformação Digital nas Empresas do Futuro",
                "transformacao-digital"
            ),
            # Múltiplos espaços e pontuação
            (
                "Marketing    Digital:   Estratégias   &   Táticas!!!",
                "marketing-digital"
            ),
            # Palavras em maiúsculas
            (
                "COMO VENDER MAIS COM MARKETING DIGITAL",
                "como-vender-marketing-digital"
            ),
            # Caracteres especiais no meio do texto
            (
                "Estratégias de E-mail & SMS Marketing: Guia Completo",
                "estrategias-e-mail-sms-marketing"
            )
        ]
        
        for title, expected_slug in test_cases:
            generated_slug = self.generator.generate_slug(title)
            
            # Verificar correspondência com slug esperado
            self.assertEqual(
                generated_slug,
                expected_slug,
                f"Slug incorreto para '{title}'\nGerado: {generated_slug}\nEsperado: {expected_slug}"
            )
            
            # Verificar comprimento máximo
            self.assertLessEqual(
                len(generated_slug),
                50,
                f"Slug muito longo: {len(generated_slug)} caracteres"
            )
            
            # Verificar caracteres válidos
            self.assertTrue(
                all(c.islower() or c.isdigit() or c == '-' for c in generated_slug),
                f"Slug contém caracteres inválidos: {generated_slug}"
            )
            
            # Verificar hífens duplicados
            self.assertFalse(
                '--' in generated_slug,
                f"Slug contém hífens duplicados: {generated_slug}"
            )
            
            # Verificar início e fim
            self.assertFalse(
                generated_slug.startswith('-') or generated_slug.endswith('-'),
                f"Slug começa ou termina com hífen: {generated_slug}"
            )

    def test_image_file_naming(self):
        """
        Verifica se os nomes dos arquivos de imagem seguem o padrão SEO.
        - Nome baseado no slug do título
        - Extensão .webp
        - Comprimento máximo respeitado
        - Caracteres válidos apenas
        """
        test_cases = [
            (
                "Como Implementar Marketing Digital para PMEs: Guia Completo",
                "Marketing Digital"
            ),
            (
                "Estratégias de SEO para E-commerce: O Guia Definitivo",
                "E-commerce"
            ),
            (
                "A Importância da Transformação Digital nas Empresas Portuguesas",
                "Transformacao Digital"
            ),
            (
                "10 Dicas Práticas de Marketing Digital para PMEs",
                "Marketing Digital"
            )
        ]
        
        for title, category in test_cases:
            image_path = self.generator.create_featured_image(title, category)
            filename = image_path.name
            
            # Verificar extensão
            self.assertTrue(
                filename.endswith(".webp"),
                f"Arquivo não tem extensão .webp: {filename}"
            )
            
            # Verificar slug no nome do arquivo
            expected_slug = self.generator.generate_slug(title)
            self.assertEqual(
                filename,
                f"{expected_slug}.webp",
                f"Nome do arquivo não corresponde ao slug esperado para '{title}'"
            )
            
            # Verificar comprimento total
            self.assertLessEqual(
                len(filename),
                55,  # 50 chars + .webp
                f"Nome do arquivo muito longo: {filename}"
            )
            
            # Verificar caracteres válidos no nome
            name_without_ext = filename[:-5]  # Remover .webp
            self.assertTrue(
                all(c.islower() or c.isdigit() or c == '-' for c in name_without_ext),
                f"Nome do arquivo contém caracteres inválidos: {filename}"
            )

if __name__ == "__main__":
    unittest.main() 