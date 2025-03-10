#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes para o gerador de conteúdo.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import pytest
from unittest.mock import Mock, patch
from src.generators.content_generator import ContentGenerator, Article

def test_article_initialization():
    """Testa a inicialização de um artigo."""
    title = "Teste de Artigo"
    category = "blog-marketing-digital"
    article = Article(title, category)
    
    assert article.title == title
    assert article.category == category
    assert isinstance(article.sections, dict)
    assert isinstance(article.meta, dict)
    assert 'tags' in article.meta
    assert 'featured_image' in article.meta
    assert 'excerpt' in article.meta
    assert 'seo_title' in article.meta
    assert 'seo_description' in article.meta

def test_article_add_section():
    """Testa a adição de seções a um artigo."""
    article = Article("Teste", "blog-marketing-digital")
    article.add_section("attention", "Conteúdo de teste")
    
    assert "attention" in article.sections
    assert article.sections["attention"] == "Conteúdo de teste"

def test_article_to_html():
    """Testa a conversão de artigo para HTML."""
    article = Article("Teste de HTML", "blog-marketing-digital")
    article.add_section("attention", "<p>Introdução de teste</p>")
    article.add_section("interest", "<h3>1. Primeiro Tópico</h3><p>Conteúdo</p>")
    article.add_section("desire", "<p>Benefícios de teste</p>")
    article.add_section("action", "<p>Conclusão de teste</p>")
    article.add_section("faq", "<strong>Pergunta 1?</strong> Resposta 1")
    
    html = article.to_html()
    
    assert "<h1>Teste de HTML</h1>" in html
    assert "<h2>Introdução</h2>" in html
    assert "<h3>1. Primeiro Tópico</h3>" in html
    assert "<h2>Benefícios</h2>" in html
    assert "<h2>Conclusão</h2>" in html
    assert "<h2>Perguntas Frequentes</h2>" in html
    assert "<h3>Pergunta 1?</h3>" in html

def test_content_generator_initialization(mock_dify_response):
    """Testa a inicialização do gerador de conteúdo."""
    mock_dify = Mock()
    mock_dify.knowledge_base_id = "test_kb_id"
    
    generator = ContentGenerator(mock_dify)
    assert generator.dify_client == mock_dify
    assert generator.knowledge_base_id == "test_kb_id"
    assert isinstance(generator.internal_links, dict)

def test_content_generator_format_title():
    """Testa a formatação de títulos."""
    mock_dify = Mock()
    generator = ContentGenerator(mock_dify)
    
    title = generator.format_title("Marketing Digital")
    assert isinstance(title, str)
    assert "Marketing Digital" in title

@patch('src.generators.content_generator.ContentGenerator._generate_section')
def test_content_generator_generate_article(mock_generate_section):
    """Testa a geração de artigos."""
    mock_dify = Mock()
    generator = ContentGenerator(mock_dify)
    
    # Configurar mock para retornar conteúdo de teste
    mock_generate_section.return_value = "Conteúdo de teste"
    
    article = generator.generate_article("Marketing Digital", "blog-marketing-digital")
    
    assert isinstance(article, Article)
    assert "Marketing Digital" in article.title
    assert article.category == "blog-marketing-digital"
    assert len(article.sections) == 5  # attention, interest, desire, action, faq
    
    # Verificar se _generate_section foi chamado para cada seção
    assert mock_generate_section.call_count == 5