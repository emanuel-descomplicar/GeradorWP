"""
Utilitários para manipulação de conteúdo.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

from typing import Dict, List, Optional
import re
from .dify import DifyClient
from ..config.templates import ACIDA_TEMPLATE, CTA_TEMPLATE, HTML_TEMPLATE

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
            # Gera o conteúdo estruturado com ênfase em precisão e fontes
            prompt = ACIDA_TEMPLATE.format(content=content) + """

            Regras adicionais:
            1. Inclua apenas informações verificáveis
            2. Cite fontes confiáveis para cada afirmação importante
            3. Use dados estatísticos recentes de Portugal quando disponíveis
            4. Evite generalizações sem suporte
            5. Mantenha um tom profissional e factual
            6. Inclua referências a estudos e relatórios relevantes
            7. Priorize fontes portuguesas e europeias
            8. Valide todas as informações técnicas
            """
            
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
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
            # Gera o CTA com foco em transparência
            prompt = CTA_TEMPLATE.format(
                content=content,
                cta_type=cta_type,
                cta_text=f"Texto base: {cta_text}" if cta_text else ""
            ) + """
            
            Regras adicionais:
            1. Mantenha promessas realistas e verificáveis
            2. Seja transparente sobre a oferta
            3. Evite exageros ou claims não comprovados
            4. Use dados concretos quando disponíveis
            5. Mantenha conformidade com RGPD
            """
            
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
            )
            
            # Extrai o CTA
            cta_html = response["choices"][0]["text"].strip()
            
            # Adiciona o CTA ao final do conteúdo
            if not content.endswith(cta_html):
                content = f"{content}\n\n{cta_html}"
            
            return content
            
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
            # Prepara o prompt com foco em relevância
            posts_info = "\n".join([
                f"- {post['title']}: {post['url']}"
                for post in internal_posts
            ])
            
            prompt = f"""
            Adicione links internos relevantes ao seguinte conteúdo, usando os posts disponíveis.
            Garanta que cada link adicionado seja contextualmente relevante e agregue valor real ao leitor.
            
            Posts disponíveis:
            {posts_info}
            
            Conteúdo original:
            {content}
            
            Regras:
            1. Adicione links apenas onde houver relevância direta
            2. Evite excesso de links (máximo 1 link a cada 300 palavras)
            3. Priorize conteúdo complementar e aprofundamento
            4. Mantenha o fluxo natural do texto
            5. Use âncoras descritivas e contextuais
            
            Retorne apenas o conteúdo com os links internos, sem explicações adicionais.
            """
            
            # Gera o conteúdo com links
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
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
        format_type: str = "html",
        title: Optional[str] = None,
        category: Optional[str] = None,
        tags: Optional[List[str]] = None,
        date: Optional[str] = None
    ) -> str:
        """
        Formata o conteúdo para um tipo específico.
        
        Args:
            content: Conteúdo original
            format_type: Tipo de formatação (html, markdown, etc.)
            title: Título do post
            category: Categoria do post
            tags: Tags do post
            date: Data do post
            
        Returns:
            Conteúdo formatado
        """
        try:
            # Formata as tags
            tags_html = ""
            if tags:
                tags_html = "\n".join([
                    f'<a href="#" class="post-tag">{tag}</a>'
                    for tag in tags
                ])
            
            # Gera o conteúdo formatado com foco em estrutura e semântica
            prompt = HTML_TEMPLATE.format(
                content=content,
                title=title or "",
                category=category or "",
                date=date or "",
                tags=tags_html
            ) + """
            
            Regras adicionais:
            1. Use estrutura HTML semântica
            2. Garanta acessibilidade (WCAG 2.1)
            3. Inclua metadados relevantes
            4. Otimize para SEO técnico
            5. Mantenha formatação consistente
            6. Inclua atributos alt em imagens
            7. Use heading hierarchy correta
            8. Adicione schema markup quando relevante
            """
            
            # Gera o conteúdo formatado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
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
            # Prepara o prompt com foco em relevância e precisão
            prompt = f"""
            Extraia as {max_keywords} palavras-chave mais relevantes do seguinte conteúdo,
            focando em termos relevantes para o mercado português.
            
            Conteúdo:
            {content}
            
            Regras:
            1. Use português de Portugal
            2. Foque em termos com volume de pesquisa comprovado
            3. Inclua termos específicos do mercado português
            4. Priorize termos técnicos precisos
            5. Evite termos muito genéricos
            6. Valide a relevância atual dos termos
            7. Considere a intenção de pesquisa
            8. Mantenha consistência com o setor
            
            Retorne apenas as palavras-chave separadas por vírgula, sem explicações adicionais.
            """
            
            # Gera as palavras-chave
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
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
            # Prepara o prompt com foco em precisão e valor
            prompt = f"""
            Gere um resumo conciso e factual do seguinte conteúdo,
            com no máximo {max_length} caracteres, em português de Portugal.
            
            Conteúdo:
            {content}
            
            Regras:
            1. Use português de Portugal
            2. Seja direto e factual
            3. Inclua o benefício principal comprovado
            4. Mantenha tom profissional
            5. Evite brasileirismos
            6. Use dados concretos quando disponíveis
            7. Evite promessas não verificáveis
            8. Mantenha foco no valor real
            
            Retorne apenas o resumo, sem explicações adicionais.
            """
            
            # Gera o resumo
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.3  # Temperatura baixa para maior precisão
            )
            
            # Extrai o resumo
            excerpt = response["choices"][0]["text"].strip()
            
            # Garante o comprimento máximo
            if len(excerpt) > max_length:
                excerpt = excerpt[:max_length-3] + "..."
            
            return excerpt
            
        except Exception as e:
            return "" 