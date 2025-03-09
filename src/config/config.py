"""
Configurações do projeto GeradorWP.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações da API Dify
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL")

# Configurações do WordPress
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Configurações de cache
CACHE_TTL = int(os.getenv("CACHE_TTL", "3600"))  # 1 hora
CACHE_DIR = os.getenv("CACHE_DIR", ".cache")

# Configurações de requisições
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "5"))

# Configurações de logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "gerador-wp.log")

# Configurações de conteúdo
MIN_CONTENT_LENGTH = int(os.getenv("MIN_CONTENT_LENGTH", "1000"))
MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", "5000"))
DEFAULT_CATEGORY = os.getenv("DEFAULT_CATEGORY", "Blog")
DEFAULT_TAGS = os.getenv("DEFAULT_TAGS", "").split(",")

def validate_config() -> None:
    """
    Valida as configurações do projeto.
    
    Raises:
        ValueError: Se alguma configuração obrigatória estiver faltando
    """
    required_vars = {
        "DIFY_API_KEY": DIFY_API_KEY,
        "DIFY_API_URL": DIFY_API_URL,
        "WP_URL": WP_URL,
        "WP_USERNAME": WP_USERNAME,
        "WP_APP_PASSWORD": WP_APP_PASSWORD
    }
    
    missing_vars = [
        var for var, value in required_vars.items()
        if not value
    ]
    
    if missing_vars:
        raise ValueError(
            f"Configurações obrigatórias faltando: {', '.join(missing_vars)}"
        )
    
    # Valida URLs
    if not WP_URL.startswith(("http://", "https://")):
        raise ValueError("WP_URL deve começar com http:// ou https://")
    
    # Valida comprimentos de conteúdo
    if MIN_CONTENT_LENGTH > MAX_CONTENT_LENGTH:
        raise ValueError(
            "MIN_CONTENT_LENGTH não pode ser maior que MAX_CONTENT_LENGTH"
        )
    
    # Valida timeouts e retries
    if REQUEST_TIMEOUT <= 0:
        raise ValueError("REQUEST_TIMEOUT deve ser maior que 0")
    if MAX_RETRIES < 0:
        raise ValueError("MAX_RETRIES não pode ser negativo")
    if RETRY_DELAY < 0:
        raise ValueError("RETRY_DELAY não pode ser negativo")

# Configurações de SEO
DEFAULT_META_DESCRIPTION_LENGTH = int(os.getenv('DEFAULT_META_DESCRIPTION_LENGTH', '160'))
DEFAULT_TITLE_LENGTH = int(os.getenv('DEFAULT_TITLE_LENGTH', '60'))

# Configurações de Imagens
IMAGE_WIDTH = int(os.getenv('IMAGE_WIDTH', '1200'))
IMAGE_HEIGHT = int(os.getenv('IMAGE_HEIGHT', '630'))
IMAGE_QUALITY = int(os.getenv('IMAGE_QUALITY', '90')) 