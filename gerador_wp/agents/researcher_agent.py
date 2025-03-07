"""
ResearcherAgent - Responsável por pesquisar e coletar informações para o conteúdo.
"""

from typing import Dict, List, Optional
from crewai import Agent
from langchain.tools import Tool
from bs4 import BeautifulSoup
import requests
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
    RETRY_DELAY
)
from ..utils.cache import Cache
from ..utils.logger import Logger
from ..utils.http import HttpClient
from ..utils.dify import DifyClient
from ..utils.exceptions import ResearchError

class ResearcherAgent:
    """Agente responsável por pesquisar e coletar informações para o conteúdo."""
    
    def __init__(self):
        """Inicializa o ResearcherAgent."""
        self.logger = Logger(__name__)
        self.cache = Cache()
        self.http = HttpClient()
        self.dify = DifyClient()
        
        self.agent = Agent(
            role='Pesquisador de Conteúdo',
            goal='Pesquisar e coletar informações relevantes para criar conteúdo de qualidade',
            backstory="""Você é um pesquisador especializado em marketing digital e criação de conteúdo.
            Sua função é coletar informações relevantes, analisar tendências e identificar dados estatísticos
            que possam enriquecer o conteúdo.""",
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
                name="web_search",
                func=self._web_search,
                description="Pesquisa informações na web sobre um tópico específico"
            ),
            Tool(
                name="analyze_content",
                func=self._analyze_content,
                description="Analisa conteúdo existente para identificar padrões e tendências"
            ),
            Tool(
                name="collect_stats",
                func=self._collect_stats,
                description="Coleta dados estatísticos relevantes para o tópico"
            )
        ]
    
    def _web_search(self, query: str) -> Dict:
        """
        Realiza uma pesquisa na web sobre um tópico específico.
        
        Args:
            query: A consulta de pesquisa
            
        Returns:
            Dict com os resultados da pesquisa
        """
        try:
            # Gera chave de cache
            cache_key = f"web_search_{hashlib.md5(query.encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug(f"Cache hit para pesquisa: {query}")
                return cached_result
            
            # Prepara o prompt
            prompt = f"""
            Pesquise informações relevantes sobre o seguinte tópico:
            
            Tópico: {query}
            
            Retorne apenas os resultados mais relevantes, incluindo:
            - Principais conceitos
            - Dados estatísticos
            - Tendências atuais
            - Melhores práticas
            - Exemplos práticos
            
            Formate a resposta como um objeto JSON com os campos acima.
            """
            
            # Faz a pesquisa
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
            self.logger.log_error(e, f"Erro na pesquisa web: {query}")
            raise ResearchError(f"Erro ao pesquisar: {str(e)}")
    
    def _analyze_content(self, url: str) -> Dict:
        """
        Analisa conteúdo existente para identificar padrões e tendências.
        
        Args:
            url: URL do conteúdo a ser analisado
            
        Returns:
            Dict com a análise do conteúdo
        """
        try:
            # Gera chave de cache
            cache_key = f"analyze_content_{hashlib.md5(url.encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug(f"Cache hit para análise: {url}")
                return cached_result
            
            # Faz download do conteúdo
            response = self.http.get(url)
            
            # Parse do HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrai o texto
            text = soup.get_text()
            
            # Prepara o prompt
            prompt = f"""
            Analise o seguinte conteúdo e identifique:
            
            Conteúdo:
            {text[:2000]}...
            
            Retorne a análise como um objeto JSON com:
            - Tópicos principais
            - Palavras-chave
            - Tom de voz
            - Estrutura
            - Pontos fortes
            - Pontos fracos
            - Sugestões de melhoria
            """
            
            # Faz a análise
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
            self.logger.log_error(e, f"Erro na análise de conteúdo: {url}")
            raise ResearchError(f"Erro ao analisar conteúdo: {str(e)}")
    
    def _collect_stats(self, topic: str) -> Dict:
        """
        Coleta dados estatísticos relevantes para o tópico.
        
        Args:
            topic: O tópico para coletar estatísticas
            
        Returns:
            Dict com as estatísticas coletadas
        """
        try:
            # Gera chave de cache
            cache_key = f"collect_stats_{hashlib.md5(topic.encode()).hexdigest()}"
            
            # Tenta recuperar do cache
            cached_result = self.cache.get(cache_key)
            if cached_result:
                self.logger.debug(f"Cache hit para estatísticas: {topic}")
                return cached_result
            
            # Prepara o prompt
            prompt = f"""
            Colete dados estatísticos relevantes sobre:
            
            Tópico: {topic}
            
            Retorne apenas as estatísticas mais relevantes e atuais como um objeto JSON com:
            - Dados numéricos
            - Percentuais
            - Tendências
            - Previsões
            - Comparações
            - Fontes
            """
            
            # Faz a coleta
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
            self.logger.log_error(e, f"Erro na coleta de estatísticas: {topic}")
            raise ResearchError(f"Erro ao coletar estatísticas: {str(e)}")
    
    def research(self, topic: str, keywords: List[str]) -> Dict:
        """
        Realiza a pesquisa completa sobre um tópico.
        
        Args:
            topic: O tópico principal para pesquisa
            keywords: Lista de palavras-chave relacionadas
            
        Returns:
            Dict com os resultados da pesquisa
        """
        try:
            self.logger.info(f"Iniciando pesquisa para: {topic}")
            
            # Pesquisa web
            web_results = self._web_search(topic)
            
            # Coleta estatísticas
            stats = self._collect_stats(topic)
            
            # Analisa conteúdo relacionado
            related_content = []
            for keyword in keywords:
                search_results = self._web_search(f"{topic} {keyword}")
                if "urls" in search_results:
                    for url in search_results["urls"][:3]:
                        analysis = self._analyze_content(url)
                        related_content.append({
                            "url": url,
                            "analysis": analysis
                        })
            
            # Compila os resultados
            results = {
                "topic": topic,
                "keywords": keywords,
                "web_results": web_results,
                "statistics": stats,
                "related_content": related_content,
                "timestamp": datetime.now().isoformat()
            }
            
            self.logger.info(f"Pesquisa concluída para: {topic}")
            return results
            
        except Exception as e:
            self.logger.log_error(e, f"Erro na pesquisa completa: {topic}")
            raise ResearchError(f"Erro ao realizar pesquisa: {str(e)}") 