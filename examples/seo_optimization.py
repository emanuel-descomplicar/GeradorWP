"""
Exemplo de otimização SEO do GeradorWP.
"""

import os
from dotenv import load_dotenv
from gerador_wp.utils.seo import SEOOptimizer
from gerador_wp.utils.content import ContentManager
from gerador_wp.utils.logger import Logger
from gerador_wp.utils.exceptions import ValidationError

def print_section(title: str) -> None:
    """
    Imprime título de seção.
    
    Args:
        title: Título da seção
    """
    print(f"\n{title}")
    print("=" * len(title))

def main():
    """Função principal do exemplo."""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Inicializa utilitários
    seo = SEOOptimizer()
    content = ContentManager()
    logger = Logger(__name__)
    
    try:
        print("Iniciando otimização SEO...")
        
        # Dados de exemplo
        original_title = "Como Fazer Marketing Digital em 2024: Guia Completo"
        keywords = [
            "marketing digital",
            "estratégias de marketing",
            "marketing online",
            "tendências 2024"
        ]
        
        original_content = """
        O marketing digital é essencial para qualquer negócio em 2024.
        Neste guia completo, vamos explorar as principais estratégias
        e tendências que você precisa conhecer para ter sucesso online.
        
        Vamos abordar tópicos como:
        - Redes sociais
        - SEO
        - Marketing de conteúdo
        - E-mail marketing
        - Marketing de influência
        
        Continue lendo para descobrir como aplicar essas estratégias
        no seu negócio e alcançar resultados extraordinários.
        """
        
        # 1. Otimização do Título
        print_section("1. Otimização do Título")
        print("Original:", original_title)
        
        optimized_title = seo.optimize_title(
            original_title,
            keywords,
            max_length=60
        )
        
        print("Otimizado:", optimized_title)
        print(f"Comprimento: {len(optimized_title)} caracteres")
        
        # 2. Geração de Meta Description
        print_section("2. Meta Description")
        meta_description = seo.optimize_meta_description(
            original_content,
            keywords,
            max_length=160
        )
        
        print("Meta Description:", meta_description)
        print(f"Comprimento: {len(meta_description)} caracteres")
        
        # 3. Otimização de Conteúdo
        print_section("3. Otimização de Conteúdo")
        print("Conteúdo Original:")
        print(original_content)
        
        optimized_content = seo.optimize_content(
            original_content,
            keywords,
            min_keyword_density=0.01,
            max_keyword_density=0.03
        )
        
        print("\nConteúdo Otimizado:")
        print(optimized_content)
        
        # 4. Análise de Densidade de Palavras-chave
        print_section("4. Densidade de Palavras-chave")
        for keyword in keywords:
            density = seo._calculate_keyword_density(
                optimized_content,
                keyword
            )
            print(f"- {keyword}: {density*100:.1f}%")
        
        # 5. Geração de Slug
        print_section("5. Geração de Slug")
        slug = seo.generate_slug(optimized_title)
        print("Slug:", slug)
        
        # 6. Extração de Palavras-chave
        print_section("6. Extração de Palavras-chave")
        extracted_keywords = content.extract_keywords(
            optimized_content,
            max_keywords=5
        )
        print("Palavras-chave extraídas:", ", ".join(extracted_keywords))
        
        # 7. Geração de Excerpt
        print_section("7. Geração de Excerpt")
        excerpt = content.generate_excerpt(
            optimized_content,
            max_length=160
        )
        print("Excerpt:", excerpt)
        print(f"Comprimento: {len(excerpt)} caracteres")
        
        # 8. Links Internos
        print_section("8. Links Internos")
        related_posts = [
            {
                "title": "Tendências de Marketing Digital para 2024",
                "url": "/tendencias-marketing-digital-2024"
            },
            {
                "title": "Como Fazer SEO em 2024",
                "url": "/como-fazer-seo-2024"
            }
        ]
        
        content_with_links = content.add_internal_links(
            optimized_content,
            related_posts
        )
        
        print("Conteúdo com Links:")
        print(content_with_links)
        
        # 9. Call-to-Action
        print_section("9. Call-to-Action")
        final_content = content.add_cta(
            content_with_links,
            cta_type="newsletter",
            cta_text="Inscreva-se em nossa newsletter para receber mais dicas de marketing digital!"
        )
        
        print("Conteúdo Final com CTA:")
        print(final_content)
        
        print("\nOtimização SEO concluída com sucesso!")
        
    except ValidationError as e:
        print(f"\nErro de validação: {e}")
        logger.error(f"Erro de validação: {str(e)}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        logger.error(f"Erro inesperado: {str(e)}")

if __name__ == "__main__":
    main() 