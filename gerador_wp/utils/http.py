"""
Cliente HTTP com retry e cache para o GeradorWP.
"""

import time
from typing import Any, Dict, Optional, Union
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .cache import Cache
from .logger import Logger
from ..config.config import (
    REQUEST_TIMEOUT,
    MAX_RETRIES,
    RETRY_DELAY
)

class HttpClient:
    """Classe para fazer requisições HTTP com retry e cache."""
    
    def __init__(self):
        """Inicializa o cliente HTTP."""
        self.cache = Cache()
        self.logger = Logger(__name__)
        
        # Configura o retry
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY,
            status_forcelist=[500, 502, 503, 504]
        )
        
        # Configura a sessão
        self.session = requests.Session()
        self.session.mount("http://", HTTPAdapter(max_retries=retry_strategy))
        self.session.mount("https://", HTTPAdapter(max_retries=retry_strategy))
    
    def get(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        cache_key: Optional[str] = None,
        use_cache: bool = True
    ) -> Dict[str, Any]:
        """
        Faz uma requisição GET.
        
        Args:
            url: URL da requisição
            params: Parâmetros da query string
            headers: Cabeçalhos da requisição
            cache_key: Chave para cache
            use_cache: Se deve usar cache
            
        Returns:
            Resposta da requisição
        """
        start_time = time.time()
        
        try:
            # Tenta recuperar do cache
            if use_cache and cache_key:
                cached_response = self.cache.get(cache_key)
                if cached_response:
                    self.logger.debug(f"Cache hit para {url}")
                    return cached_response
            
            # Faz a requisição
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Registra a requisição
            self.logger.log_request(
                "GET",
                url,
                response.status_code,
                time.time() - start_time
            )
            
            # Verifica o status
            response.raise_for_status()
            
            # Processa a resposta
            result = response.json()
            
            # Armazena no cache
            if use_cache and cache_key:
                self.cache.set(cache_key, result)
            
            return result
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, f"Erro na requisição GET para {url}")
            raise
    
    def post(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição POST.
        
        Args:
            url: URL da requisição
            data: Dados do formulário
            json: Dados JSON
            headers: Cabeçalhos da requisição
            
        Returns:
            Resposta da requisição
        """
        start_time = time.time()
        
        try:
            # Faz a requisição
            response = self.session.post(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Registra a requisição
            self.logger.log_request(
                "POST",
                url,
                response.status_code,
                time.time() - start_time
            )
            
            # Verifica o status
            response.raise_for_status()
            
            # Processa a resposta
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, f"Erro na requisição POST para {url}")
            raise
    
    def put(
        self,
        url: str,
        data: Optional[Union[Dict[str, Any], str]] = None,
        json: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição PUT.
        
        Args:
            url: URL da requisição
            data: Dados do formulário
            json: Dados JSON
            headers: Cabeçalhos da requisição
            
        Returns:
            Resposta da requisição
        """
        start_time = time.time()
        
        try:
            # Faz a requisição
            response = self.session.put(
                url,
                data=data,
                json=json,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Registra a requisição
            self.logger.log_request(
                "PUT",
                url,
                response.status_code,
                time.time() - start_time
            )
            
            # Verifica o status
            response.raise_for_status()
            
            # Processa a resposta
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, f"Erro na requisição PUT para {url}")
            raise
    
    def delete(
        self,
        url: str,
        headers: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Faz uma requisição DELETE.
        
        Args:
            url: URL da requisição
            headers: Cabeçalhos da requisição
            
        Returns:
            Resposta da requisição
        """
        start_time = time.time()
        
        try:
            # Faz a requisição
            response = self.session.delete(
                url,
                headers=headers,
                timeout=REQUEST_TIMEOUT
            )
            
            # Registra a requisição
            self.logger.log_request(
                "DELETE",
                url,
                response.status_code,
                time.time() - start_time
            )
            
            # Verifica o status
            response.raise_for_status()
            
            # Processa a resposta
            return response.json()
            
        except requests.exceptions.RequestException as e:
            self.logger.log_error(e, f"Erro na requisição DELETE para {url}")
            raise 