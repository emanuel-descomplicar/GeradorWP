"""
Utilitários para otimização SEO.
"""

from typing import Dict, List, Optional
import re
from .dify import DifyClient

class SEOOptimizer:
    """Classe para otimização SEO de conteúdo."""
    
    def __init__(self):
        """Inicializa o otimizador SEO."""
        self.dify = DifyClient()
    
    def optimize_title(
        self,
        title: str,
        keywords: List[str],
        max_length: int = 60
    ) -> str:
        """
        Otimiza o título para SEO.
        
        Args:
            title: Título original
            keywords: Lista de palavras-chave
            max_length: Comprimento máximo do título
            
        Returns:
            Título otimizado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize o seguinte título para SEO, mantendo-o com no máximo {max_length} caracteres
            e incluindo as palavras-chave principais: {', '.join(keywords)}
            
            Título original: {title}
            
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
            
            # Garante o comprimento máximo
            if len(optimized_title) > max_length:
                optimized_title = optimized_title[:max_length-3] + "..."
            
            return optimized_title
            
        except Exception as e:
            return title
    
    def optimize_meta_description(
        self,
        content: str,
        keywords: List[str],
        max_length: int = 160
    ) -> str:
        """
        Gera uma meta description otimizada.
        
        Args:
            content: Conteúdo do artigo
            keywords: Lista de palavras-chave
            max_length: Comprimento máximo da descrição
            
        Returns:
            Meta description otimizada
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Gere uma meta description otimizada para SEO com no máximo {max_length} caracteres,
            incluindo as palavras-chave principais: {', '.join(keywords)}
            
            Conteúdo: {content[:500]}...
            
            Retorne apenas a meta description, sem explicações adicionais.
            """
            
            # Gera a meta description
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=200
            )
            
            # Extrai a descrição
            meta_description = response["choices"][0]["text"].strip()
            
            # Garante o comprimento máximo
            if len(meta_description) > max_length:
                meta_description = meta_description[:max_length-3] + "..."
            
            return meta_description
            
        except Exception as e:
            return ""
    
    def optimize_content(
        self,
        content: str,
        keywords: List[str],
        min_keyword_density: float = 0.01,
        max_keyword_density: float = 0.03
    ) -> str:
        """
        Otimiza o conteúdo para SEO.
        
        Args:
            content: Conteúdo original
            keywords: Lista de palavras-chave
            min_keyword_density: Densidade mínima de palavras-chave
            max_keyword_density: Densidade máxima de palavras-chave
            
        Returns:
            Conteúdo otimizado
        """
        try:
            # Prepara o prompt
            prompt = f"""
            Otimize o seguinte conteúdo para SEO, mantendo uma densidade de palavras-chave
            entre {min_keyword_density*100}% e {max_keyword_density*100}% para as palavras-chave:
            {', '.join(keywords)}
            
            Conteúdo original:
            {content}
            
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
            
            # Verifica a densidade de palavras-chave
            for keyword in keywords:
                density = self._calculate_keyword_density(
                    optimized_content,
                    keyword
                )
                
                if density < min_keyword_density:
                    # Adiciona mais ocorrências da palavra-chave
                    optimized_content = self._increase_keyword_density(
                        optimized_content,
                        keyword,
                        min_keyword_density
                    )
                elif density > max_keyword_density:
                    # Remove algumas ocorrências da palavra-chave
                    optimized_content = self._decrease_keyword_density(
                        optimized_content,
                        keyword,
                        max_keyword_density
                    )
            
            return optimized_content
            
        except Exception as e:
            return content
    
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