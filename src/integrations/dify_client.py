#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Cliente para integração com a API Dify.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
from typing import Dict, Optional
import requests
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

# Configuração do logging
logger = logging.getLogger(__name__)

class DifyClient:
    """Cliente para interação com a API Dify."""
    
    def __init__(self, api_key: str = None, base_url: str = None, knowledge_base_id: str = None):
        """Inicializa o cliente Dify.
        
        Args:
            api_key: Chave de API do Dify (se None, usa DIFY_API_KEY do .env)
            base_url: URL base da API (se None, usa DIFY_API_URL do .env)
            knowledge_base_id: ID da base de conhecimento (se None, usa DIFY_KNOWLEDGE_BASE_ID do .env)
        """
        self.api_key = api_key or os.getenv('DIFY_API_KEY')
        self.base_url = base_url or os.getenv('DIFY_API_URL')
        self.knowledge_base_id = knowledge_base_id or os.getenv('DIFY_KNOWLEDGE_BASE_ID')
        
        if not all([self.api_key, self.base_url, self.knowledge_base_id]):
            raise ValueError("Credenciais Dify incompletas. Verifique as variáveis de ambiente.")
        
        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        logger.info(f"DifyClient inicializado com base_url: {self.base_url}")
        logger.debug(f"Headers: {json.dumps(self.headers, indent=2)}")
    
    def generate_content(self, prompt: str, conversation_id: Optional[str] = None) -> Dict:
        """Gera conteúdo usando a API Dify.
        
        Args:
            prompt: Prompt para geração de conteúdo
            conversation_id: ID da conversa para continuidade (opcional)
        
        Returns:
            Resposta da API com o conteúdo gerado
        """
        endpoint = f"{self.base_url}/chat-messages"
        
        payload = {
            "inputs": {},
            "query": prompt,
            "user": "gerador-wp",
            "stream": False,
            "conversation_id": conversation_id,
            "knowledge_base_id": self.knowledge_base_id
        }
        
        logger.debug(f"Enviando requisição para {endpoint}")
        logger.debug(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            
            # Log da resposta
            logger.debug(f"Status code: {response.status_code}")
            logger.debug(f"Response headers: {json.dumps(dict(response.headers), indent=2)}")
            logger.debug(f"Response body: {response.text}")
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao gerar conteúdo: {str(e)}")
            if hasattr(e.response, 'text'):
                logger.error(f"Detalhes do erro: {e.response.text}")
            raise
    
    def get_similar_content(self, query: str, limit: int = 5) -> Dict:
        """Busca conteúdo similar na base de conhecimento.
        
        Args:
            query: Texto para busca
            limit: Número máximo de resultados
        
        Returns:
            Lista de conteúdos similares
        """
        endpoint = f"{self.base_url}/knowledge-base/{self.knowledge_base_id}/search"
        
        payload = {
            "query": query,
            "limit": limit
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao buscar conteúdo similar: {str(e)}")
            raise
    
    def validate_content(self, content: str) -> Dict:
        """Valida o conteúdo gerado usando critérios predefinidos.
        
        Args:
            content: Conteúdo a ser validado
        
        Returns:
            Resultado da validação
        """
        endpoint = f"{self.base_url}/validate"
        
        payload = {
            "content": content,
            "knowledge_base_id": self.knowledge_base_id
        }
        
        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro ao validar conteúdo: {str(e)}")
            raise