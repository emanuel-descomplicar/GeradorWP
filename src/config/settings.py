"""
Settings - Configurações do projeto

Este módulo fornece acesso centralizado a todas as configurações do projeto,
com suporte a carregar configurações de arquivos e variáveis de ambiente.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
from typing import Dict, Any, Optional
from dotenv import load_dotenv
from pathlib import Path

from src.utils.cache import Cache

# Carregar variáveis de ambiente
load_dotenv()

class Settings:
    """
    Gerenciador de configurações do projeto.
    
    Esta classe centraliza todas as configurações utilizadas pelo sistema,
    carregando de diversas fontes (arquivos, ambiente, padrões) e fornecendo
    acesso consistente a elas.
    """
    
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        """Implementa padrão Singleton."""
        if cls._instance is None:
            cls._instance = super(Settings, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, config_file: str = None):
        """
        Inicializa o gerenciador de configurações.
        
        Args:
            config_file: Caminho opcional para arquivo de configuração JSON/YAML
        """
        # Evitar reinicialização no Singleton
        if self._initialized:
            return
        
        self.logger = logging.getLogger(__name__)
        self.config_file = config_file
        self.config = {}
        self._cache = None
        
        # Carregar configurações padrão
        self._load_default_config()
        
        # Carregar configurações de arquivo se fornecido
        if config_file:
            self._load_from_file(config_file)
        
        # Sobrescrever com variáveis de ambiente
        self._load_from_env()
        
        self._initialized = True
        self.logger.info("Configurações carregadas")
    
    def _load_default_config(self):
        """Carrega as configurações padrão."""
        self.config = {
            # Configurações gerais
            "app_name": "GeradorWP",
            "version": "0.1.0",
            
            # Configurações de logging
            "logging": {
                "level": "INFO",
                "file": "geradorwp.log",
                "console": True
            },
            
            # Configurações de cache
            "cache": {
                "enabled": True,
                "dir": "cache",
                "ttl": 86400  # 1 dia em segundos
            },
            
            # Configurações WordPress
            "wordpress": {
                "url": os.getenv("WP_URL", ""),
                "username": os.getenv("WP_USERNAME", ""),
                "password": os.getenv("WP_PASSWORD", "") or os.getenv("WP_APP_PASSWORD", "")
            },
            
            # Configurações de API
            "api": {
                "dify": {
                    "api_key": os.getenv("DIFY_API_KEY", ""),
                    "api_url": os.getenv("DIFY_API_URL", "")
                },
                "openai": {
                    "api_key": os.getenv("OPENAI_API_KEY", ""),
                    "model": "gpt-4"
                }
            },
            
            # Configurações de conteúdo
            "content": {
                "min_word_count": 2000,
                "max_word_count": 3000,
                "use_acida_model": True,
                "seo_min_score": 80
            },
            
            # Configurações de pesquisa
            "research": {
                "min_sources": 5,
                "max_sources": 15,
                "min_source_quality": 0.7
            },
            
            # Configurações de publicação
            "publishing": {
                "default_status": "draft",
                "validate_before_publish": True,
                "verify_after_publish": True,
                "add_featured_image": True
            }
        }
    
    def _load_from_file(self, file_path: str):
        """
        Carrega configurações de um arquivo JSON ou YAML.
        
        Args:
            file_path: Caminho para o arquivo de configuração
        """
        try:
            path = Path(file_path)
            
            if not path.exists():
                self.logger.warning(f"Arquivo de configuração não encontrado: {file_path}")
                return
            
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    import yaml
                    loaded_config = yaml.safe_load(f)
                else:
                    loaded_config = json.load(f)
            
            # Atualizar configurações recursivamente
            self._update_dict_recursive(self.config, loaded_config)
            self.logger.info(f"Configurações carregadas do arquivo: {file_path}")
            
        except Exception as e:
            self.logger.error(f"Erro ao carregar configurações do arquivo {file_path}: {str(e)}")
    
    def _load_from_env(self):
        """Carrega configurações de variáveis de ambiente."""
        # WordPress
        if os.getenv("WP_URL"):
            self.config["wordpress"]["url"] = os.getenv("WP_URL")
        if os.getenv("WP_USERNAME"):
            self.config["wordpress"]["username"] = os.getenv("WP_USERNAME")
        if os.getenv("WP_PASSWORD") or os.getenv("WP_APP_PASSWORD"):
            self.config["wordpress"]["password"] = os.getenv("WP_PASSWORD") or os.getenv("WP_APP_PASSWORD")
        
        # Dify API
        if os.getenv("DIFY_API_KEY"):
            self.config["api"]["dify"]["api_key"] = os.getenv("DIFY_API_KEY")
        if os.getenv("DIFY_API_URL"):
            self.config["api"]["dify"]["api_url"] = os.getenv("DIFY_API_URL")
        
        # OpenAI API
        if os.getenv("OPENAI_API_KEY"):
            self.config["api"]["openai"]["api_key"] = os.getenv("OPENAI_API_KEY")
        if os.getenv("OPENAI_MODEL"):
            self.config["api"]["openai"]["model"] = os.getenv("OPENAI_MODEL")
        
        # Logging
        if os.getenv("LOG_LEVEL"):
            self.config["logging"]["level"] = os.getenv("LOG_LEVEL")
        if os.getenv("LOG_FILE"):
            self.config["logging"]["file"] = os.getenv("LOG_FILE")
    
    def _update_dict_recursive(self, original: Dict, update: Dict):
        """
        Atualiza um dicionário recursivamente.
        
        Args:
            original: Dicionário original a ser atualizado
            update: Dicionário com atualizações
        """
        for key, value in update.items():
            if key in original and isinstance(original[key], dict) and isinstance(value, dict):
                self._update_dict_recursive(original[key], value)
            else:
                original[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém uma configuração pelo caminho de chaves.
        
        Args:
            key: Caminho de chaves separadas por ponto (e.g., "wordpress.url")
            default: Valor padrão a retornar se a configuração não for encontrada
            
        Returns:
            Valor da configuração ou padrão se não encontrada
        """
        keys = key.split('.')
        config = self.config
        
        try:
            for k in keys:
                config = config[k]
            return config
        except (KeyError, TypeError):
            return default
    
    def get_all(self) -> Dict[str, Any]:
        """
        Obtém todas as configurações.
        
        Returns:
            Dicionário com todas as configurações
        """
        return self.config.copy()
    
    def get_cache(self) -> Cache:
        """
        Obtém a instância de cache.
        
        Returns:
            Instância de Cache configurada
        """
        if self._cache is None:
            cache_config = self.config.get("cache", {})
            self._cache = Cache(
                cache_dir=cache_config.get("dir", "cache"),
                ttl=cache_config.get("ttl", 86400),
                enabled=cache_config.get("enabled", True)
            )
        return self._cache
    
    def reload(self):
        """Recarrega todas as configurações."""
        self._load_default_config()
        if self.config_file:
            self._load_from_file(self.config_file)
        self._load_from_env()
        self.logger.info("Configurações recarregadas")

# Instância global de configurações
_settings_instance = None

def get_settings(config_file: str = None) -> Settings:
    """
    Obtém a instância global de configurações.
    
    Args:
        config_file: Caminho opcional para arquivo de configuração
        
    Returns:
        Instância de Settings
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings(config_file)
    return _settings_instance 