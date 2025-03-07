"""
Tarefa de Publicação para o GeradorWP
"""
from crewai import Task
from src.config.config import WP_URL

class PublishingTask:
    def __init__(self, content):
        self.content = content
    
    def get_task(self, agent):
        return Task(
            description=f"""Publique o seguinte conteúdo no WordPress:
            
            {self.content}
            
            Objetivos específicos:
            1. Configure os metadados apropriados (categorias, tags)
            2. Otimize o SEO (meta description, keywords)
            3. Configure o status de publicação
            4. Verifique a formatação e links
            5. Garanta que todas as imagens estejam otimizadas
            
            O resultado deve ser um post publicado com sucesso no WordPress.""",
            agent=agent,
            context=f"Publicação no WordPress: {WP_URL}"
        ) 