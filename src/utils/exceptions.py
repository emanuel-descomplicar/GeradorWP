"""
Exceções e validações personalizadas.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

from typing import Any, Dict, List, Optional
import re

# Exceções
class WordPressError(Exception):
    """Exceção base para erros do WordPress."""
    pass

class ValidationError(Exception):
    """Exceção base para erros de validação."""
    pass

class ConfigError(Exception):
    """Exceção base para erros de configuração."""
    pass

class CacheError(Exception):
    """Exceção base para erros de cache."""
    pass

class DifyError(Exception):
    """Exceção base para erros da API Dify."""
    pass

# Validações
def validate_title(title: str) -> bool:
    """
    Valida o título de um artigo.
    
    Args:
        title: Título a ser validado
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica comprimento
    if not (10 <= len(title) <= 60):
        return False
    
    # Verifica caracteres especiais
    if re.search(r'[^\w\s\-.,!?]', title):
        return False
    
    return True

def validate_content(content: str) -> bool:
    """
    Valida o conteúdo de um artigo.
    
    Args:
        content: Conteúdo a ser validado
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica comprimento mínimo (500 palavras)
    if len(content.split()) < 500:
        return False
    
    # Verifica HTML básico
    if not re.match(r'^<[^>]+>', content):
        return False
    
    return True

def validate_excerpt(excerpt: str) -> bool:
    """
    Valida o resumo de um artigo.
    
    Args:
        excerpt: Resumo a ser validado
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica comprimento
    if not (50 <= len(excerpt) <= 160):
        return False
    
    return True

def validate_tags(tags: List[str]) -> bool:
    """
    Valida as tags de um artigo.
    
    Args:
        tags: Lista de tags a ser validada
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica quantidade
    if not (1 <= len(tags) <= 10):
        return False
    
    # Verifica cada tag
    for tag in tags:
        # Comprimento
        if not (2 <= len(tag) <= 30):
            return False
        
        # Caracteres permitidos
        if re.search(r'[^\w\s\-]', tag):
            return False
    
    return True

def validate_category(category: str) -> bool:
    """
    Valida a categoria de um artigo.
    
    Args:
        category: Categoria a ser validada
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica comprimento
    if not (2 <= len(category) <= 30):
        return False
    
    # Verifica caracteres permitidos
    if re.search(r'[^\w\s\-]', category):
        return False
    
    return True

def validate_image(image_path: str) -> bool:
    """
    Valida uma imagem.
    
    Args:
        image_path: Caminho da imagem
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica extensão
    if not image_path.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        return False
    
    return True

def validate_url(url: str) -> bool:
    """
    Valida uma URL.
    
    Args:
        url: URL a ser validada
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica formato básico
    if not re.match(r'^https?://', url):
        return False
    
    return True

def validate_html(html: str) -> bool:
    """
    Valida código HTML.
    
    Args:
        html: HTML a ser validado
        
    Returns:
        True se válido, False caso contrário
    """
    # Verifica tags abertas/fechadas
    tags = re.findall(r'<[^>]+>', html)
    stack = []
    
    for tag in tags:
        # Tag de fechamento
        if tag.startswith('</'):
            if not stack:
                return False
            if not tag[2:-1] == stack[-1]:
                return False
            stack.pop()
        # Tag de abertura
        elif not tag.endswith('/>'):
            tag_name = re.match(r'<(\w+)', tag).group(1)
            stack.append(tag_name)
    
    return len(stack) == 0

def validate_config(config: Dict[str, Any]) -> bool:
    """
    Valida configurações.
    
    Args:
        config: Dicionário de configurações
        
    Returns:
        True se válido, False caso contrário
    """
    required_keys = [
        'WP_URL',
        'WP_USERNAME',
        'WP_APP_PASSWORD',
        'DIFY_API_KEY',
        'DIFY_API_URL'
    ]
    
    # Verifica chaves obrigatórias
    for key in required_keys:
        if key not in config:
            return False
        if not config[key]:
            return False
    
    return True 