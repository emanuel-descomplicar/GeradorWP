"""
Utilitários para otimização SEO.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

from typing import Dict, List, Optional
import re
from .dify import DifyClient

class SEOOptimizer:
    """Classe para otimização SEO."""
    
    def __init__(self):
        """Inicializa o otimizador SEO."""
        self.dify = DifyClient()
    
    def optimize_title(self, title: str, keywords: List[str]) -> str:
        """
        Otimiza o título para SEO.
        
        Args:
            title: Título original
            keywords: Palavras-chave alvo
            
        Returns:
            Título otimizado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize o seguinte título para SEO, usando as palavras-chave fornecidas:
            
            Título: {title}
            
            Palavras-chave:
            {', '.join(keywords)}
            
            Regras:
            1. Mantenha entre 50-60 caracteres
            2. Inclua palavra-chave principal no início
            3. Use linguagem natural e atraente
            4. Evite clickbait
            5. Use português de Portugal
            
            Retorne apenas o título otimizado, sem explicações adicionais.
            """
            
            # Gera o título otimizado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=100
            )
            
            # Extrai o título
            optimized_title = response["choices"][0]["text"].strip()
            
            return optimized_title
            
        except Exception as e:
            return title
    
    def optimize_meta_description(
        self,
        description: str,
        keywords: List[str],
        max_length: int = 160
    ) -> str:
        """
        Otimiza a meta descrição para SEO.
        
        Args:
            description: Descrição original
            keywords: Palavras-chave alvo
            max_length: Comprimento máximo
            
        Returns:
            Meta descrição otimizada
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize a seguinte meta descrição para SEO, usando as palavras-chave fornecidas:
            
            Descrição: {description}
            
            Palavras-chave:
            {', '.join(keywords)}
            
            Regras:
            1. Mantenha entre 150-160 caracteres
            2. Inclua palavra-chave principal naturalmente
            3. Seja persuasivo e informativo
            4. Inclua call-to-action
            5. Use português de Portugal
            
            Retorne apenas a meta descrição otimizada, sem explicações adicionais.
            """
            
            # Gera a meta descrição
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            # Extrai a descrição
            optimized_description = response["choices"][0]["text"].strip()
            
            # Garante o comprimento máximo
            if len(optimized_description) > max_length:
                optimized_description = optimized_description[:max_length-3] + "..."
            
            return optimized_description
            
        except Exception as e:
            return description
    
    def optimize_headings(
        self,
        content: str,
        keywords: List[str]
    ) -> str:
        """
        Otimiza os títulos e subtítulos para SEO.
        
        Args:
            content: Conteúdo HTML
            keywords: Palavras-chave alvo
            
        Returns:
            Conteúdo com títulos otimizados
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize os títulos e subtítulos do seguinte conteúdo para SEO,
            usando as palavras-chave fornecidas:
            
            Conteúdo: {content}
            
            Palavras-chave:
            {', '.join(keywords)}
            
            Regras:
            1. Mantenha hierarquia H1 > H2 > H3
            2. Inclua palavras-chave naturalmente
            3. Use linguagem persuasiva
            4. Mantenha consistência
            5. Use português de Portugal
            
            Retorne apenas o conteúdo com títulos otimizados, sem explicações adicionais.
            """
            
            # Gera o conteúdo otimizado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            optimized_content = response["choices"][0]["text"].strip()
            
            return optimized_content
            
        except Exception as e:
            return content
    
    def optimize_content(
        self,
        content: str,
        keywords: List[str]
    ) -> str:
        """
        Otimiza o conteúdo para SEO.
        
        Args:
            content: Conteúdo HTML
            keywords: Palavras-chave alvo
            
        Returns:
            Conteúdo otimizado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize o seguinte conteúdo para SEO,
            usando as palavras-chave fornecidas:
            
            Conteúdo: {content}
            
            Palavras-chave:
            {', '.join(keywords)}
            
            Regras:
            1. Mantenha densidade de palavras-chave natural (1-3%)
            2. Use variações das palavras-chave
            3. Adicione links internos relevantes
            4. Otimize imagens (alt text)
            5. Use português de Portugal
            6. Mantenha parágrafos curtos
            7. Use listas e destaques
            8. Inclua chamadas para ação
            
            Retorne apenas o conteúdo otimizado, sem explicações adicionais.
            """
            
            # Gera o conteúdo otimizado
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Extrai o conteúdo
            optimized_content = response["choices"][0]["text"].strip()
            
            return optimized_content
            
        except Exception as e:
            return content
    
    def generate_schema_markup(
        self,
        title: str,
        description: str,
        content: str,
        author: str = "Descomplicar",
        publisher: str = "Descomplicar",
        date: Optional[str] = None
    ) -> Dict:
        """
        Gera schema markup para o artigo.
        
        Args:
            title: Título do artigo
            description: Descrição do artigo
            content: Conteúdo do artigo
            author: Autor do artigo
            publisher: Publicador do artigo
            date: Data de publicação
            
        Returns:
            Schema markup em formato JSON-LD
        """
        try:
            # Prepara o schema
            schema = {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": title,
                "description": description,
                "articleBody": content,
                "author": {
                    "@type": "Organization",
                    "name": author,
                    "url": "https://descomplicar.pt"
                },
                "publisher": {
                    "@type": "Organization",
                    "name": publisher,
                    "url": "https://descomplicar.pt",
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://descomplicar.pt/logo.png"
                    }
                }
            }
            
            # Adiciona data se fornecida
            if date:
                schema["datePublished"] = date
                schema["dateModified"] = date
            
            return schema
            
        except Exception as e:
            return {}
    
    def generate_slug(self, title: str) -> str:
        """
        Gera um slug otimizado para SEO.
        
        Args:
            title: Título do artigo
            
        Returns:
            Slug otimizado
        """
        try:
            # Remove caracteres especiais
            slug = re.sub(r'[^\w\s-]', '', title.lower())
            
            # Substitui espaços por hífens
            slug = re.sub(r'[-\s]+', '-', slug)
            
            # Remove hífens no início e fim
            slug = slug.strip('-')
            
            return slug
            
        except Exception as e:
            return ""
    
    def _calculate_keyword_density(
        self,
        content: str,
        keyword: str
    ) -> float:
        """
        Calcula a densidade de uma palavra-chave no conteúdo.
        
        Args:
            content: Conteúdo
            keyword: Palavra-chave
            
        Returns:
            Densidade da palavra-chave
        """
        try:
            # Conta palavras totais
            total_words = len(content.split())
            
            # Conta ocorrências da palavra-chave
            keyword_count = len(
                re.findall(
                    r'\b' + re.escape(keyword.lower()) + r'\b',
                    content.lower()
                )
            )
            
            return keyword_count / total_words if total_words > 0 else 0
            
        except Exception as e:
            return 0
    
    def _increase_keyword_density(
        self,
        content: str,
        keyword: str,
        target_density: float
    ) -> str:
        """
        Aumenta a densidade de uma palavra-chave no conteúdo.
        
        Args:
            content: Conteúdo
            keyword: Palavra-chave
            target_density: Densidade alvo
            
        Returns:
            Conteúdo com densidade aumentada
        """
        try:
            # Calcula palavras totais
            total_words = len(content.split())
            
            # Calcula número de ocorrências necessárias
            target_count = int(total_words * target_density)
            current_count = len(
                re.findall(
                    r'\b' + re.escape(keyword.lower()) + r'\b',
                    content.lower()
                )
            )
            
            # Adiciona ocorrências em posições estratégicas
            if target_count > current_count:
                paragraphs = content.split('\n\n')
                for i in range(target_count - current_count):
                    if i < len(paragraphs):
                        paragraphs[i] = f"{paragraphs[i]} {keyword}."
                
                content = '\n\n'.join(paragraphs)
            
            return content
            
        except Exception as e:
            return content
    
    def _decrease_keyword_density(
        self,
        content: str,
        keyword: str,
        target_density: float
    ) -> str:
        """
        Diminui a densidade de uma palavra-chave no conteúdo.
        
        Args:
            content: Conteúdo
            keyword: Palavra-chave
            target_density: Densidade alvo
            
        Returns:
            Conteúdo com densidade diminuída
        """
        try:
            # Calcula palavras totais
            total_words = len(content.split())
            
            # Calcula número de ocorrências necessárias
            target_count = int(total_words * target_density)
            current_count = len(
                re.findall(
                    r'\b' + re.escape(keyword.lower()) + r'\b',
                    content.lower()
                )
            )
            
            # Remove ocorrências extras
            if current_count > target_count:
                # Encontra todas as ocorrências
                matches = list(
                    re.finditer(
                        r'\b' + re.escape(keyword.lower()) + r'\b',
                        content.lower()
                    )
                )
                
                # Remove as ocorrências extras
                for match in matches[target_count:]:
                    start, end = match.span()
                    content = content[:start] + content[end:]
            
            return content
            
        except Exception as e:
            return content 