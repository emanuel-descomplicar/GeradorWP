"""
Agente de Escrita para o GeradorWP
"""
from crewai import Agent
from src.config.config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE

class WriterAgent:
    def __init__(self):
        self.agent = Agent(
            role='Escritor de Conteúdo',
            goal='Criar conteúdo WordPress de alta qualidade, otimizado para SEO e envolvente',
            backstory="""Você é um escritor profissional especializado em criar conteúdo 
            para WordPress. Você tem experiência em SEO, storytelling e criação de 
            conteúdo que engaja os leitores.""",
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