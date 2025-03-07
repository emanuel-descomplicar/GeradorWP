"""
Agente de Publicação para o GeradorWP
"""
from crewai import Agent
from src.config.config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

class PublisherAgent:
    def __init__(self):
        self.agent = Agent(
            role='Publicador de Conteúdo',
            goal='Publicar conteúdo no WordPress de forma eficiente e segura',
            backstory="""Você é um especialista em WordPress com experiência em 
            publicação de conteúdo, gestão de metadados e otimização de posts. 
            Você garante que todo o conteúdo seja publicado corretamente e 
            seguindo as melhores práticas.""",
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