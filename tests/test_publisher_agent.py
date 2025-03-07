"""
Testes unitários para o PublisherAgent.
"""

import unittest
from unittest.mock import Mock, patch
import json
from datetime import datetime

from src.agents.publisher_agent import PublisherAgent
from src.utils.exceptions import PublishingError

class TestPublisherAgent(unittest.TestCase):
    """Testes para o PublisherAgent."""
    
    def setUp(self):
        """Configura o ambiente de teste."""
        self.agent = PublisherAgent()
        
        # Mock das dependências
        self.agent.cache = Mock()
        self.agent.http = Mock()
        self.agent.dify = Mock()
        self.agent.wp = Mock()
        self.agent.image = Mock()
        self.agent.logger = Mock()
        
        # Dados de exemplo
        self.content = {
            "titulo": "Título do Artigo",
            "meta_description": "Descrição do artigo",
            "content": "Conteúdo completo do artigo",
            "excerpt": "Resumo do artigo",
            "keywords": ["palavra1", "palavra2"]
        }
        
        self.media_files = [
            "https://exemplo.com/imagem1.jpg",
            "https://exemplo.com/imagem2.jpg"
        ]
    
    def test_format_content_cache_hit(self):
        """Testa formatação de conteúdo com cache hit."""
        # Configura o mock
        expected_result = {
            "post_title": "Título do Artigo",
            "post_content": "<p>Conteúdo do artigo</p>",
            "post_excerpt": "Resumo do artigo"
        }
        self.agent.cache.get.return_value = expected_result
        
        # Executa o teste
        result = self.agent._format_content(self.content)
        
        # Verifica o resultado
        self.assertEqual(result, expected_result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_not_called()
    
    def test_format_content_cache_miss(self):
        """Testa formatação de conteúdo com cache miss."""
        # Configura o mock
        self.agent.cache.get.return_value = None
        self.agent.dify.completion.return_value = {
            "choices": [{
                "text": json.dumps({
                    "post_title": "Título do Artigo",
                    "post_content": "<p>Conteúdo do artigo</p>",
                    "post_excerpt": "Resumo do artigo"
                })
            }]
        }
        
        # Executa o teste
        result = self.agent._format_content(self.content)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("post_title", result)
        self.agent.cache.get.assert_called_once()
        self.agent.dify.completion.assert_called_once()
        self.agent.cache.set.assert_called_once()
    
    def test_upload_media_success(self):
        """Testa upload de mídia com sucesso."""
        # Configura o mock
        media_data = {
            "media_0": self.media_files[0],
            "media_1": self.media_files[1]
        }
        self.agent.cache.get.return_value = None
        self.agent.image.download_image.return_value = b"image_bytes"
        self.agent.image.optimize_image.return_value = b"optimized_bytes"
        self.agent.wp._upload_image.return_value = 123
        
        # Executa o teste
        result = self.agent._upload_media(media_data)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertEqual(len(result), 2)
        self.agent.image.download_image.assert_called()
        self.agent.image.optimize_image.assert_called()
        self.agent.wp._upload_image.assert_called()
    
    def test_publish_post_success(self):
        """Testa publicação de post com sucesso."""
        # Configura o mock
        post_data = {
            "post_title": "Título do Artigo",
            "post_content": "<p>Conteúdo do artigo</p>",
            "post_excerpt": "Resumo do artigo",
            "post_status": "draft"
        }
        self.agent.cache.get.return_value = None
        self.agent.wp.create_post.return_value = {
            "id": 123,
            "title": "Título do Artigo",
            "link": "https://exemplo.com/artigo"
        }
        
        # Executa o teste
        result = self.agent._publish_post(post_data)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("title", result)
        self.agent.wp.create_post.assert_called_once()
    
    def test_publish_success(self):
        """Testa publicação completa com sucesso."""
        # Configura o mock
        self.agent._format_content = Mock(return_value={
            "post_title": "Título do Artigo",
            "post_content": "<p>Conteúdo do artigo</p>"
        })
        self.agent._upload_media = Mock(return_value={
            "media_0": {
                "url": self.media_files[0],
                "attachment_id": 123
            }
        })
        self.agent._publish_post = Mock(return_value={
            "id": 456,
            "title": "Título do Artigo",
            "link": "https://exemplo.com/artigo"
        })
        
        # Executa o teste
        result = self.agent.publish(self.content, self.media_files)
        
        # Verifica o resultado
        self.assertIsInstance(result, dict)
        self.assertIn("id", result)
        self.assertIn("timestamp", result)
        self.assertIn("media_files", result)
        self.assertEqual(result["status"], "success")
        self.agent._format_content.assert_called_once()
        self.agent._upload_media.assert_called_once()
        self.agent._publish_post.assert_called_once()
    
    def test_publish_error(self):
        """Testa erro na publicação."""
        # Configura o mock para lançar erro
        self.agent._format_content = Mock(side_effect=Exception("Erro de teste"))
        
        # Executa o teste
        with self.assertRaises(PublishingError):
            self.agent.publish(self.content, self.media_files)
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()
    
    def test_invalid_content(self):
        """Testa formatação com conteúdo inválido."""
        # Executa o teste
        with self.assertRaises(PublishingError):
            self.agent._format_content({})
        
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
        with self.assertRaises(PublishingError):
            self.agent._format_content(self.content)
        
        # Verifica o log de erro
        self.agent.logger.log_error.assert_called_once()

if __name__ == '__main__':
    unittest.main() 