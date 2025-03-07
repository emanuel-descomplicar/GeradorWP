"""
WriterAgent - Responsável por criar o conteúdo do artigo.
"""

from typing import Dict, List, Optional
from crewai import Agent
from langchain.tools import Tool
import json
import os
from datetime import datetime
import hashlib

from ..config.config import (
    DIFY_API_KEY,
    DIFY_API_URL,
    CACHE_TTL,
    CACHE_DIR,
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY,
    MIN_CONTENT_LENGTH,
    MAX_CONTENT_LENGTH
)
from ..utils.cache import Cache
from ..utils.logger import Logger
from ..utils.dify import DifyClient
from ..utils.content import ContentManager
from ..utils.seo import SEOOptimizer
from ..utils.exceptions import WritingError

class WriterAgent:
    """Agente responsável por criar o conteúdo do artigo."""
    
    def __init__(self):
        """Inicializa o WriterAgent."""
        self.logger = Logger(__name__)
        self.cache = Cache()
        self.dify = DifyClient()
        self.content = ContentManager()
        self.seo = SEOOptimizer()
        
        self.agent = Agent(
            role='Escritor de Conteúdo',
            goal='Criar conteúdo de qualidade otimizado para SEO',
            backstory="""Você é um escritor especializado em marketing digital e criação de conteúdo.
            Sua função é transformar pesquisas em artigos bem estruturados, otimizados para SEO
            e adaptados ao público-alvo.""",
            verbose=True,
            allow_delegation=False,
            tools=self._get_tools(),
            llm_config={
                "config_list": [{
                    "model": "dify",
                    "api_key": DIFY_API_KEY,
                    "api_base": DIFY_API_URL
                }]
            }
        )
        
        # Cria o diretório de cache se não existir
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
    
    def _get_tools(self) -> List[Tool]:
        """Retorna a lista de ferramentas disponíveis para o agente."""
        return [
            Tool(
                name="structure_content",
                func=self._structure_content,
                description="Estrutura o conteúdo do artigo seguindo o padrão ACIDA"
            ),
            Tool(
                name="optimize_seo",
                func=self._optimize_seo,
                description="Otimiza o conteúdo para SEO"
            ),
            Tool(
                name="review_content",
                func=self._review_content,
                description="Revisa e melhora o conteúdo"
            )
        ]
    
    def _structure_content(self, research_data: Dict) -> Dict:
        """
        Estrutura o conteúdo do artigo seguindo o padrão ACIDA.
        
        Args:
            research_data: Dados da pesquisa para estruturar
            
        Returns:
            Dict com o conteúdo estruturado
        """
        try:
            # Gera chave de cache
            cache_key = f"structure_content_{hashlib.md5(json.dumps(research_data).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para estruturação de conteúdo")
                return cached_result
            
            # Prepara o prompt
            prompt = f"""
            Estruture um artigo seguindo o padrão ACIDA (Atenção, Curiosidade, Interesse, Desejo, Ação)
            usando os seguintes dados de pesquisa:
            
            Tópico: {research_data.get('topic')}
            Palavras-chave: {', '.join(research_data.get('keywords', []))}
            
            Dados da pesquisa:
            {json.dumps(research_data.get('web_results', {}), indent=2)}
            
            Estatísticas:
            {json.dumps(research_data.get('statistics', {}), indent=2)}
            
            Retorne a estrutura como um objeto JSON com as seções:
            - titulo
            - meta_description
            - introducao (Atenção)
            - contexto (Curiosidade)
            - desenvolvimento (Interesse)
            - beneficios (Desejo)
            - conclusao (Ação)
            - cta
            """
            
            # Gera a estrutura
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Processa o resultado
            result = json.loads(response["choices"][0]["text"])
            
            # Armazena no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao estruturar conteúdo")
            raise WritingError(f"Erro ao estruturar conteúdo: {str(e)}")
    
    def _optimize_seo(self, content: Dict) -> Dict:
        """
        Otimiza o conteúdo para SEO.
        
        Args:
            content: Conteúdo a ser otimizado
            
        Returns:
            Dict com o conteúdo otimizado
        """
        try:
            # Gera chave de cache
            cache_key = f"optimize_seo_{hashlib.md5(json.dumps(content).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para otimização SEO")
                return cached_result
            
            # Extrai palavras-chave
            keywords = self.content.extract_keywords(
                content.get('titulo', '') + ' ' + content.get('meta_description', '')
            )
            
            # Otimiza título
            content['titulo'] = self.seo.optimize_title(
                content['titulo'],
                keywords
            )
            
            # Otimiza meta description
            content['meta_description'] = self.seo.optimize_meta_description(
                content.get('meta_description', ''),
                keywords
            )
            
            # Otimiza conteúdo
            for section in ['introducao', 'contexto', 'desenvolvimento', 'beneficios', 'conclusao']:
                if section in content:
                    content[section] = self.seo.optimize_content(
                        content[section],
                        keywords
                    )
            
            # Gera slug
            content['slug'] = self.seo.generate_slug(content['titulo'])
            
            # Armazena no cache
            self.cache.set(cache_key, content)
            
            return content
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao otimizar SEO")
            raise WritingError(f"Erro ao otimizar SEO: {str(e)}")
    
    def _review_content(self, content: Dict) -> Dict:
        """
        Revisa e melhora o conteúdo.
        
        Args:
            content: Conteúdo a ser revisado
            
        Returns:
            Dict com o conteúdo revisado
        """
        try:
            # Gera chave de cache
            cache_key = f"review_content_{hashlib.md5(json.dumps(content).encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug("Cache hit para revisão de conteúdo")
                return cached_result
            
            # Prepara o prompt
            prompt = f"""
            Revise e melhore o seguinte conteúdo, verificando:
            - Clareza e coesão
            - Gramática e ortografia
            - Fluidez do texto
            - Tom de voz
            - Adequação ao público
            - Chamadas para ação
            
            Conteúdo:
            {json.dumps(content, indent=2)}
            
            Retorne o conteúdo revisado como um objeto JSON mantendo a mesma estrutura.
            """
            
            # Faz a revisão
            response = self.dify.completion(
                prompt=prompt,
                temperature=0.7,
                max_tokens=2000
            )
            
            # Processa o resultado
            result = json.loads(response["choices"][0]["text"])
            
            # Armazena no cache
            self.cache.set(cache_key, result)
            
            return result
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao revisar conteúdo")
            raise WritingError(f"Erro ao revisar conteúdo: {str(e)}")
    
    def write(self, research_data: Dict, keywords: List[str]) -> Dict:
        """
        Cria o conteúdo completo do artigo.
        
        Args:
            research_data: Dados da pesquisa
            keywords: Lista de palavras-chave para otimização
            
        Returns:
            Dict com o conteúdo final do artigo
        """
        try:
            self.logger.info("Iniciando criação de conteúdo")
            
            # Estrutura o conteúdo
            content = self._structure_content(research_data)
            
            # Otimiza para SEO
            content = self._optimize_seo(content)
            
            # Adiciona links internos
            if "related_content" in research_data:
                content = self.content.add_internal_links(
                    content,
                    research_data["related_content"]
                )
            
            # Adiciona CTA
            content = self.content.add_cta(content)
            
            # Revisa o conteúdo
            content = self._review_content(content)
            
            # Formata para HTML
            content = self.content.format_content(content, "html")
            
            # Gera excerpt
            content["excerpt"] = self.content.generate_excerpt(
                content.get("meta_description", "")
            )
            
            # Adiciona metadados
            content.update({
                "keywords": keywords,
                "timestamp": datetime.now().isoformat(),
                "word_count": len(content.get("content", "").split()),
                "reading_time": len(content.get("content", "").split()) // 200  # ~200 palavras por minuto
            })
            
            self.logger.info("Conteúdo criado com sucesso")
            return content
            
        except Exception as e:
            self.logger.log_error(e, "Erro ao criar conteúdo")
            raise WritingError(f"Erro ao criar conteúdo: {str(e)}") 