"""
ResearcherAgent - Responsável por pesquisar e coletar informações relevantes.
"""
from typing import Dict, List
from crewai import Agent
from ..config.settings import Settings

class ResearcherAgent:
    """Agente responsável por pesquisar e coletar informações para o artigo."""
    
    def __init__(self, settings: Settings):
        """Inicializa o ResearcherAgent com as configurações necessárias."""
        self.settings = settings
        self.agent = Agent(
            role='Pesquisador de Conteúdo',
            goal='Coletar informações relevantes e precisas sobre o tópico',
            backstory="""Você é um pesquisador especializado em marketing digital e tecnologia.
            Sua função é coletar informações precisas e relevantes para criar conteúdo de qualidade.""",
            verbose=True
        )
    
    def research(self, topic: str) -> Dict[str, List[str]]:
        """
        Realiza pesquisa sobre o tópico fornecido.
        
        Args:
            topic: Tópico a ser pesquisado
            
        Returns:
            Dict com as informações coletadas organizadas por categoria
        """
        # TODO: Implementar pesquisa real
        return {
            'main_points': [],
            'statistics': [],
            'examples': [],
            'sources': []
        }

    def get_agent(self):
        return self.agent 