"""
Testes de integração para o GeradorWP.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime
import os

from src.agents.researcher_agent import ResearcherAgent
from src.agents.writer_agent import WriterAgent
from src.agents.publisher_agent import PublisherAgent
from src.utils.exceptions import ResearchError, WritingError, PublishingError

class TestIntegration(unittest.TestCase):
    """Testes de integração para o GeradorWP."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        # Carrega variáveis de ambiente de teste
        os.environ["DIFY_API_KEY"] = "test_key"
        os.environ["DIFY_API_URL"] = "https://api.test.dify.ai/v1"
        os.environ["WP_URL"] = "https://test.wordpress.com"
        os.environ["WP_USERNAME"] = "test_user"
        os.environ["WP_PASSWORD"] = "test_pass"
        os.environ["WP_APP_PASSWORD"] = "test_app_pass"
        
        # Inicializa os agentes
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.publisher = PublisherAgent()
        
        # Dados de exemplo
        self.topic = "Marketing Digital"
        self.keywords = ["seo", "marketing", "digital"]
    
    def test_full_workflow_success(self):
        """Testa o fluxo completo com sucesso."""
        try:
            # Fase 1: Pesquisa
            research_data = self.researcher.research(
                self.topic,
                self.keywords
            )
            
            self.assertIsInstance(research_data, dict)
            self.assertIn("topic", research_data)
            self.assertIn("web_results", research_data)
            self.assertIn("statistics", research_data)
            
            # Fase 2: Escrita
            content = self.writer.write(
                research_data,
                self.keywords
            )
            
            self.assertIsInstance(content, dict)
            self.assertIn("titulo", content)
            self.assertIn("content", content)
            self.assertIn("meta_description", content)
            
            # Fase 3: Publicação
            result = self.publisher.publish(
                content,
                []  # Sem arquivos de mídia para teste
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn("id", result)
            self.assertIn("link", result)
            self.assertEqual(result["status"], "success")
            
        except (ResearchError, WritingError, PublishingError) as e:
            self.fail(f"Erro no fluxo: {str(e)}")
    
    def test_research_to_write_integration(self):
        """Testa integração entre ResearcherAgent e WriterAgent."""
        try:
            # Fase 1: Pesquisa
            research_data = self.researcher.research(
                self.topic,
                self.keywords
            )
            
            self.assertIsInstance(research_data, dict)
            
            # Fase 2: Escrita
            content = self.writer.write(
                research_data,
                self.keywords
            )
            
            self.assertIsInstance(content, dict)
            self.assertGreater(len(content.get("content", "")), 0)
            self.assertIn("keywords", content)
            self.assertEqual(content["keywords"], self.keywords)
            
        except (ResearchError, WritingError) as e:
            self.fail(f"Erro na integração: {str(e)}")
    
    def test_write_to_publish_integration(self):
        """Testa integração entre WriterAgent e PublisherAgent."""
        try:
            # Prepara conteúdo de teste
            content = {
                "titulo": "Título de Teste",
                "content": "<p>Conteúdo de teste</p>",
                "meta_description": "Descrição de teste",
                "excerpt": "Resumo de teste",
                "keywords": self.keywords
            }
            
            # Fase 1: Publicação
            result = self.publisher.publish(
                content,
                []  # Sem arquivos de mídia para teste
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn("id", result)
            self.assertEqual(result["status"], "success")
            
        except PublishingError as e:
            self.fail(f"Erro na integração: {str(e)}")
    
    def test_error_handling_integration(self):
        """Testa tratamento de erros entre os agentes."""
        # Testa erro na pesquisa
        with self.assertRaises(ResearchError):
            self.researcher.research("", [])
        
        # Testa erro na escrita
        with self.assertRaises(WritingError):
            self.writer.write({}, [])
        
        # Testa erro na publicação
        with self.assertRaises(PublishingError):
            self.publisher.publish({}, [])
    
    def test_cache_integration(self):
        """Testa integração do cache entre os agentes."""
        try:
            # Primeira execução
            research_data = self.researcher.research(
                self.topic,
                self.keywords
            )
            
            content = self.writer.write(
                research_data,
                self.keywords
            )
            
            result1 = self.publisher.publish(
                content,
                []
            )
            
            # Segunda execução (deve usar cache)
            research_data = self.researcher.research(
                self.topic,
                self.keywords
            )
            
            content = self.writer.write(
                research_data,
                self.keywords
            )
            
            result2 = self.publisher.publish(
                content,
                []
            )
            
            # Verifica se os resultados são iguais
            self.assertEqual(
                result1.get("content"),
                result2.get("content")
            )
            
        except Exception as e:
            self.fail(f"Erro no teste de cache: {str(e)}")
    
    def test_media_handling_integration(self):
        """Testa integração do gerenciamento de mídia."""
        try:
            # Prepara conteúdo de teste
            content = {
                "titulo": "Título de Teste",
                "content": "<p>Conteúdo de teste</p>",
                "meta_description": "Descrição de teste",
                "excerpt": "Resumo de teste",
                "keywords": self.keywords
            }
            
            # Lista de arquivos de mídia
            media_files = [
                "https://exemplo.com/imagem1.jpg",
                "https://exemplo.com/imagem2.jpg"
            ]
            
            # Publica com mídia
            result = self.publisher.publish(
                content,
                media_files
            )
            
            self.assertIsInstance(result, dict)
            self.assertIn("media_files", result)
            self.assertEqual(len(result["media_files"]), 2)
            
        except PublishingError as e:
            self.fail(f"Erro no teste de mídia: {str(e)}")

if __name__ == '__main__':
    unittest.main() 