#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de conteúdo para artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import time
import logging
import re
import random
from typing import Dict, List, Optional, Tuple
from bs4 import BeautifulSoup

# Configuração do logging
logger = logging.getLogger(__name__)

# Padrões de título
TITLE_PATTERNS = [
    "Como {tema}: {subtitulo}",
    "{tema} para Empresas: {subtitulo}",
    "{tema}: {subtitulo}",
    "Guia de {tema}: {subtitulo}",
    "{tema} na Prática: {subtitulo}",
    "Estratégias de {tema}: {subtitulo}",
    "Tudo sobre {tema}: {subtitulo}",
    "{tema} para PMEs: {subtitulo}",
    "Manual de {tema}: {subtitulo}",
    "{tema} em Portugal: {subtitulo}"
]

# Padrões de subtítulo
SUBTITLE_PATTERNS = [
    "Guia Completo",
    "Tudo o que Precisa de Saber",
    "Estratégias Práticas",
    "Dicas e Boas Práticas",
    "O Guia Definitivo",
    "Passo a Passo",
    "Melhores Práticas",
    "Como Implementar",
    "Guia para Iniciantes",
    "Estratégias Avançadas"
]

class Article:
    """Representa um artigo com suas seções e metadados."""
    
    def __init__(self, title: str, category: str):
        """Inicializa um novo artigo.
        
        Args:
            title: Título do artigo
            category: Categoria do artigo
        """
        self.title = title
        self.category = category
        self.sections = {}
        self.meta = {
            'tags': [],
            'featured_image': None,
            'excerpt': None,
            'seo_title': None,
            'seo_description': None
        }
    
    def add_section(self, name: str, content: str):
        """Adiciona uma seção ao artigo.
        
        Args:
            name: Nome da seção
            content: Conteúdo da seção
        """
        self.sections[name] = content
    
    def to_html(self) -> str:
        """Converte o artigo para HTML formatado.
        
        Returns:
            HTML formatado do artigo
        """
        # Definir títulos das seções
        section_titles = {
            'attention': 'Introdução',
            'interest': 'Desenvolvimento',
            'desire': 'Benefícios',
            'action': 'Conclusão',
            'faq': 'Perguntas Frequentes'
        }
        
        # Funções auxiliares
        def clean_content(content: str) -> str:
            """Limpa o conteúdo HTML."""
            # Remove tags vazias e espaços extras
            content = re.sub(r'<[^>]*?/>', '', content)
            content = re.sub(r'\s+', ' ', content)
            return content.strip()
        
        def extract_topics(content: str) -> List[Tuple[int, str]]:
            """Extrai tópicos numerados do conteúdo."""
            topics = []
            patterns = [
                r'<strong>(\d+)[\.:\)]?\s+(.*?)</strong>',
                r'<b>(\d+)[\.:\)]?\s+(.*?)</b>',
                r'<p>(\d+)[\.:\)]?\s+(.*?)</p>',
                r'<h3>(\d+)[\.:\)]?\s+(.*?)</h3>'
            ]
            
            for pattern in patterns:
                matches = re.finditer(pattern, content)
                for match in matches:
                    num = int(match.group(1))
                    title = match.group(2).strip()
                    topics.append((num, title))
            
            return sorted(topics)
        
        def extract_questions(content: str) -> List[Tuple[str, str]]:
            """Extrai perguntas e respostas do FAQ."""
            questions = []
            pattern = r'<strong>(.*?)</strong>\s*(.*?)(?=<strong>|$)'
            matches = re.finditer(pattern, content, re.DOTALL)
            
            for match in matches:
                question = match.group(1).strip()
                answer = match.group(2).strip()
                if question and answer:
                    questions.append((question, answer))
            
            return questions
        
        # Construir o HTML
        html_parts = []
        
        # Título principal
        html_parts.append(f'<h1>{self.title}</h1>')
        
        # Seção de Atenção (Introdução)
        if 'attention' in self.sections:
            html_parts.append(f'<h2>{section_titles["attention"]}</h2>')
            html_parts.append(clean_content(self.sections['attention']))
        
        # Seção de Interesse (Desenvolvimento)
        if 'interest' in self.sections:
            html_parts.append(f'<h2>{section_titles["interest"]}</h2>')
            topics = extract_topics(self.sections['interest'])
            for num, title in topics:
                html_parts.append(f'<h3>{num}. {title}</h3>')
        
        # Seção de Desejo (Benefícios)
        if 'desire' in self.sections:
            html_parts.append(f'<h2>{section_titles["desire"]}</h2>')
            html_parts.append(clean_content(self.sections['desire']))
        
        # Seção de Ação (Conclusão)
        if 'action' in self.sections:
            html_parts.append(f'<h2>{section_titles["action"]}</h2>')
            html_parts.append(clean_content(self.sections['action']))
        
        # Seção de FAQ
        if 'faq' in self.sections:
            html_parts.append(f'<h2>{section_titles["faq"]}</h2>')
            questions = extract_questions(self.sections['faq'])
            for question, answer in questions:
                html_parts.append(f'<h3>{question}</h3>')
                html_parts.append(f'<p>{answer}</p>')
        
        # Juntar todas as partes
        return '\n'.join(html_parts)

class ContentGenerator:
    """Gerador de conteúdo para artigos."""
    
    def __init__(self, dify_client, knowledge_base_id: str = None):
        """Inicializa o gerador de conteúdo.
        
        Args:
            dify_client: Instância do cliente Dify
            knowledge_base_id: ID da base de conhecimento (se None, usa o valor do cliente Dify)
        """
        self.dify_client = dify_client
        self.knowledge_base_id = knowledge_base_id or dify_client.knowledge_base_id
        
        # Inicializar mapeamento de links internos
        self.internal_links = self._initialize_internal_links()
        
        logger.info(f"ContentGenerator inicializado com knowledge_base_id: {self.knowledge_base_id}")
    
    def _initialize_internal_links(self) -> Dict[str, List[Dict[str, str]]]:
        """Inicializa o mapeamento de links internos por categoria."""
        return {
            "general": [
                {
                    "url": "https://descomplicar.pt/transforme-o-seu-negocio-com-o-poder-do-marketing-digital/",
                    "title": "Transforme o seu negócio com o Poder do Marketing Digital",
                    "context": "transformação digital e crescimento de negócios",
                    "description": "artigo sobre como potencializar resultados através do marketing digital"
                }
            ],
            "blog-marketing-digital": [
                {
                    "url": "https://descomplicar.pt/marketing/",
                    "title": "Marketing Digital Descomplicar",
                    "context": "estratégias de marketing digital",
                    "description": "serviços completos de marketing digital para empresas"
                }
            ]
        }
    
    def format_title(self, topic: str) -> str:
        """Formata o título do artigo usando padrões predefinidos.
        
        Args:
            topic: Tópico principal do artigo
        
        Returns:
            Título formatado
        """
        pattern = random.choice(TITLE_PATTERNS)
        subtitle = random.choice(SUBTITLE_PATTERNS)
        return pattern.format(tema=topic, subtitulo=subtitle)
    
    def generate_article(self, topic: str, category: str) -> Article:
        """Gera um novo artigo.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo
        
        Returns:
            Artigo gerado
        """
        # Formatar título
        title = self.format_title(topic)
        logger.info(f"Gerando artigo: {title}")
        
        # Criar artigo
        article = Article(title, category)
        
        # Gerar seções
        sections = ['attention', 'interest', 'desire', 'action', 'faq']
        for section in sections:
            content = self._generate_section(topic, section)
            article.add_section(section, content)
        
        return article
    
    def _generate_section(self, topic: str, section: str) -> str:
        """Gera o conteúdo de uma seção do artigo.
        
        Args:
            topic: Tópico do artigo
            section: Nome da seção
        
        Returns:
            Conteúdo da seção
        """
        # Implementar lógica de geração de conteúdo aqui
        # Por enquanto, retorna um placeholder
        return f"Conteúdo da seção {section} sobre {topic}"