"""
Exemplo de fluxo personalizado do GeradorWP.
"""

import os
from dotenv import load_dotenv
from gerador_wp.agents import ResearcherAgent, WriterAgent, PublisherAgent
from gerador_wp.utils.content import ContentManager
from gerador_wp.utils.seo import SEOOptimizer
from gerador_wp.utils.image import ImageManager
from gerador_wp.utils.exceptions import ResearchError, WritingError, PublishingError

def main():
    """Função principal do exemplo."""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    try:
        # Inicializa os agentes e utilitários
        researcher = ResearcherAgent()
        writer = WriterAgent()
        publisher = PublisherAgent()
        content_manager = ContentManager()
        seo = SEOOptimizer()
        image = ImageManager()
        
        # Define o tópico e palavras-chave
        topic = "Inteligência Artificial na Educação"
        keywords = [
            "inteligência artificial",
            "educação",
            "tecnologia educacional",
            "ensino personalizado",
            "aprendizagem adaptativa"
        ]
        
        print(f"Iniciando fluxo personalizado para: {topic}")
        
        # Fase 1: Pesquisa Avançada
        print("\n1. Realizando pesquisa avançada...")
        research_data = researcher.research(topic, keywords)
        
        # Extrai palavras-chave adicionais
        additional_keywords = content_manager.extract_keywords(
            research_data["web_results"].get("principais_conceitos", "")
        )
        keywords.extend(additional_keywords)
        print(f"✓ Palavras-chave expandidas: {', '.join(keywords)}")
        
        # Fase 2: Geração de Conteúdo
        print("\n2. Gerando conteúdo otimizado...")
        content = writer.write(research_data, keywords)
        
        # Otimização adicional de SEO
        content["titulo"] = seo.optimize_title(content["titulo"], keywords)
        content["meta_description"] = seo.optimize_meta_description(
            content["meta_description"],
            keywords
        )
        print("✓ SEO otimizado")
        
        # Gera imagem destacada
        print("\n3. Gerando imagem destacada...")
        image_prompt = f"Uma imagem moderna e profissional sobre {topic}"
        image_bytes = image.generate_image(image_prompt)
        
        if image_bytes:
            # Otimiza a imagem
            image_bytes = image.optimize_image(image_bytes)
            
            # Cria miniatura
            thumbnail_bytes = image.create_thumbnail(image_bytes)
            
            print("✓ Imagem gerada e otimizada")
            
            # Lista de arquivos de mídia
            media_files = ["imagem_destacada.jpg"]
        else:
            media_files = []
            print("⚠ Não foi possível gerar a imagem")
        
        # Adiciona links internos e CTA
        print("\n4. Enriquecendo o conteúdo...")
        content = content_manager.add_internal_links(
            content,
            research_data.get("related_content", [])
        )
        
        content = content_manager.add_cta(
            content,
            cta_type="newsletter",
            cta_text="Inscreva-se em nossa newsletter para receber mais conteúdo sobre IA na Educação!"
        )
        print("✓ Links e CTA adicionados")
        
        # Fase 3: Publicação Personalizada
        print("\n5. Publicando conteúdo...")
        result = publisher.publish(content, media_files)
        
        # Exibe resultados
        print("\nPublicação concluída:")
        print(f"- Título: {result['title']}")
        print(f"- Link: {result['link']}")
        print(f"- Status: {result['status']}")
        print(f"- Palavras: {content['word_count']}")
        print(f"- Tempo de leitura: {content['reading_time']} minutos")
        print(f"- Palavras-chave: {', '.join(keywords)}")
        
        if media_files:
            print(f"- Imagens: {len(media_files)}")
        
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