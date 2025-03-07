"""
Tarefa de Escrita para o GeradorWP
"""
from crewai import Task

class WritingTask:
    def __init__(self, research_data):
        self.research_data = research_data
    
    def get_task(self, agent):
        return Task(
            description=f"""Crie um artigo WordPress de alta qualidade baseado nas informações 
            pesquisadas:
            
            {self.research_data}
            
            Objetivos específicos:
            1. Crie um título SEO-friendly
            2. Desenvolva uma introdução cativante
            3. Estruture o conteúdo de forma clara e lógica
            4. Inclua exemplos práticos e casos de uso
            5. Otimize para SEO com palavras-chave relevantes
            6. Adicione uma conclusão forte
            
            O resultado deve ser um artigo completo e pronto para publicação.""",
            agent=agent,
            context="Criação de artigo WordPress"
        ) 