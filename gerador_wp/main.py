"""
Módulo principal do GeradorWP.
"""

import argparse
import sys
from typing import List, Optional
from crewai import Crew, Task

from .agents.researcher_agent import ResearcherAgent
from .agents.writer_agent import WriterAgent
from .agents.publisher_agent import PublisherAgent
from .config.config import validate_config

def main(args: Optional[List[str]] = None) -> int:
    """
    Função principal do GeradorWP.
    
    Args:
        args: Argumentos da linha de comando
        
    Returns:
        Código de saída (0 para sucesso, 1 para erro)
    """
    # Configura o parser de argumentos
    parser = argparse.ArgumentParser(
        description="Gerador de conteúdo para WordPress usando CrewAI"
    )
    parser.add_argument(
        "topic",
        help="Tópico principal do artigo"
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        help="Palavras-chave para otimização SEO"
    )
    parser.add_argument(
        "--draft",
        action="store_true",
        help="Publicar como rascunho"
    )
    parser.add_argument(
        "--category",
        help="Categoria do artigo no WordPress"
    )
    parser.add_argument(
        "--tags",
        nargs="+",
        help="Tags para o artigo"
    )
    
    # Processa os argumentos
    args = parser.parse_args(args)
    
    try:
        # Valida as configurações
        validate_config()
        
        # Inicializa os agentes
        researcher = ResearcherAgent()
        writer = WriterAgent()
        publisher = PublisherAgent()
        
        # Define as tarefas
        research_task = Task(
            description=f"Pesquisar informações sobre {args.topic}",
            agent=researcher.agent
        )
        
        writing_task = Task(
            description="Criar o conteúdo do artigo",
            agent=writer.agent
        )
        
        publishing_task = Task(
            description="Publicar o artigo no WordPress",
            agent=publisher.agent
        )
        
        # Cria e executa a crew
        crew = Crew(
            agents=[researcher.agent, writer.agent, publisher.agent],
            tasks=[research_task, writing_task, publishing_task],
            verbose=True
        )
        
        # Executa as tarefas
        result = crew.kickoff()
        
        # Processa o resultado
        if result:
            print("Artigo gerado e publicado com sucesso!")
            return 0
        else:
            print("Erro ao gerar e publicar o artigo.")
            return 1
            
    except Exception as e:
        print(f"Erro: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 