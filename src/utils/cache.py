"""
Cache - Sistema de cache para o projeto

Este módulo fornece um sistema de cache para armazenar temporariamente resultados
de operações custosas, como pesquisas na web ou chamadas de API.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import time
import logging
import hashlib
from typing import Dict, Any, Optional, Union, Callable
from pathlib import Path
from functools import wraps

class Cache:
    """
    Sistema de cache para armazenar e recuperar dados.
    
    Esta classe implementa um sistema de cache em disco para armazenar
    resultados de operações custosas, com suporte a TTL (time-to-live).
    """
    
    def __init__(self, cache_dir: str = "cache", ttl: int = 86400, enabled: bool = True):
        """
        Inicializa o sistema de cache.
        
        Args:
            cache_dir: Diretório onde os arquivos de cache serão armazenados
            ttl: Tempo de vida dos itens em cache, em segundos (padrão: 1 dia)
            enabled: Se True, o cache está ativo; caso contrário, sempre retorna miss
        """
        self.logger = logging.getLogger(__name__)
        self.cache_dir = Path(cache_dir)
        self.ttl = ttl
        self.enabled = enabled
        
        # Criar diretório de cache se não existir
        if enabled and not self.cache_dir.exists():
            self.cache_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Diretório de cache criado: {self.cache_dir}")
        
        self.logger.info(f"Sistema de cache inicializado (enabled={enabled}, ttl={ttl}s)")
    
    def _get_cache_file(self, key: str) -> Path:
        """
        Obtém o caminho para o arquivo de cache de uma chave.
        
        Args:
            key: A chave do item
            
        Returns:
            Path para o arquivo de cache
        """
        # Criar hash da chave para evitar caracteres inválidos no filesystem
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{hashed_key}.json"
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Recupera um item do cache, se existir e não tiver expirado.
        
        Args:
            key: A chave do item
            default: Valor padrão a retornar se o item não for encontrado
            
        Returns:
            O item do cache ou o valor padrão
        """
        if not self.enabled:
            return default
        
        cache_file = self._get_cache_file(key)
        
        # Verificar se o arquivo existe
        if not cache_file.exists():
            self.logger.debug(f"Cache miss para chave: {key}")
            return default
        
        try:
            # Carregar dados do cache
            with open(cache_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            # Verificar expiração
            if time.time() > data.get("expires_at", 0):
                self.logger.debug(f"Cache expirado para chave: {key}")
                # Remover arquivo expirado
                os.remove(cache_file)
                return default
            
            self.logger.debug(f"Cache hit para chave: {key}")
            return data.get("value")
            
        except (json.JSONDecodeError, OSError) as e:
            self.logger.warning(f"Erro ao ler cache para chave {key}: {str(e)}")
            return default
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Armazena um item no cache.
        
        Args:
            key: A chave do item
            value: O valor a ser armazenado
            ttl: Tempo de vida em segundos (se None, usa o TTL global)
            
        Returns:
            True se o item foi armazenado com sucesso, False caso contrário
        """
        if not self.enabled:
            return False
        
        cache_file = self._get_cache_file(key)
        ttl = ttl if ttl is not None else self.ttl
        
        try:
            # Preparar dados para salvar
            data = {
                "key": key,
                "value": value,
                "created_at": time.time(),
                "expires_at": time.time() + ttl
            }
            
            # Salvar no arquivo
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            self.logger.debug(f"Item armazenado em cache: {key} (TTL: {ttl}s)")
            return True
            
        except (OSError, TypeError) as e:
            self.logger.warning(f"Erro ao armazenar em cache para chave {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """
        Remove um item do cache.
        
        Args:
            key: A chave do item a ser removido
            
        Returns:
            True se o item foi removido com sucesso, False caso contrário
        """
        if not self.enabled:
            return False
        
        cache_file = self._get_cache_file(key)
        
        # Verificar se o arquivo existe
        if not cache_file.exists():
            return False
        
        try:
            # Remover arquivo
            os.remove(cache_file)
            self.logger.debug(f"Item removido do cache: {key}")
            return True
            
        except OSError as e:
            self.logger.warning(f"Erro ao remover do cache para chave {key}: {str(e)}")
            return False
    
    def clear(self) -> int:
        """
        Limpa todo o cache.
        
        Returns:
            Número de itens removidos
        """
        if not self.enabled or not self.cache_dir.exists():
            return 0
        
        count = 0
        try:
            # Remover todos os arquivos de cache
            for cache_file in self.cache_dir.glob("*.json"):
                os.remove(cache_file)
                count += 1
            
            self.logger.info(f"Cache limpo: {count} itens removidos")
            return count
            
        except OSError as e:
            self.logger.warning(f"Erro ao limpar cache: {str(e)}")
            return count
    
    def clean_expired(self) -> int:
        """
        Remove todos os itens expirados do cache.
        
        Returns:
            Número de itens expirados removidos
        """
        if not self.enabled or not self.cache_dir.exists():
            return 0
        
        count = 0
        now = time.time()
        
        try:
            # Verificar cada arquivo de cache
            for cache_file in self.cache_dir.glob("*.json"):
                try:
                    with open(cache_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # Remover se expirado
                    if now > data.get("expires_at", 0):
                        os.remove(cache_file)
                        count += 1
                except:
                    # Se houver erro ao ler o arquivo, considerá-lo inválido e remover
                    os.remove(cache_file)
                    count += 1
            
            if count > 0:
                self.logger.info(f"Limpeza de cache: {count} itens expirados removidos")
            return count
            
        except OSError as e:
            self.logger.warning(f"Erro ao limpar itens expirados: {str(e)}")
            return count

def cached(ttl: Optional[int] = None, key_func: Optional[Callable] = None):
    """
    Decorador para cachear resultados de funções.
    
    Args:
        ttl: Tempo de vida em segundos (se None, usa o TTL global do cache)
        key_func: Função opcional para gerar a chave do cache com base nos argumentos
        
    Returns:
        Decorador para aplicar em funções
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Obter instância de cache global
            from src.config.settings import get_settings
            settings = get_settings()
            cache = settings.get_cache()
            
            # Se cache desativado, apenas executar a função
            if not cache.enabled:
                return func(*args, **kwargs)
            
            # Determinar chave do cache
            if key_func:
                key = key_func(*args, **kwargs)
            else:
                # Chave padrão: nome_da_funcao:hash_dos_argumentos
                args_str = str(args) + str(sorted(kwargs.items()))
                args_hash = hashlib.md5(args_str.encode()).hexdigest()
                key = f"{func.__module__}.{func.__name__}:{args_hash}"
            
            # Verificar cache
            cached_result = cache.get(key)
            if cached_result is not None:
                return cached_result
            
            # Executar função e armazenar resultado
            result = func(*args, **kwargs)
            cache.set(key, result, ttl)
            return result
            
        return wrapper
    return decorator 