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
from src.integrations.dify_client import DifyClient

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
            # Remove tags HTML extras
            content = re.sub(r'</?(?:html|body|article|section)[^>]*>', '', content)
            # Remove tags vazias
            content = re.sub(r'<[^>]*?/>', '', content)
            # Remove tags h1 duplicadas
            content = re.sub(r'<h1>.*?</h1>', '', content)
            # Remove tags h2 duplicadas que correspondem aos títulos das seções
            for title in section_titles.values():
                content = re.sub(f'<h2>{title}</h2>', '', content)
            # Remove tags ```html e ``` extras
            content = re.sub(r'```html\s*', '', content)
            content = re.sub(r'```\s*', '', content)
            # Remove tags h3 duplicadas ou mal formatadas
            content = re.sub(r'<h3>(.*?)</h3>\s*<p></h3>', r'<h3>\1</h3>', content)
            content = re.sub(r'<h3></p>', '</p>', content)
            # Remove espaços extras
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
        
        def format_section(content: str, section_type: str) -> str:
            """Formata uma seção específica do artigo."""
            if section_type == 'interest':
                # Extrai e formata tópicos numerados
                topics = extract_topics(content)
                formatted_content = []
                for num, title in topics:
                    formatted_content.append(f'<h3>{num}. {title}</h3>')
                    # Encontra o conteúdo entre este tópico e o próximo
                    pattern = f'<h3>{num}[\.:\)]?\s+{re.escape(title)}</h3>(.*?)(?=<h3>|$)'
                    match = re.search(pattern, content, re.DOTALL)
                    if match:
                        topic_content = clean_content(match.group(1))
                        formatted_content.append(topic_content)
                return '\n\n'.join(formatted_content)
            elif section_type == 'faq':
                # Formata perguntas e respostas
                questions = extract_questions(content)
                formatted_content = []
                for question, answer in questions:
                    formatted_content.extend([
                        f'<h3>{question}</h3>',
                        f'<p>{clean_content(answer)}</p>'
                    ])
                return '\n\n'.join(formatted_content)
            else:
                # Limpa e retorna o conteúdo normal
                return clean_content(content)
        
        # Construir o HTML
        html_parts = []
        
        # Título principal
        html_parts.append(f'<h1>{self.title}</h1>')
        
        # Seções do artigo
        for section_name, section_title in section_titles.items():
            if section_name in self.sections:
                html_parts.append(f'<h2>{section_title}</h2>')
                content = format_section(self.sections[section_name], section_name)
                html_parts.append(content)
        
        # Juntar todas as partes com quebras de linha
        return '\n\n'.join(html_parts)

class ContentGenerator:
    """Gerador de conteúdo usando a API Dify."""
    
    def __init__(self, dify_client: Optional[DifyClient] = None):
        """Inicializa o gerador de conteúdo.
        
        Args:
            dify_client: Cliente Dify (opcional, cria um novo se None)
        """
        self.dify = dify_client or DifyClient()
        self.internal_links = self._initialize_internal_links()
        
        logger.info(f"ContentGenerator inicializado com knowledge_base_id: {self.dify.knowledge_base_id}")
    
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
        # Mapear seções para prompts específicos
        prompts = {
            'attention': f"""Escreva uma introdução cativante sobre {topic}. 
            Inclua a importância do tema, contexto atual e o que será abordado no artigo.
            Use parágrafos curtos e linguagem clara. Formate em HTML com tags <p> e <h3>.
            Inclua 2-3 tópicos numerados sobre os principais pontos que serão abordados.""",
            
            'interest': f"""Desenvolva o conteúdo principal sobre {topic}.
            Explique detalhadamente cada aspecto importante, use exemplos práticos e dados relevantes.
            Formate em HTML usando tags <p>, <h3>, <ul>, <li> e <strong>.
            Inclua 4-5 tópicos numerados com subtítulos em <h3> explicando cada aspecto importante.""",
            
            'desire': f"""Liste e explique os principais benefícios de {topic}.
            Foque em resultados práticos e valor agregado.
            Formate em HTML usando tags <p>, <h3>, <ul> e <li>.
            Inclua 3-4 tópicos numerados com os benefícios mais relevantes.""",
            
            'action': f"""Escreva uma conclusão persuasiva sobre {topic}.
            Inclua um resumo dos pontos principais e próximos passos práticos.
            Formate em HTML usando tags <p> e <strong>.
            Termine com uma chamada para ação clara.""",
            
            'faq': f"""Crie uma seção de perguntas frequentes sobre {topic}.
            Inclua 5 perguntas relevantes com respostas objetivas.
            Formate cada pergunta com <strong> e cada resposta em <p>.
            Foque em dúvidas comuns e respostas práticas."""
        }
        
        # Gerar conteúdo usando o Dify
        try:
            response = self.dify.generate_content(prompts[section])
            if response and 'answer' in response:
                return response['answer']
            else:
                logger.error(f"Erro ao gerar conteúdo para seção {section}: resposta inválida")
                return f"<p>Erro ao gerar conteúdo para {section}</p>"
        except Exception as e:
            logger.error(f"Erro ao gerar conteúdo para seção {section}: {str(e)}")
            return f"<p>Erro ao gerar conteúdo para {section}</p>"