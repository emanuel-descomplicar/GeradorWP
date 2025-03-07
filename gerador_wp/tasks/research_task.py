"""
Tarefa de Pesquisa para o GeradorWP
"""
from crewai import Task

class ResearchTask:
    def __init__(self, topic):
        self.topic = topic
    
    def get_task(self, agent):
        return Task(
            description=f"""Pesquise informações detalhadas sobre o tópico: {self.topic}
            
            Objetivos específicos:
            1. Encontre fontes confiáveis e atualizadas
            2. Colete dados relevantes e estatísticas
            3. Identifique tendências e insights importantes
            4. Prepare um resumo estruturado das informações
            
            O resultado deve ser um relatório detalhado que servirá como base para 
            a criação do conteúdo.""",
            agent=agent,
            context=f"Pesquisa sobre: {self.topic}"
        ) 