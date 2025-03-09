"""
Módulo para integração com a API do Dify.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import requests
from typing import Dict, Any, Optional, List
from dotenv import load_dotenv
from .exceptions import DifyError

load_dotenv()

class DifyClient:
    """Cliente para integração com a API do Dify."""

    def __init__(self):
        """Inicializa o cliente Dify com as credenciais do .env."""
        self.api_key = os.getenv('DIFY_API_KEY')
        self.api_url = os.getenv('DIFY_API_URL')
        
        if not self.api_key or not self.api_url:
            raise ValueError("DIFY_API_KEY e DIFY_API_URL devem estar definidos no arquivo .env")

        self.headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }

    def chat_completion(
        self,
        messages: list,
        temperature: float = 0.3,  # Reduzido para maior precisão
        top_p: float = 0.95,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Realiza uma chamada à API do Dify para completar um chat.
        Usa temperatura baixa (0.3) para garantir respostas mais precisas e factuais,
        aproveitando a base de conhecimento da Dify.

        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "mensagem"}]
            temperature: Controla a precisão das respostas (0.3 para maior precisão)
            top_p: Controla a diversidade das respostas (0.0 a 1.0)
            presence_penalty: Penalidade para repetição de tópicos (-2.0 a 2.0)
            frequency_penalty: Penalidade para repetição de tokens (-2.0 a 2.0)
            max_tokens: Número máximo de tokens na resposta

        Returns:
            Dict com a resposta da API
        """
        endpoint = f"{self.api_url}/chat-messages"
        
        # Extrair a query do último message
        query = ""
        for msg in reversed(messages):
            if msg.get("role") == "user":
                query = msg.get("content", "")
                break
        
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "default"
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise DifyError(f"Erro na chamada à API do Dify: {str(e)}")

    def completion(
        self,
        prompt: str,
        temperature: float = 0.3,  # Reduzido para maior precisão
        max_tokens: Optional[int] = None,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0
    ) -> Dict[str, Any]:
        """
        Realiza uma chamada à API do Dify para completar um texto.
        Usa temperatura baixa (0.3) para garantir respostas mais precisas e factuais,
        aproveitando a base de conhecimento da Dify.

        Args:
            prompt: O texto para completar
            temperature: Controla a precisão das respostas (0.3 para maior precisão)
            max_tokens: Número máximo de tokens na resposta
            top_p: Controla a diversidade das respostas (0.0 a 1.0)
            frequency_penalty: Penalidade para repetição de tokens (-2.0 a 2.0)
            presence_penalty: Penalidade para repetição de tópicos (-2.0 a 2.0)

        Returns:
            Dict com a resposta da API
        """
        endpoint = f"{self.api_url}/completion-messages"
        
        payload = {
            "inputs": {},
            "query": prompt,
            "response_mode": "blocking",
            "user": "default"
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            return {
                "choices": [{
                    "text": data.get("answer", ""),
                    "finish_reason": "stop"
                }]
            }
        except requests.exceptions.RequestException as e:
            raise DifyError(f"Erro na chamada à API do Dify: {str(e)}")

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Gera texto usando a API do Dify.
        Usa temperatura baixa por padrão para garantir precisão e factualidade.

        Args:
            prompt: O prompt para gerar o texto
            **kwargs: Argumentos adicionais para a API

        Returns:
            str: O texto gerado
        """
        try:
            # Define temperatura baixa por padrão se não especificada
            if 'temperature' not in kwargs:
                kwargs['temperature'] = 0.3
                
            response = self.completion(prompt, **kwargs)
            return response["choices"][0]["text"]
        except Exception as e:
            raise DifyError(f"Erro ao gerar texto: {str(e)}")

    def analyze_text(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Analisa um texto usando a API do Dify.
        Usa temperatura baixa por padrão para garantir análise precisa.

        Args:
            text: O texto para analisar
            **kwargs: Argumentos adicionais para a API

        Returns:
            Dict com a análise do texto
        """
        prompt = f"Analise o seguinte texto:\n\n{text}"
        try:
            # Define temperatura baixa por padrão se não especificada
            if 'temperature' not in kwargs:
                kwargs['temperature'] = 0.3
                
            response = self.completion(prompt, **kwargs)
            return {"analysis": response["choices"][0]["text"]}
        except Exception as e:
            raise DifyError(f"Erro ao analisar texto: {str(e)}")

    def generate_image(
        self,
        prompt: str,
        size: str = "1024x1024",
        quality: str = "standard",
        style: str = "natural"
    ) -> Dict[str, Any]:
        """
        Gera uma imagem usando a API do Dify.

        Args:
            prompt: Descrição da imagem
            size: Tamanho da imagem (1024x1024, 512x512, etc.)
            quality: Qualidade da imagem (standard, hd)
            style: Estilo da imagem (natural, vivid)

        Returns:
            Dict com a URL da imagem gerada
        """
        endpoint = f"{self.api_url}/images/generations"
        
        payload = {
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "style": style,
            "response_format": "url"
        }

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            return {"url": data.get("data", [{}])[0].get("url", "")}
        except requests.exceptions.RequestException as e:
            raise DifyError(f"Erro na geração de imagem: {str(e)}") 