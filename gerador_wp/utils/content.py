"""
Utilitários para manipulação de conteúdo.
"""

from typing import Dict, List, Optional
import re
from .dify import DifyClient

class ContentManager:
    """Classe para gerenciamento de conteúdo."""
    
    def __init__(self):
        """Inicializa o gerenciador de conteúdo."""
        self.dify = DifyClient()
    
    def structure_content(
        self,
        content: str,
        template: str = "ACIDA"
    ) -> str:
        """
        Estrutura o conteúdo seguindo um template específico.
        
        Args:
            content: Conteúdo original
            template: Template a ser usado (ACIDA, AIDA, etc.)
            
        Returns:
            Conteúdo estruturado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Estruture o seguinte conteúdo seguindo o template {template}:
            
            Conteúdo original:
            {content}
            
            Retorne apenas o conteúdo estruturado, sem explicações adicionais.
            """
            
            # Gera o conteúdo estruturado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            structured_content = response["choices"][0]["text"].strip()
            
            return structured_content
            
        except Exception as e:
            return content
    
    def add_cta(
        self,
        content: str,
        cta_type: str = "generic",
        cta_text: Optional[str] = None
    ) -> str:
        """
        Adiciona um Call-to-Action ao conteúdo.
        
        Args:
            content: Conteúdo original
            cta_type: Tipo de CTA (generic, newsletter, contact, etc.)
            cta_text: Texto personalizado do CTA
            
        Returns:
            Conteúdo com CTA
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Adicione um Call-to-Action do tipo {cta_type} ao final do seguinte conteúdo.
            {f'Use o texto: {cta_text}' if cta_text else ''}
            
            Conteúdo original:
            {content}
            
            Retorne apenas o conteúdo com o CTA, sem explicações adicionais.
            """
            
            # Gera o conteúdo com CTA
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            content_with_cta = response["choices"][0]["text"].strip()
            
            return content_with_cta
            
        except Exception as e:
            return content
    
    def add_internal_links(
        self,
        content: str,
        internal_posts: List[Dict[str, str]]
    ) -> str:
        """
        Adiciona links internos ao conteúdo.
        
        Args:
            content: Conteúdo original
            internal_posts: Lista de posts internos com título e URL
            
        Returns:
            Conteúdo com links internos
        """
        try:
            # Prepara o prompt
            posts_info = "\n".join([
                f"- {post['title']}: {post['url']}"
                for post in internal_posts
            ])
            
            prompt = f"""
            Adicione links internos relevantes ao seguinte conteúdo, usando os posts disponíveis:
            
            Posts disponíveis:
            {posts_info}
            
            Conteúdo original:
            {content}
            
            Retorne apenas o conteúdo com os links internos, sem explicações adicionais.
            """
            
            # Gera o conteúdo com links
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            content_with_links = response["choices"][0]["text"].strip()
            
            return content_with_links
            
        except Exception as e:
            return content
    
    def add_external_links(
        self,
        content: str,
        external_links: List[Dict[str, str]]
    ) -> str:
        """
        Adiciona links externos ao conteúdo.
        
        Args:
            content: Conteúdo original
            external_links: Lista de links externos com título e URL
            
        Returns:
            Conteúdo com links externos
        """
        try:
            # Prepara o prompt
            links_info = "\n".join([
                f"- {link['title']}: {link['url']}"
                for link in external_links
            ])
            
            prompt = f"""
            Adicione links externos relevantes ao seguinte conteúdo, usando os links disponíveis:
            
            Links disponíveis:
            {links_info}
            
            Conteúdo original:
            {content}
            
            Retorne apenas o conteúdo com os links externos, sem explicações adicionais.
            """
            
            # Gera o conteúdo com links
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            content_with_links = response["choices"][0]["text"].strip()
            
            return content_with_links
            
        except Exception as e:
            return content
    
    def format_content(
        self,
        content: str,
        format_type: str = "html"
    ) -> str:
        """
        Formata o conteúdo para um tipo específico.
        
        Args:
            content: Conteúdo original
            format_type: Tipo de formatação (html, markdown, etc.)
            
        Returns:
            Conteúdo formatado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Formate o seguinte conteúdo em {format_type}:
            
            Conteúdo original:
            {content}
            
            Retorne apenas o conteúdo formatado, sem explicações adicionais.
            """
            
            # Gera o conteúdo formatado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            formatted_content = response["choices"][0]["text"].strip()
            
            return formatted_content
            
        except Exception as e:
            return content
    
    def extract_keywords(
        self,
        content: str,
        max_keywords: int = 5
    ) -> List[str]:
        """
        Extrai palavras-chave do conteúdo.
        
        Args:
            content: Conteúdo
            max_keywords: Número máximo de palavras-chave
            
        Returns:
            Lista de palavras-chave
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Extraia as {max_keywords} palavras-chave mais relevantes do seguinte conteúdo:
            
            Conteúdo:
            {content}
            
            Retorne apenas as palavras-chave separadas por vírgula, sem explicações adicionais.
            """
            
            # Gera as palavras-chave
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=100
            )
            
            # Extrai as palavras-chave
            keywords = [
                keyword.strip()
                for keyword in response["choices"][0]["text"].strip().split(",")
            ]
            
            return keywords[:max_keywords]
            
        except Exception as e:
            return []
    
    def generate_excerpt(
        self,
        content: str,
        max_length: int = 160
    ) -> str:
        """
        Gera um resumo do conteúdo.
        
        Args:
            content: Conteúdo
            max_length: Comprimento máximo do resumo
            
        Returns:
            Resumo do conteúdo
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Gere um resumo conciso do seguinte conteúdo com no máximo {max_length} caracteres:
            
            Conteúdo:
            {content}
            
            Retorne apenas o resumo, sem explicações adicionais.
            """
            
            # Gera o resumo
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            # Extrai o resumo
            excerpt = response["choices"][0]["text"].strip()
            
            # Garante o comprimento máximo
            if len(excerpt) > max_length:
                excerpt = excerpt[:max_length-3] + "..."
            
            return excerpt
            
        except Exception as e:
            return "" 