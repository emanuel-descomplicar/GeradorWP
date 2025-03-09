"""
WritingTask - Define requisitos e padrões de escrita

Este módulo define tarefas específicas de escrita para o WriterAgent,
incluindo estrutura de conteúdo, padrões de escrita e revisão de qualidade.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import logging
from typing import Dict, List, Any, Optional

class WritingTask:
    """
    Define uma tarefa de escrita para o WriterAgent.
    
    Esta classe define a estrutura, requisitos e padrões para
    a criação de conteúdo pelo WriterAgent.
    """
    
    def __init__(self, topic: str, keywords: List[str], research_data: Dict[str, Any], config: Optional[Dict[str, Any]] = None):
        """
        Inicializa uma tarefa de escrita.
        
        Args:
            topic: O tópico principal do artigo
            keywords: Lista de palavras-chave para SEO
            research_data: Dados coletados pela pesquisa
            config: Configurações opcionais para a tarefa
        """
        self.logger = logging.getLogger(__name__)
        self.topic = topic
        self.keywords = keywords
        self.research_data = research_data
        self.config = config or {}
        
        # Definir requisitos padrão de escrita
        self.min_word_count = self.config.get("min_word_count", 2000)
        self.max_word_count = self.config.get("max_word_count", 3000)
        self.seo_min_score = self.config.get("seo_min_score", 80)
        self.use_acida_model = self.config.get("use_acida_model", True)
        
        self.logger.info(f"WritingTask inicializada para o tópico: {topic}")
    
    def get_parameters(self) -> Dict[str, Any]:
        """
        Obtém os parâmetros da tarefa de escrita.
        
        Returns:
            Um dicionário com os parâmetros da tarefa
        """
        return {
            "topic": self.topic,
            "keywords": self.keywords,
            "min_word_count": self.min_word_count,
            "max_word_count": self.max_word_count,
            "seo_min_score": self.seo_min_score,
            "use_acida_model": self.use_acida_model,
            "research_data_summary": {
                "sources_count": len(self.research_data.get("sources", [])),
                "key_trends": self.research_data.get("trends", [])[:3],
                "validation_score": self.research_data.get("validation", {}).get("quality_score", 0)
            },
            "additional_params": self.config.get("additional_params", {})
        }
    
    def get_acida_structure(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtém a estrutura ACIDA para o artigo.
        
        Returns:
            Um dicionário com a estrutura ACIDA detalhada
        """
        return {
            "attention": {
                "word_count": 250,
                "elements": ["estatísticas impactantes", "contexto português", "perguntas retóricas"],
                "goal": "Captar atenção do leitor apresentando o problema/tema"
            },
            "confidence": {
                "word_count": 450,
                "elements": ["dados e fontes respeitáveis", "citações de especialistas", "referências a instituições portuguesas"],
                "goal": "Estabelecer credibilidade e autoridade sobre o tema"
            },
            "interest": {
                "word_count": 550,
                "elements": ["benefícios tangíveis", "exemplos práticos", "casos de estudo"],
                "goal": "Despertar interesse mostrando benefícios e resultados concretos"
            },
            "decision": {
                "word_count": 450,
                "elements": ["passos concretos", "recursos necessários", "considerações específicas"],
                "goal": "Ajudar na tomada de decisão com passos claros"
            },
            "action": {
                "word_count": 175,
                "elements": ["conclusão persuasiva", "call-to-action claro", "próximos passos"],
                "goal": "Motivar à ação com resumo conclusivo e direcionamento"
            }
        }
    
    def validate_content(self, content: Dict[str, Any]) -> Dict[str, Any]:
        """
        Valida o conteúdo criado de acordo com os requisitos definidos.
        
        Args:
            content: O conteúdo a ser validado
            
        Returns:
            Um dicionário com o conteúdo validado e indicadores de qualidade
        """
        self.logger.info(f"Validando conteúdo criado para o tópico: {self.topic}")
        
        # Verificar contagem de palavras
        word_count = content.get("word_count", 0)
        
        # Verificar pontuação SEO
        seo_score = content.get("seo_score", 0)
        
        # Verificar estrutura ACIDA se habilitada
        acida_complete = True
        acida_score = 1.0
        
        if self.use_acida_model:
            structure = content.get("content_structure", {})
            required_sections = ["attention", "confidence", "interest", "decision", "action"]
            
            # Verificar se todas as seções estão presentes
            missing_sections = [s for s in required_sections if s not in structure]
            acida_complete = len(missing_sections) == 0
            
            # Calcular pontuação ACIDA (simplificada)
            if not acida_complete:
                acida_score = (len(required_sections) - len(missing_sections)) / len(required_sections)
        
        # Adicionar metadados de validação
        validated_content = content.copy()
        validated_content["validation"] = {
            "word_count_ok": self.min_word_count <= word_count <= self.max_word_count,
            "seo_score_ok": seo_score >= self.seo_min_score,
            "acida_complete": acida_complete,
            "acida_score": acida_score,
            "overall_quality": (word_count / self.min_word_count * 0.3) + (seo_score / 100 * 0.4) + (acida_score * 0.3),
            "meets_criteria": (
                self.min_word_count <= word_count <= self.max_word_count and
                seo_score >= self.seo_min_score and
                acida_complete
            ),
            "improvement_suggestions": []
        }
        
        # Adicionar sugestões de melhoria se necessário
        if word_count < self.min_word_count:
            validated_content["validation"]["improvement_suggestions"].append(
                f"Aumentar o número de palavras (mínimo: {self.min_word_count})"
            )
        elif word_count > self.max_word_count:
            validated_content["validation"]["improvement_suggestions"].append(
                f"Reduzir o número de palavras (máximo: {self.max_word_count})"
            )
        
        if seo_score < self.seo_min_score:
            validated_content["validation"]["improvement_suggestions"].append(
                f"Melhorar a otimização SEO (mínimo: {self.seo_min_score})"
            )
        
        if not acida_complete:
            validated_content["validation"]["improvement_suggestions"].append(
                f"Completar a estrutura ACIDA (seções em falta: {', '.join(missing_sections)})"
            )
        
        self.logger.info(f"Validação de conteúdo concluída com qualidade geral: {validated_content['validation']['overall_quality']:.2f}")
        return validated_content 