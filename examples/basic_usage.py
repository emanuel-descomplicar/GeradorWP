"""
Exemplo básico de uso do GeradorWP.
"""

import os
from dotenv import load_dotenv
from gerador_wp.agents import ResearcherAgent, WriterAgent, PublisherAgent
from gerador_wp.utils.exceptions import ResearchError, WritingError, PublishingError

def main():
    """Função principal do exemplo."""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    try:
        # Inicializa os agentes
        researcher = ResearcherAgent()
        writer = WriterAgent()
        publisher = PublisherAgent()
        
        # Define o tópico e palavras-chave
        topic = "Marketing Digital em 2024"
        keywords = [
            "marketing digital",
            "tendências 2024",
            "estratégias de marketing",
            "mídias sociais",
            "marketing online"
        ]
        
        print(f"Iniciando geração de conteúdo para: {topic}")
        print(f"Palavras-chave: {', '.join(keywords)}")
        
        # Fase 1: Pesquisa
        print("\n1. Realizando pesquisa...")
        research_data = researcher.research(topic, keywords)
        print("✓ Pesquisa concluída")
        
        # Fase 2: Escrita
        print("\n2. Gerando conteúdo...")
        content = writer.write(research_data, keywords)
        print("✓ Conteúdo gerado")
        print(f"- Título: {content['titulo']}")
        print(f"- Palavras: {content['word_count']}")
        print(f"- Tempo de leitura: {content['reading_time']} minutos")
        
        # Fase 3: Publicação
        print("\n3. Publicando conteúdo...")
        result = publisher.publish(content, [])
        print("✓ Conteúdo publicado")
        print(f"- ID: {result['id']}")
        print(f"- Link: {result['link']}")
        print(f"- Status: {result['status']}")
        
        print("\nProcesso concluído com sucesso!")
        
    except ResearchError as e:
        print(f"\nErro na pesquisa: {e}")
    except WritingError as e:
        print(f"\nErro na escrita: {e}")
    except PublishingError as e:
        print(f"\nErro na publicação: {e}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")

if __name__ == "__main__":
    main() 