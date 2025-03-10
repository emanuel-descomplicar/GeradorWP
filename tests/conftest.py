"""
Configuração dos testes do GeradorWP.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import pytest
from pathlib import Path
import sys

# Adicionar diretório raiz ao PYTHONPATH
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

@pytest.fixture
def test_data_dir():
    """Retorna o diretório de dados de teste."""
    return Path(__file__).parent / 'data'

@pytest.fixture
def sample_article_data():
    """Retorna dados de exemplo para testes de artigos."""
    return {
        'title': 'Marketing Digital para Pequenas Empresas',
        'category': 'blog-marketing-digital',
        'sections': {
            'attention': 'Texto de atenção...',
            'interest': 'Texto de interesse...',
            'desire': 'Texto de desejo...',
            'action': 'Texto de ação...',
            'faq': 'Perguntas frequentes...'
        }
    }

@pytest.fixture
def mock_dify_response():
    """Retorna uma resposta simulada da API Dify."""
    return {
        'answer': 'Resposta simulada da API...',
        'conversation_id': '123456789',
        'created_at': '2024-03-10T09:00:00Z'
    }

@pytest.fixture
def mock_wordpress_client(mocker):
    """Retorna um cliente WordPress simulado."""
    return mocker.Mock()