"""
Agente de Pesquisa para o GeradorWP
"""
from crewai import Agent
from src.config.config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

class ResearcherAgent:
    def __init__(self):
        self.agent = Agent(
            role='Pesquisador de Conteúdo',
            goal='Pesquisar e coletar informações relevantes e precisas sobre tópicos específicos',
            backstory="""Você é um pesquisador especializado em coletar e analisar informações 
            de alta qualidade. Você tem experiência em encontrar fontes confiáveis e 
            sintetizar informações de forma clara e objetiva.""",
            verbose=True,
            allow_delegation=False,
            llm_config={
                "api_key": OPENAI_API_KEY,
                "model": MODEL_NAME,
                "temperature": TEMPERATURE
            }
        )
    
    def get_agent(self):
        return self.agent 