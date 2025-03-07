"""
WriterAgent - Responsável por criar o conteúdo do artigo.
"""
from typing import Dict, List
from crewai import Agent
from ..config.settings import Settings

class WriterAgent:
    """Agente responsável por criar o conteúdo do artigo."""
    
    def __init__(self, settings: Settings):
        """Inicializa o WriterAgent com as configurações necessárias."""
        self.settings = settings
        self.agent = Agent(
            role='Escritor de Conteúdo',
            goal='Criar conteúdo relevante e otimizado para SEO',
            backstory="""Você é um escritor especializado em marketing digital e tecnologia.
            Sua função é criar conteúdo de qualidade, otimizado para SEO e relevante para o público-alvo.""",
            verbose=True
        )
    
    def write(self, research_data: Dict[str, List[str]], topic: str) -> str:
        """
        Cria o conteúdo do artigo baseado nas informações pesquisadas.
        
        Args:
            research_data: Dados coletados pelo ResearcherAgent
            topic: Tópico do artigo
            
        Returns:
            Conteúdo do artigo em formato HTML
        """
        # TODO: Implementar geração de conteúdo
        return "" 