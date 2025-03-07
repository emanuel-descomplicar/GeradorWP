"""
Testes para o módulo de configuração.
"""
import pytest
from src.config.config import (
    OPENAI_API_KEY,
    WP_URL,
    WP_USERNAME,
    WP_PASSWORD,
    DEFAULT_MODEL,
    TEMPERATURE,
    LOG_LEVEL,
    CACHE_DIR,
    CACHE_EXPIRY
)

def test_config_variables():
    """Testa se as variáveis de configuração estão definidas."""
    assert OPENAI_API_KEY is not None, "OPENAI_API_KEY não está definida"
    assert WP_URL is not None, "WP_URL não está definida"
    assert WP_USERNAME is not None, "WP_USERNAME não está definida"
    assert WP_PASSWORD is not None, "WP_PASSWORD não está definida"
    assert DEFAULT_MODEL == "gpt-4-turbo-preview", "DEFAULT_MODEL incorreto"
    assert TEMPERATURE == 0.7, "TEMPERATURE incorreta"
    assert LOG_LEVEL in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], "LOG_LEVEL inválido"
    assert CACHE_DIR == ".cache", "CACHE_DIR incorreto"
    assert CACHE_EXPIRY == 3600, "CACHE_EXPIRY incorreto" 