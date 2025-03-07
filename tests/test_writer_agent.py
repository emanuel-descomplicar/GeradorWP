"""
Testes unitários para o WriterAgent.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime

from src.agents.writer_agent import WriterAgent
from src.utils.exceptions import WritingError

class TestWriterAgent(unittest.TestCase):
    """Testes para o WriterAgent."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.agent = WriterAgent()
        
        # Mock das dependências
        self.agent.cache = Mock()
        self.agent.dify = Mock()
        self.agent.content = Mock()
        self.agent.seo = Mock()
        self.agent.logger = Mock()
        
        # Dados de exemplo
        self.research_data = {
            "topic": "Marketing Digital",
            "keywords": ["seo", "marketing"],
            "web_results": {
                "principais_conceitos": ["conceito1", "conceito2"],
                "dados_estatisticos": ["dado1", "dado2"]
            },
            "statistics": {
                "dados_numericos": [1, 2, 3],
                "percentuais": ["10%", "20%"]
            }
        }
    
    def test_structure_content_cache_hit(self):
        """Testa estruturação de conteúdo com cache hit."""
        # Configura o mock
        expected_result = {
            "titulo": "Título Teste",
            "meta_description": "Descrição teste",
            "introducao": "Introdução teste"
        }
        self.agent.cache.get.return_value = expected_result
        
        # Executa o teste
        result = self.agent._structure_content(self.research_data)
        
        # Verifica o resultado
        self.assertEqual(result, expected_result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_not_called()
    
    def test_structure_content_cache_miss(self):
        """Testa estruturação de conteúdo com cache miss."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "titulo": "Título Teste",
                    "meta_description": "Descrição teste",
                    "introducao": "Introdução teste"
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._structure_content(self.research_data)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("titulo", result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_called_once()
        self.agent.cache.set.assert_called_once()
    
    def test_optimize_seo_success(self):
        """Testa otimização SEO com sucesso."""
        # Configura o mock
        content = {
            "titulo": "Título Original",
            "meta_description": "Descrição original",
            "introducao": "Introdução original"
        }
        self.agent.cache.get.return_value = None
        self.agent.content.extract_keywords.return_value = ["palavra1", "palavra2"]
        self.agent.seo.optimize_title.return_value = "Título Otimizado"
        self.agent.seo.optimize_meta_description.return_value = "Descrição otimizada"
        self.agent.seo.optimize_content.return_value = "Conteúdo otimizado"
        self.agent.seo.generate_slug.return_value = "titulo-otimizado"
        
        # Executa o teste
        result = self.agent._optimize_seo(content)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertEqual(result["titulo"], "Título Otimizado")
        self.assertEqual(result["slug"], "titulo-otimizado")
        self.agent.seo.optimize_title.assert_called_once()
        self.agent.seo.optimize_meta_description.assert_called_once()
        self.agent.seo.optimize_content.assert_called()
    
    def test_review_content_success(self):
        """Testa revisão de conteúdo com sucesso."""
        # Configura o mock
        content = {
            "titulo": "Título Teste",
            "meta_description": "Descrição teste",
            "introducao": "Introdução teste"
        }
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "titulo": "Título Revisado",
                    "meta_description": "Descrição revisada",
                    "introducao": "Introdução revisada"
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._review_content(content)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertEqual(result["titulo"], "Título Revisado")
        self.agent.dify.completion.assert_called_once()
        self.agent.cache.set.assert_called_once()
    
    def test_write_success(self):
        """Testa criação completa de conteúdo com sucesso."""
        # Configura o mock
        self.agent._structure_content = Mock(return_value={
            "titulo": "Título Teste",
            "meta_description": "Descrição teste"
        })
        self.agent._optimize_seo = Mock(return_value={
            "titulo": "Título Otimizado",
            "meta_description": "Descrição otimizada"
        })
        self.agent._review_content = Mock(return_value={
            "titulo": "Título Final",
            "meta_description": "Descrição final",
            "content": "Conteúdo completo do artigo"
        })
        self.agent.content.add_internal_links = Mock(return_value={})
        self.agent.content.add_cta = Mock(return_value={})
        self.agent.content.format_content = Mock(return_value={})
        self.agent.content.generate_excerpt = Mock(return_value="Excerpt teste")
        
        # Executa o teste
        result = self.agent.write(self.research_data, ["palavra1", "palavra2"])
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("keywords", result)
        self.assertIn("timestamp", result)
        self.assertIn("word_count", result)
        self.assertIn("reading_time", result)
        self.agent._structure_content.assert_called_once()
        self.agent._optimize_seo.assert_called_once()
        self.agent._review_content.assert_called_once()
    
    def test_write_error(self):
        """Testa erro na criação de conteúdo."""
        # Configura o mock para lançar erro
        self.agent._structure_content = Mock(side_effect=Exception("Erro de teste"))
        
        # Executa o teste
        with self.assertRaises(WritingError):
            self.agent.write(self.research_data, ["palavra1"])
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()
    
    def test_invalid_research_data(self):
        """Testa estruturação com dados de pesquisa inválidos."""
        # Executa o teste
        with self.assertRaises(WritingError):
            self.agent._structure_content({})
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()
    
    def test_invalid_json_response(self):
        """Testa resposta JSON inválida."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": "resposta inválida"
            }]
        }
        
        # Executa o teste
        with self.assertRaises(WritingError):
            self.agent._structure_content(self.research_data)
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()

if __name__ == '__main__':
    unittest.main() 