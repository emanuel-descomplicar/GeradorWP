"""
Exceções personalizadas para o GeradorWP.
"""

class GeradorWPError(Exception):
    """Classe base para exceções do GeradorWP."""
    pass

class ConfigError(GeradorWPError):
    """Erro de configuração."""
    pass

class ValidationError(GeradorWPError):
    """Erro de validação."""
    pass

class APIError(GeradorWPError):
    """Erro de API."""
    pass

class WordPressError(GeradorWPError):
    """Erro do WordPress."""
    pass

class DifyError(GeradorWPError):
    """Erro da API do Dify."""
    pass

class CacheError(GeradorWPError):
    """Erro de cache."""
    pass

class ContentError(GeradorWPError):
    """Erro de conteúdo."""
    pass

class ImageError(GeradorWPError):
    """Erro de imagem."""
    pass

class ResearchError(GeradorWPError):
    """Erro de pesquisa."""
    pass

class WritingError(GeradorWPError):
    """Erro de escrita."""
    pass

class PublishingError(GeradorWPError):
    """Erro de publicação."""
    pass 