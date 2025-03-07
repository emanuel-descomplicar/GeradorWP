"""
Configurações do projeto GeradorWP.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

import os
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da API Dify
DIFY_API_KEY = os.getenv("DIFY_API_KEY")
DIFY_API_URL = os.getenv("DIFY_API_URL")

# Configurações do WordPress
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")
WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD")

# Configurações de Cache
CACHE_ENABLED = os.getenv("CACHE_ENABLED", "true").lower() == "true"
CACHE_EXPIRY = int(os.getenv("CACHE_EXPIRY", "3600"))
CACHE_DIR = Path(os.getenv("CACHE_DIR", "./cache"))

# Configurações de Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_DIR = Path(os.getenv("LOG_DIR", "./logs"))
LOG_FORMAT = os.getenv("LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Configurações de Pesquisa
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "10"))
SEARCH_TIMEOUT = int(os.getenv("SEARCH_TIMEOUT", "30"))
TRUSTED_SOURCES_ONLY = os.getenv("TRUSTED_SOURCES_ONLY", "true").lower() == "true"

# Configurações de Conteúdo
MIN_WORD_COUNT = int(os.getenv("MIN_WORD_COUNT", "2000"))
MAX_WORD_COUNT = int(os.getenv("MAX_WORD_COUNT", "3000"))
KEYWORD_DENSITY_MIN = float(os.getenv("KEYWORD_DENSITY_MIN", "0.5"))
KEYWORD_DENSITY_MAX = float(os.getenv("KEYWORD_DENSITY_MAX", "5.0"))

# Configurações de Validação
VALIDATE_LINKS = os.getenv("VALIDATE_LINKS", "true").lower() == "true"
VALIDATE_IMAGES = os.getenv("VALIDATE_IMAGES", "true").lower() == "true"
CHECK_PLAGIARISM = os.getenv("CHECK_PLAGIARISM", "true").lower() == "true"
VALIDATE_SEO = os.getenv("VALIDATE_SEO", "true").lower() == "true"

# Configurações de Backup
BACKUP_ENABLED = os.getenv("BACKUP_ENABLED", "true").lower() == "true"
BACKUP_DIR = Path(os.getenv("BACKUP_DIR", "./backups"))
BACKUP_RETENTION = int(os.getenv("BACKUP_RETENTION", "7"))

# Configurações de Performance
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
CONCURRENT_REQUESTS = int(os.getenv("CONCURRENT_REQUESTS", "5"))

# Criação de diretórios necessários
for directory in [CACHE_DIR, LOG_DIR, BACKUP_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Dicionário com todas as configurações
SETTINGS: Dict[str, Any] = {
    "dify": {
        "api_key": DIFY_API_KEY,
        "api_url": DIFY_API_URL
    },
    "wordpress": {
        "url": WP_URL,
        "username": WP_USERNAME,
        "password": WP_PASSWORD,
        "app_password": WP_APP_PASSWORD
    },
    "cache": {
        "enabled": CACHE_ENABLED,
        "expiry": CACHE_EXPIRY,
        "dir": CACHE_DIR
    },
    "logging": {
        "level": LOG_LEVEL,
        "dir": LOG_DIR,
        "format": LOG_FORMAT
    },
    "search": {
        "max_results": MAX_SEARCH_RESULTS,
        "timeout": SEARCH_TIMEOUT,
        "trusted_sources_only": TRUSTED_SOURCES_ONLY
    },
    "content": {
        "min_word_count": MIN_WORD_COUNT,
        "max_word_count": MAX_WORD_COUNT,
        "keyword_density_min": KEYWORD_DENSITY_MIN,
        "keyword_density_max": KEYWORD_DENSITY_MAX
    },
    "validation": {
        "validate_links": VALIDATE_LINKS,
        "validate_images": VALIDATE_IMAGES,
        "check_plagiarism": CHECK_PLAGIARISM,
        "validate_seo": VALIDATE_SEO
    },
    "backup": {
        "enabled": BACKUP_ENABLED,
        "dir": BACKUP_DIR,
        "retention": BACKUP_RETENTION
    },
    "performance": {
        "max_retries": MAX_RETRIES,
        "request_timeout": REQUEST_TIMEOUT,
        "concurrent_requests": CONCURRENT_REQUESTS
    }
} 