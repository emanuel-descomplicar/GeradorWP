"""
GeradorWP - Sistema de Geração de Conteúdo WordPress usando Crew AI
"""
from crewai import Crew, Process
from src.agents.researcher import ResearcherAgent
from src.agents.writer import WriterAgent
from src.agents.publisher import PublisherAgent
from src.tasks.research_task import ResearchTask
from src.tasks.writing_task import WritingTask
from src.tasks.publishing_task import PublishingTask
from src.config.config import validate_config

def generate_content(topic):
    """
    Gera e publica conteúdo WordPress sobre um tópico específico
    """
    # Valida as configurações
    validate_config()
    
    # Inicializa os agentes
    researcher = ResearcherAgent().get_agent()
    writer = WriterAgent().get_agent()
    publisher = PublisherAgent().get_agent()
    
    # Cria as tarefas
    research_task = ResearchTask(topic).get_task(researcher)
    writing_task = WritingTask("").get_task(writer)  # Será atualizado com os resultados da pesquisa
    publishing_task = PublishingTask("").get_task(publisher)  # Será atualizado com o conteúdo final
    
    # Cria e executa o crew
    crew = Crew(
        agents=[researcher, writer, publisher],
        tasks=[research_task, writing_task, publishing_task],
        process=Process.sequential,
        verbose=True
    )
    
    # Executa o processo
    result = crew.kickoff()
    
    return result

if __name__ == "__main__":
    # Exemplo de uso
    topic = "Inteligência Artificial no Marketing Digital"
    result = generate_content(topic)
    print(f"Resultado: {result}") 