#!/usr/bin/env python3
"""
Script de teste para publicação no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

from src.utils.wordpress import WordPressClient
from src.utils.image import ImageGenerator
from src.utils.content import ContentManager
from src.utils.seo import SEOOptimizer

def main():
    # Inicializar componentes
    wp = WordPressClient()
    image_gen = ImageGenerator()
    content_manager = ContentManager()
    seo = SEOOptimizer()
    
    # Título sem data
    title = "Marketing Digital para Clínicas Médicas: Guia Completo"
    
    # Conteúdo base
    content_base = """
    No cenário atual, ter uma presença digital eficaz tornou-se essencial para clínicas médicas que desejam expandir sua base de pacientes e fortalecer sua reputação no mercado. Com a crescente busca por serviços de saúde online, implementar estratégias adequadas de marketing digital pode fazer a diferença entre o sucesso e o anonimato digital.

    Estudos mostram que mais de 70% dos pacientes pesquisam online antes de escolher um profissional de saúde. Uma estratégia de marketing digital bem planejada pode destacar suas qualificações, especialidades e diferenciais, construindo credibilidade com potenciais pacientes. A presença digital profissional transmite confiança e profissionalismo, elementos cruciais na área da saúde.

    O marketing digital oferece diversas ferramentas para clínicas médicas, desde um website profissional até perfis em redes sociais e conteúdo educativo. Estas ferramentas permitem alcançar um público específico, educar sobre condições médicas e tratamentos, e estabelecer sua clínica como referência em sua especialidade. A criação de conteúdo relevante e o engajamento nas redes sociais são fundamentais para manter o interesse do público.

    Para implementar uma estratégia de marketing digital eficaz, considere investir em:
    - Website profissional e otimizado para SEO
    - Presença ativa nas redes sociais relevantes
    - Conteúdo educativo e informativo
    - Sistema de agendamento online
    - Gestão de reputação online

    Estas ações podem transformar visitantes online em pacientes reais para sua clínica.

    Comece hoje mesmo a desenvolver sua presença digital. Identifique os canais mais relevantes para sua especialidade, crie conteúdo que ressoe com seu público-alvo e estabeleça uma comunicação eficiente com seus pacientes atuais e potenciais.
    """
    
    # Estruturar conteúdo no formato ACIDA
    content = content_manager.structure_content(content_base, template="ACIDA")
    
    # Adicionar CTAs
    content = content_manager.add_cta(
        content,
        cta_type="consultoria",
        cta_text="Precisa de ajuda com o marketing digital da sua clínica? A Descomplicar oferece consultoria especializada em marketing digital para profissionais de saúde. Agende uma análise gratuita do seu projeto."
    )
    content = content_manager.add_cta(
        content,
        cta_type="servicos",
        cta_text="Transforme sua Presença Digital. Descubra como a Descomplicar pode ajudar sua clínica a alcançar mais pacientes online com estratégias personalizadas de marketing digital."
    )
    
    # Formatar conteúdo em HTML
    content = content_manager.format_content(
        content,
        format_type="html",
        title=title,
        category="Marketing Digital",
        tags=[
            "marketing digital para clínicas",
            "marketing médico",
            "presença digital na saúde",
            "estratégia digital para médicos",
            "marketing para profissionais de saúde",
            "comunicação em saúde",
            "clínica online",
            "gestão de clínicas"
        ]
    )
    
    # Gerar imagem destacada
    featured_image = image_gen.create_featured_image(
        title=title,
        category="Marketing Digital"
    )
    
    # Extrair palavras-chave do conteúdo
    extracted_keywords = content_manager.extract_keywords(content_base, max_keywords=8)
    
    # Combinar com tags específicas
    tags = list(set(extracted_keywords + [
        "marketing digital para clínicas",
        "marketing médico",
        "presença digital na saúde",
        "estratégia digital para médicos",
        "marketing para profissionais de saúde",
        "comunicação em saúde",
        "clínica online",
        "gestão de clínicas"
    ]))
    
    # Gerar resumo otimizado
    excerpt = content_manager.generate_excerpt(content_base)
    
    # Publicar como rascunho
    result = wp.create_post(
        title=title,
        content=content,
        excerpt=excerpt,
        status="draft",
        category="Marketing Digital",
        tags=tags,
        featured_image=featured_image
    )
    
    # Verificar resultado
    print(f"Artigo publicado com sucesso!")
    print(f"ID: {result['id']}")
    print(f"URL: {result['link']}")
    print(f"Status: {result['status']}")
    print(f"Categoria: {result['category_name']}")
    print(f"Tags: {', '.join(result['tag_names'])}")
    print(f"Imagem Destacada: {result.get('thumbnail', 'Não definida')}")

if __name__ == "__main__":
    main() 