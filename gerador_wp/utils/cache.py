"""
Sistema de cache para o GeradorWP.
"""

import os
import json
import time
from typing import Any, Dict, Optional
from datetime import datetime

from ..config.config import CACHE_TTL, CACHE_DIR

class Cache:
    """Classe para gerenciar o cache do sistema."""
    
    def __init__(self):
        """Inicializa o sistema de cache."""
        self.cache_dir = CACHE_DIR
        self.cache_ttl = CACHE_TTL
        
        # Cria o diretório de cache se não existir
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
    
    def _get_cache_path(self, key: str) -> str:
        """
        Retorna o caminho do arquivo de cache para uma chave.
        
        Args:
            key: Chave do cache
            
        Returns:
            Caminho do arquivo de cache
        """
        return os.path.join(self.cache_dir, f"{key}.json")
    
    def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Recupera um valor do cache.
        
        Args:
            key: Chave do cache
            
        Returns:
            Valor do cache ou None se não existir ou estiver expirado
        """
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            return None
        
        try:
            with open(cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                
            # Verifica se o cache expirou
            if time.time() - data["timestamp"] > self.cache_ttl:
                self.delete(key)
                return None
                
            return data["value"]
            
        except Exception:
            return None
    
    def set(self, key: str, value: Dict[str, Any]) -> None:
        """
        Armazena um valor no cache.
        
        Args:
            key: Chave do cache
            value: Valor a ser armazenado
        """
        cache_path = self._get_cache_path(key)
        
        try:
            data = {
                "timestamp": time.time(),
                "value": value
            }
            
            with open(cache_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                
        except Exception:
            pass
    
    def delete(self, key: str) -> None:
        """
        Remove um valor do cache.
        
        Args:
            key: Chave do cache
        """
        cache_path = self._get_cache_path(key)
        
        if os.path.exists(cache_path):
            try:
                os.remove(cache_path)
            except Exception:
                pass
    
    def clear(self) -> None:
        """Remove todos os valores do cache."""
        try:
            for filename in os.listdir(self.cache_dir):
                if filename.endswith(".json"):
                    os.remove(os.path.join(self.cache_dir, filename))
        except Exception:
            pass
    
    def cleanup(self) -> None:
        """Remove todos os valores expirados do cache."""
        try:
            for filename in os.listdir(self.cache_dir):
                if not filename.endswith(".json"):
                    continue
                    
                cache_path = os.path.join(self.cache_dir, filename)
                
                try:
                    with open(cache_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                        
                    if time.time() - data["timestamp"] > self.cache_ttl:
                        os.remove(cache_path)
                        
                except Exception:
                    os.remove(cache_path)
                    
        except Exception:
            pass 