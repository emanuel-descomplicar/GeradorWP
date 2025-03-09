"""
ResearchTask - Define objetivos e critérios de pesquisa

Este módulo define tarefas específicas de pesquisa para o ResearcherAgent,
incluindo objetivos, critérios de qualidade e validação de dados.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import logging
from typing import Dict, List, Any, Optional

class ResearchTask:
    """
    Define uma tarefa de pesquisa para o ResearcherAgent.
    
    Esta classe define os objetivos, critérios e parâmetros para
    execução de pesquisas pelo ResearcherAgent.
    """
    
    def __init__(self, topic: str, keywords: List[str], config: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma tarefa de pesquisa.
        
        Args:
            topic: O tópico principal da pesquisa
            keywords: Lista de palavras-chave relacionadas
            config: Configurações opcionais para a tarefa
        """
        self.logger = logging.getLogger(__name__)
        self.topic = topic
        self.keywords = keywords
        self.config = config or {}
        
        # Definir critérios padrão de pesquisa
        self.min_sources = self.config.get("min_sources", 5)
        self.max_sources = self.config.get("max_sources", 15)
        self.min_source_quality = self.config.get("min_source_quality", 0.7)  # de 0 a 1
        
        self.logger.info(f"ResearchTask inicializada para o tópico: {topic}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Obtém os parâmetros da tarefa de pesquisa.
        
        Returns:
            Um dicionário com os parâmetros da tarefa
        """
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "min_sources": self.min_sources,
            "max_sources": self.max_sources,
            "min_source_quality": self.min_source_quality,
            "additional_params": self.config.get("additional_params", {})
        }
    
    def validate_results(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida os resultados da pesquisa de acordo com os critérios definidos.
        
        Args:
            results: Os resultados da pesquisa a serem validados
            
        Returns:
            Um dicionário com os resultados validados e um indicador de qualidade
        """
        self.logger.info(f"Validando resultados da pesquisa para o tópico: {self.topic}")
        
        # Verificar número de fontes
        sources = results.get("sources", [])
        sources_count = len(sources)
        
        # Verificar qualidade das fontes
        quality_sources = [s for s in sources if s.get("relevance", 0) >= self.min_source_quality]
        quality_sources_count = len(quality_sources)
        
        # Calcular pontuação de qualidade
        quality_score = 0
        if sources_count > 0:
            quality_score = quality_sources_count / sources_count
        
        # Adicionar metadados de validação
        validated_results = results.copy()
        validated_results["validation"] = {
            "sources_count": sources_count,
            "quality_sources_count": quality_sources_count,
            "quality_score": quality_score,
            "meets_criteria": sources_count >= self.min_sources and quality_score >= 0.6,
            "improvement_suggestions": []
        }
        
        # Adicionar sugestões de melhoria se necessário
        if sources_count < self.min_sources:
            validated_results["validation"]["improvement_suggestions"].append(
                f"Aumentar o número de fontes (mínimo recomendado: {self.min_sources})"
            )
        
        if quality_score < 0.6:
            validated_results["validation"]["improvement_suggestions"].append(
                "Melhorar a qualidade das fontes (aumentar relevância)"
            )
        
        self.logger.info(f"Validação concluída com pontuação de qualidade: {quality_score:.2f}")
        return validated_results 