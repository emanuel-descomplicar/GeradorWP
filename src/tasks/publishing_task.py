"""
PublishingTask - Define parâmetros de publicação

Este módulo define tarefas específicas de publicação para o PublisherAgent,
incluindo formatação final, otimização de mídia e verificação de publicação.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import logging
from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv

class PublishingTask:
    """
    Define uma tarefa de publicação para o PublisherAgent.
    
    Esta classe define os parâmetros, requisitos e validações para
    a publicação de conteúdo no WordPress pelo PublisherAgent.
    """
    
    def __init__(self, content: Dict[str, Any], category: str, status: str = "draft", config: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma tarefa de publicação.
        
        Args:
            content: O conteúdo a ser publicado
            category: A categoria do artigo
            status: O status da publicação (draft, publish, etc.)
            config: Configurações opcionais para a tarefa
        """
        self.logger = logging.getLogger(__name__)
        self.content = content
        self.category = category
        self.status = status
        self.config = config or {}
        
        # Carregar variáveis de ambiente
        load_dotenv()
        
        # Configurações do WordPress
        self.wp_url = os.getenv("WP_URL")
        
        # Definir requisitos padrão de publicação
        self.validate_before_publish = self.config.get("validate_before_publish", True)
        self.verify_after_publish = self.config.get("verify_after_publish", True)
        self.add_featured_image = self.config.get("add_featured_image", True)
        
        self.logger.info(f"PublishingTask inicializada para a categoria: {category}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Obtém os parâmetros da tarefa de publicação.
        
        Returns:
            Um dicionário com os parâmetros da tarefa
        """
        return {
            "title": self.content.get("title", ""),
            "category": self.category,
            "status": self.status,
            "validate_before_publish": self.validate_before_publish,
            "verify_after_publish": self.verify_after_publish,
            "add_featured_image": self.add_featured_image,
            "content_summary": {
                "word_count": self.content.get("word_count", 0),
                "seo_score": self.content.get("seo_score", 0),
                "validation_score": self.content.get("validation", {}).get("overall_quality", 0)
            },
            "additional_params": self.config.get("additional_params", {})
        }
    
    def prepare_post_data(self) -> Dict[str, Any]:
        """
        Prepara os dados do post para publicação no WordPress.
        
        Returns:
            Um dicionário com os dados formatados para publicação
        """
        # Extrair dados necessários
        title = self.content.get("title", "")
        content = self.content.get("full_content", "")
        excerpt = self.content.get("meta_description", "")
        
        # Preparar dados do post
        post_data = {
            "title": title,
            "content": content,
            "excerpt": excerpt,
            "status": self.status,
            "categories": [self.category],
            "tags": self.content.get("seo_meta", {}).get("tags", []),
            "meta": {
                "_yoast_wpseo_metadesc": excerpt,
                "_yoast_wpseo_focuskw": self.content.get("seo_meta", {}).get("focus_keyword", "")
            }
        }
        
        return post_data
    
    def validate_pre_publish(self) -> Dict[str, Any]:
        """
        Realiza validações pré-publicação.
        
        Returns:
            Um dicionário com os resultados da validação
        """
        self.logger.info(f"Realizando validações pré-publicação para: {self.content.get('title', '')}")
        
        # Verificações a realizar
        validations = {
            "has_title": bool(self.content.get("title", "")),
            "has_content": bool(self.content.get("full_content", "")),
            "has_excerpt": bool(self.content.get("meta_description", "")),
            "word_count_sufficient": self.content.get("word_count", 0) >= 500,
            "category_valid": bool(self.category),
            "seo_meta_complete": bool(self.content.get("seo_meta", {})),
            "previous_validation_passed": self.content.get("validation", {}).get("meets_criteria", False)
        }
        
        # Resumo geral
        all_passed = all(validations.values())
        failed_validations = [k for k, v in validations.items() if not v]
        
        validation_result = {
            "all_passed": all_passed,
            "validations": validations,
            "failed_validations": failed_validations,
            "can_proceed": all_passed or not self.validate_before_publish
        }
        
        if not all_passed:
            self.logger.warning(f"Validações pré-publicação falharam: {', '.join(failed_validations)}")
        else:
            self.logger.info("Todas as validações pré-publicação passaram")
        
        return validation_result
    
    def validate_post_publish(self, publication_result: Dict[str, Any]) -> Dict[str, Any]:
        """
        Realiza validações pós-publicação.
        
        Args:
            publication_result: O resultado da publicação
            
        Returns:
            Um dicionário com os resultados da validação
        """
        self.logger.info(f"Realizando validações pós-publicação para o post ID: {publication_result.get('post_id', 'N/A')}")
        
        # Verificações a realizar
        post_id = publication_result.get("post_id", 0)
        success = publication_result.get("success", False)
        permalink = publication_result.get("permalink", "")
        
        validations = {
            "publication_success": success,
            "has_post_id": post_id > 0,
            "has_permalink": bool(permalink),
            "permalink_accessible": True  # Simulado, deveria verificar acesso real
        }
        
        # Resumo geral
        all_passed = all(validations.values())
        failed_validations = [k for k, v in validations.items() if not v]
        
        validation_result = {
            "all_passed": all_passed,
            "validations": validations,
            "failed_validations": failed_validations,
            "publication_successful": success and post_id > 0
        }
        
        if not all_passed:
            self.logger.warning(f"Validações pós-publicação falharam: {', '.join(failed_validations)}")
        else:
            self.logger.info("Todas as validações pós-publicação passaram")
        
        return validation_result 