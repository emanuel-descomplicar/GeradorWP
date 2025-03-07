"""
Testes unitários para o ResearcherAgent.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime

from src.agents.researcher_agent import ResearcherAgent
from src.utils.exceptions import ResearchError

class TestResearcherAgent(unittest.TestCase):
    """Testes para o ResearcherAgent."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.agent = ResearcherAgent()
        
        # Mock das dependências
        self.agent.cache = Mock()
        self.agent.http = Mock()
        self.agent.dify = Mock()
        self.agent.logger = Mock()
    
    def test_web_search_cache_hit(self):
        """Testa pesquisa web com cache hit."""
        # Configura o mock
        expected_result = {
            "principais_conceitos": ["conceito1", "conceito2"],
            "dados_estatisticos": ["dado1", "dado2"],
            "tendencias": ["tendencia1", "tendencia2"]
        }
        self.agent.cache.get.return_value = expected_result
        
        # Executa o teste
        result = self.agent._web_search("teste")
        
        # Verifica o resultado
        self.assertEqual(result, expected_result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_not_called()
    
    def test_web_search_cache_miss(self):
        """Testa pesquisa web com cache miss."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "principais_conceitos": ["conceito1", "conceito2"],
                    "dados_estatisticos": ["dado1", "dado2"],
                    "tendencias": ["tendencia1", "tendencia2"]
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._web_search("teste")
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("principais_conceitos", result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_called_once()
        self.agent.cache.set.assert_called_once()
    
    def test_analyze_content_success(self):
        """Testa análise de conteúdo com sucesso."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.http.get.return_value.text = "<html><body>Conteúdo de teste</body></html>"
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "topicos_principais": ["topico1", "topico2"],
                    "palavras_chave": ["palavra1", "palavra2"],
                    "tom_voz": "informativo"
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._analyze_content("http://teste.com")
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("topicos_principais", result)
        self.agent.http.get.assert_called_once()
        self.agent.dify.completion.assert_called_once()
    
    def test_collect_stats_success(self):
        """Testa coleta de estatísticas com sucesso."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "dados_numericos": [1, 2, 3],
                    "percentuais": ["10%", "20%"],
                    "tendencias": ["tendencia1", "tendencia2"]
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._collect_stats("teste")
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("dados_numericos", result)
        self.agent.dify.completion.assert_called_once()
    
    def test_research_success(self):
        """Testa pesquisa completa com sucesso."""
        # Configura o mock
        self.agent._web_search = Mock(return_value={"resultados": "teste"})
        self.agent._collect_stats = Mock(return_value={"estatisticas": "teste"})
        self.agent._analyze_content = Mock(return_value={"analise": "teste"})
        
        # Executa o teste
        result = self.agent.research("teste", ["palavra1", "palavra2"])
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertEqual(result["topic"], "teste")
        self.assertEqual(result["keywords"], ["palavra1", "palavra2"])
        self.assertIn("web_results", result)
        self.assertIn("statistics", result)
        self.assertIn("related_content", result)
        self.assertIn("timestamp", result)
    
    def test_research_error(self):
        """Testa erro na pesquisa."""
        # Configura o mock para lançar erro
        self.agent._web_search = Mock(side_effect=Exception("Erro de teste"))
        
        # Executa o teste
        with self.assertRaises(ResearchError):
            self.agent.research("teste", ["palavra1"])
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()
    
    def test_invalid_url(self):
        """Testa análise com URL inválida."""
        # Configura o mock para lançar erro
        self.agent.http.get.side_effect = Exception("URL inválida")
        
        # Executa o teste
        with self.assertRaises(ResearchError):
            self.agent._analyze_content("url_invalida")
        
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
        with self.assertRaises(ResearchError):
            self.agent._web_search("teste")
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()

if __name__ == '__main__':
    unittest.main() 