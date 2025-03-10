"""
Cliente para integração com a API Dify.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import json
import os
from typing import Dict, Optional
import requests
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DifyClient:
    """Cliente para a API Dify."""
    
    def __init__(self, api_key: str = None, base_url: str = None, knowledge_base_id: str = None):
        """Inicializa o cliente.
        
        Args:
            api_key: Chave da API Dify (se None, usa DIFY_API_KEY do ambiente)
            base_url: URL base da API (se None, usa DIFY_BASE_URL do ambiente)
            knowledge_base_id: ID da base de conhecimento (se None, usa DIFY_KNOWLEDGE_BASE_ID do ambiente)
        """
        self.api_key = api_key or os.getenv('DIFY_API_KEY')
        if not self.api_key:
            raise ValueError("API key não fornecida e variável de ambiente DIFY_API_KEY não encontrada.")
            
        self.base_url = base_url or os.getenv('DIFY_BASE_URL', "https://didi.descomplicar.pt/v1")
        self.knowledge_base_id = knowledge_base_id or os.getenv('DIFY_KNOWLEDGE_BASE_ID', "default")
        
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        logger.info(f"DifyClient inicializado:")
        logger.info(f"API Key: {self.api_key[:8]}...")
        logger.info(f"Base URL: {self.base_url}")
        logger.info(f"Knowledge Base ID: {self.knowledge_base_id}")
    
    def generate_content(
        self,
        prompt: str,
        min_words: int,
        max_words: Optional[int] = None,
        temperature: float = 0.7
    ) -> str:
        """Gera conteúdo usando a API Dify.
        
        Args:
            prompt: Prompt para geração
            min_words: Mínimo de palavras
            max_words: Máximo de palavras (opcional)
            temperature: Temperatura para geração (0.0 a 1.0)
            
        Returns:
            Conteúdo gerado
        """
        logger.debug(f"Gerando conteúdo:")
        logger.debug(f"Prompt: {prompt[:100]}...")
        logger.debug(f"Min words: {min_words}")
        logger.debug(f"Max words: {max_words}")
        
        payload = {
            "inputs": {
                "prompt": prompt,
                "min_words": min_words,
                "max_words": max_words,
                "temperature": temperature
            },
            "query": prompt,
            "response_mode": "blocking",
            "user": "content_generator"
        }
        
        logger.debug(f"URL: {self.base_url}/chat-messages")
        
        try:
            response = requests.post(
                f"{self.base_url}/chat-messages",
                headers=self.headers,
                json=payload
            )
            
            logger.debug(f"Status code: {response.status_code}")
            
            if response.status_code != 200:
                logger.error(f"Erro na API Dify: {response.text}")
                raise Exception(f"Erro na API Dify: {response.text}")
            
            response_data = response.json()
            if 'message' in response_data:
                return response_data['message']['content']
            elif 'answer' in response_data:
                return response_data['answer']
            else:
                logger.error(f"Formato de resposta inválido: {response.text}")
                raise Exception(f"Formato de resposta inválido: {response.text}")
            
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            raise
    
    def validate_content(self, content: str, knowledge_base_id: str = None) -> Dict:
        """Valida conteúdo usando a base de conhecimento Dify.
        
        Args:
            content: Conteúdo para validar
            knowledge_base_id: ID da base de conhecimento (se None, usa o valor padrão do cliente)
            
        Returns:
            Dict com resultados da validação
        """
        kb_id = knowledge_base_id or self.knowledge_base_id
        logger.debug(f"Validando conteúdo:")
        logger.debug(f"Content: {content[:100]}...")
        logger.debug(f"Knowledge base ID: {kb_id}")
        
        payload = {
            "inputs": {
                "content": content,
                "knowledge_base_id": kb_id
            },
            "query": f"Validar conteúdo: {content[:100]}...",
            "response_mode": "blocking",
            "user": "content_validator"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat-messages",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Erro na API Dify: {response.text}")
                raise Exception(f"Erro na API Dify: {response.text}")
            
            response_data = response.json()
            if 'message' in response_data:
                return {'result': response_data['message']['content']}
            elif 'answer' in response_data:
                return {'result': response_data['answer']}
            else:
                logger.error(f"Formato de resposta inválido: {response.text}")
                raise Exception(f"Formato de resposta inválido: {response.text}")
            
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            raise
    
    def get_similar_content(
        self,
        query: str,
        knowledge_base_id: str = None,
        limit: int = 5
    ) -> Dict:
        """Busca conteúdo similar na base de conhecimento.
        
        Args:
            query: Texto para busca
            knowledge_base_id: ID da base de conhecimento (se None, usa o valor padrão do cliente)
            limit: Limite de resultados
            
        Returns:
            Dict com resultados similares
        """
        kb_id = knowledge_base_id or self.knowledge_base_id
        logger.debug(f"Buscando conteúdo similar:")
        logger.debug(f"Query: {query}")
        logger.debug(f"Knowledge base ID: {kb_id}")
        logger.debug(f"Limit: {limit}")
        
        payload = {
            "inputs": {
                "query": query,
                "knowledge_base_id": kb_id,
                "limit": limit
            },
            "query": f"Buscar conteúdo similar: {query}",
            "response_mode": "blocking",
            "user": "content_searcher"
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/chat-messages",
                headers=self.headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"Erro na API Dify: {response.text}")
                raise Exception(f"Erro na API Dify: {response.text}")
            
            response_data = response.json()
            if 'message' in response_data:
                return {'results': [{'content': response_data['message']['content']}]}
            elif 'answer' in response_data:
                return {'results': [{'content': response_data['answer']}]}
            else:
                logger.error(f"Formato de resposta inválido: {response.text}")
                raise Exception(f"Formato de resposta inválido: {response.text}")
            
        except Exception as e:
            logger.error(f"Erro na requisição: {str(e)}")
            raise 