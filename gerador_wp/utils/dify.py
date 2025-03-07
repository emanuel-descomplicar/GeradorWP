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
        temperature: float = 0.7,
        top_p: float = 0.95,
        presence_penalty: float = 0,
        frequency_penalty: float = 0,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Realiza uma chamada à API do Dify para completar um chat.

        Args:
            messages: Lista de mensagens no formato [{"role": "user", "content": "mensagem"}]
            temperature: Controla a aleatoriedade das respostas (0.0 a 1.0)
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
        if messages and len(messages) > 0:
            last_message = messages[-1]
            if last_message.get("role") == "user":
                query = last_message.get("content", "")
        
        payload = {
            "inputs": {},
            "query": query,
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "default"
        }

        # Adicionar parâmetros opcionais
        if temperature != 0.7 or top_p != 0.95 or presence_penalty != 0 or frequency_penalty != 0 or max_tokens:
            payload["parameters"] = {}
            
            if temperature != 0.7:
                payload["parameters"]["temperature"] = temperature
            
            if top_p != 0.95:
                payload["parameters"]["top_p"] = top_p
            
            if presence_penalty != 0:
                payload["parameters"]["presence_penalty"] = presence_penalty
            
            if frequency_penalty != 0:
                payload["parameters"]["frequency_penalty"] = frequency_penalty
            
            if max_tokens:
                payload["parameters"]["max_tokens"] = max_tokens

        try:
            response = requests.post(endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Erro na chamada à API do Dify: {str(e)}")

    def completion(
        self,
        prompt: str,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        top_p: float = 0.95,
        frequency_penalty: float = 0,
        presence_penalty: float = 0
    ) -> Dict[str, Any]:
        """
        Realiza uma chamada à API do Dify para completar um texto.

        Args:
            prompt: O texto para completar
            temperature: Controla a aleatoriedade das respostas (0.0 a 1.0)
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

        # Adicionar parâmetros opcionais
        if temperature != 0.7 or top_p != 0.95 or presence_penalty != 0 or frequency_penalty != 0 or max_tokens:
            payload["parameters"] = {}
            
            if temperature != 0.7:
                payload["parameters"]["temperature"] = temperature
            
            if top_p != 0.95:
                payload["parameters"]["top_p"] = top_p
            
            if presence_penalty != 0:
                payload["parameters"]["presence_penalty"] = presence_penalty
            
            if frequency_penalty != 0:
                payload["parameters"]["frequency_penalty"] = frequency_penalty
            
            if max_tokens:
                payload["parameters"]["max_tokens"] = max_tokens

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
            raise Exception(f"Erro na chamada à API do Dify: {str(e)}")

    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Gera texto usando a API do Dify.

        Args:
            prompt: O prompt para gerar o texto
            **kwargs: Argumentos adicionais para a API

        Returns:
            str: O texto gerado
        """
        response = self.completion(prompt, **kwargs)
        
        if 'choices' in response and len(response['choices']) > 0:
            return response['choices'][0]['text']
        else:
            raise Exception("Resposta da API do Dify não contém texto gerado")

    def analyze_text(self, text: str, **kwargs) -> Dict[str, Any]:
        """
        Analisa um texto usando a API do Dify.

        Args:
            text: O texto para analisar
            **kwargs: Argumentos adicionais para a API

        Returns:
            Dict com a análise do texto
        """
        prompt = f"Analise o seguinte texto:\n\n{text}"
        return self.completion(prompt, **kwargs)

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
            raise Exception(f"Erro na geração de imagem: {str(e)}") 