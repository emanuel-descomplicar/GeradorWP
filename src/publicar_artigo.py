#!/usr/bin/env python3
"""
Script para publicar artigos no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
import asyncio
from pathlib import Path
from typing import Dict, List, Any
from dotenv import load_dotenv
from integrations.dify_client import DifyClient
from integrations.wordpress_client import WordPressClient
from image_generator import ImageGenerator

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Carregar variáveis de ambiente
load_dotenv()

async def generate_section_content(section_title: str, topics: list, topic_data: dict) -> str:
    """
    Gera o conteúdo detalhado para cada seção do artigo.
    Utiliza os tópicos fornecidos e os dados do tema para criar parágrafos relevantes.
    """
    dify_client = DifyClient()
    
    # Prompt base para geração de conteúdo
    base_prompt = f"""
    Gere conteúdo detalhado para a seção "{section_title}" de um artigo sobre {topic_data['title']}.
    
    Tópicos a serem abordados:
    {json.dumps(topics, indent=2)}
    
    Dados disponíveis:
    {json.dumps(topic_data, indent=2)}
    
    O conteúdo deve:
    1. Ser escrito em português europeu
    2. Incluir dados e estatísticas relevantes
    3. Citar fontes confiáveis
    4. Usar exemplos práticos
    5. Ter entre 300-500 palavras
    6. Incluir links relevantes
    7. Usar formatação HTML adequada
    """
    
    try:
        # Gera o conteúdo usando a Dify
        response = await dify_client.completion(prompt=base_prompt)
        content = response["choices"][0]["text"]
        
        # Formata o conteúdo em HTML
        formatted_content = f"""
        <div class="section-content">
            {content}
        </div>
        """
        
        return formatted_content
        
    except Exception as e:
        logging.error(f"Erro ao gerar conteúdo para seção {section_title}: {str(e)}")
        # Fallback para template simples em caso de erro
        content = []
        for topic in topics:
            content.append(f"<p>Explicação detalhada sobre {topic.lower()}.</p>")
        return "\n".join(content)

async def generate_article_sections(topic: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Gera automaticamente as seções do artigo com base no tema fornecido.
    
    Args:
        topic (dict): Dicionário com informações do tema
    
    Returns:
        List[Dict[str, Any]]: Lista de seções com título e conteúdo
    """
    dify_client = DifyClient()
    
    # Prompt para geração da estrutura
    structure_prompt = f"""
    Crie uma estrutura de artigo otimizada para o tema: "{topic['title']}".
    
    Informações sobre o tema:
    - Título: {topic['title']}
    - Categoria: {topic['category']}
    - Palavras-chave: {', '.join(topic['keywords'])}
    - Estatísticas relevantes: {json.dumps(topic.get('stats', {}), indent=2)}
    - Ferramentas: {', '.join(topic.get('tools', []))}
    - Exemplos: {', '.join(topic.get('examples', []))}
    
    A estrutura deve ter 8-10 seções, cada uma com 5 subtópicos. Retorne o resultado no seguinte formato JSON:
    
    [
      {{
        "title": "Título da Seção 1",
        "content": [
          "Subtópico 1",
          "Subtópico 2",
          "Subtópico 3",
          "Subtópico 4",
          "Subtópico 5"
        ]
      }},
      {{
        "title": "Título da Seção 2",
        "content": ["Subtópico 1", "Subtópico 2", "Subtópico 3", "Subtópico 4", "Subtópico 5"]
      }}
    ]
    
    Lembre-se que a estrutura deve ser:
    1. Relevante para o tema
    2. Otimizada para SEO
    3. Abrangente, cobrindo os principais aspectos do tema
    4. Focada no mercado português
    5. Prática e útil para o leitor
    6. Organizada em uma progressão lógica (introdução, contexto, métodos, aplicações, conclusões, etc.)
    
    Forneça apenas o JSON sem nenhum texto adicional.
    """
    
    try:
        # Gera a estrutura usando a Dify
        response = await dify_client.completion(prompt=structure_prompt)
        structure_text = response["choices"][0]["text"]
        
        # Tenta extrair o JSON do texto retornado
        # Remove possíveis marcações de código e espaços em branco
        clean_text = structure_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        # Converte a string JSON em uma lista de dicionários
        sections = json.loads(clean_text)
        logging.info(f"Estrutura do artigo gerada com {len(sections)} seções")
        return sections
        
    except Exception as e:
        logging.error(f"Erro ao gerar estrutura do artigo: {str(e)}")
        # Estrutura padrão em caso de erro
        return [
            {
                "title": f"Introdução ao {topic['category']}",
                "content": [
                    "Visão geral do tema",
                    "Importância no contexto atual",
                    "Principais desafios",
                    "Benefícios esperados",
                    "O que esperar deste artigo"
                ]
            },
            {
                "title": f"Fundamentos de {topic['title']}",
                "content": [
                    "Conceitos básicos",
                    "Evolução histórica",
                    "Estado atual em Portugal",
                    "Principais abordagens",
                    "Tendências recentes"
                ]
            },
            {
                "title": "Estratégias Essenciais",
                "content": [
                    "Estratégia 1",
                    "Estratégia 2",
                    "Estratégia 3",
                    "Estratégia 4",
                    "Estratégia 5"
                ]
            },
            {
                "title": "Implementação Prática",
                "content": [
                    "Passos iniciais",
                    "Recursos necessários",
                    "Metodologias recomendadas",
                    "Superação de obstáculos",
                    "Cronograma típico"
                ]
            },
            {
                "title": "Casos de Sucesso",
                "content": [
                    "Caso 1",
                    "Caso 2",
                    "Caso 3",
                    "Caso 4",
                    "Lições aprendidas"
                ]
            },
            {
                "title": "Próximos Passos",
                "content": [
                    "Avaliação inicial",
                    "Planeamento",
                    "Implementação",
                    "Avaliação de resultados",
                    "Melhoria contínua"
                ]
            }
        ]

async def generate_cta_content(topic: Dict[str, Any]) -> Dict[str, str]:
    """
    Gera o conteúdo dos CTAs adaptados ao tema do artigo.
    
    Args:
        topic (dict): Dicionário com informações do tema
    
    Returns:
        Dict[str, str]: Dicionário com os CTAs inicial e final
    """
    dify_client = DifyClient()
    
    # Prompt para geração do CTA
    cta_prompt = f"""
    Crie dois Call-to-Action (CTA) para um artigo sobre "{topic['title']}" para a empresa Descomplicar.
    
    Informações sobre o tema:
    - Título: {topic['title']}
    - Categoria: {topic['category']}
    
    1. CTA Inicial (após a introdução):
    - Deve destacar os serviços da Descomplicar relacionados ao tema
    - Incluir 5 pontos principais (bullets)
    - Ter dois botões: "Marcar Reunião Gratuita" e "Pedir Orçamento"
    
    2. CTA Final (no fim do artigo):
    - Deve incentivar o leitor a agir
    - Enfatizar a expertise da Descomplicar
    - Ter dois botões: "Agendar Consulta Gratuita" e "Falar com Especialista"
    
    Retorne o resultado no seguinte formato JSON:
    {{
      "initial": {{
        "title": "Título do CTA inicial",
        "description": "Texto do CTA inicial",
        "bullets": ["Ponto 1", "Ponto 2", "Ponto 3", "Ponto 4", "Ponto 5"]
      }},
      "final": {{
        "title": "Título do CTA final",
        "description": "Texto do CTA final"
      }}
    }}
    
    Forneça apenas o JSON sem nenhum texto adicional.
    """
    
    try:
        # Gera os CTAs usando a Dify
        response = await dify_client.completion(prompt=cta_prompt)
        cta_text = response["choices"][0]["text"]
        
        # Tenta extrair o JSON do texto retornado
        clean_text = cta_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        # Converte a string JSON em um dicionário
        cta_data = json.loads(clean_text)
        return cta_data
        
    except Exception as e:
        logging.error(f"Erro ao gerar CTAs: {str(e)}")
        # CTAs padrão em caso de erro
        return {
            "initial": {
                "title": f"Precisa de ajuda com {topic['category']}?",
                "description": f"A Descomplicar oferece soluções especializadas para {topic['category']}:",
                "bullets": [
                    "✓ Consultoria Especializada",
                    "✓ Implementação Personalizada",
                    "✓ Formação e Capacitação",
                    "✓ Suporte Contínuo",
                    "✓ Análise de Resultados"
                ]
            },
            "final": {
                "title": f"Pronto para Transformar o Seu Negócio com {topic['category']}?",
                "description": "A Descomplicar está preparada para ajudar a sua empresa a alcançar resultados reais. Podemos começar com uma conversa para entender as suas necessidades específicas."
            }
        }

async def generate_article_structure(topic: dict) -> str:
    """
    Gera a estrutura base do artigo seguindo um template otimizado e adaptado ao tema.
    
    Args:
        topic (dict): Dicionário com informações do tema
            - title: Título principal
            - subtitle: Subtítulo/descrição
            - category: Categoria principal
            - keywords: Lista de palavras-chave
            - stats: Estatísticas relevantes
            - tools: Ferramentas ou soluções
            - examples: Exemplos práticos
    """
    # Gerar seções do artigo
    sections = await generate_article_sections(topic)
    
    # Gerar CTAs adaptados ao tema
    cta_data = await generate_cta_content(topic)
    
    # Gerar conteúdo HTML para cada seção
    html_content = []
    
    # Introdução geral
    html_content.append(f"""
<!-- wp:paragraph -->
<p>{topic['subtitle']}</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{topic.get('featured_image_id')},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large">
    <img src="{topic.get('featured_image_url')}" alt="{topic['title']}" class="wp-image-{topic.get('featured_image_id')}"/>
    <figcaption>Fonte: Descomplicar</figcaption>
</figure>
<!-- /wp:image -->
""")
    
    # CTA inicial após a introdução
    initial_cta = cta_data.get("initial", {})
    bullets_html = "\n".join([f'<li>{bullet}</li>' for bullet in initial_cta.get("bullets", [])])
    
    html_content.append(f"""
<!-- wp:html -->
<div class="cta-box initial" style="background-color: #f5f5f5; padding: 30px; margin: 20px 0; border-radius: 5px;">
    <h3>{initial_cta.get("title", f"Precisa de ajuda com {topic['category']}?")}</h3>
    <p>{initial_cta.get("description", "A Descomplicar oferece soluções especializadas:")}</p>
    <ul style="list-style-type: none; padding-left: 0;">
        {bullets_html}
    </ul>
    <div class="cta-buttons" style="margin-top: 20px;">
        <a href="https://descomplicar.pt/marcar-reuniao/" class="btn btn-primary">Marcar Reunião Gratuita</a>
        <a href="https://descomplicar.pt/pedido-de-orcamento/" class="btn btn-secondary">Pedir Orçamento</a>
    </div>
</div>
<!-- /wp:html -->
""")
    
    # Gerar cada seção
    for section in sections:
        # Título da seção
        html_content.append(f"""
<!-- wp:heading {{"level":2}} -->
<h2>{section['title']}</h2>
<!-- /wp:heading -->
""")
        
        # Conteúdo da seção
        content = await generate_section_content(section['title'], section['content'], topic)
        html_content.append(f"""
<!-- wp:paragraph -->
{content}
<!-- /wp:paragraph -->
""")
    
    # CTA final
    final_cta = cta_data.get("final", {})
    
    html_content.append(f"""
<!-- wp:html -->
<div class="cta-box final" style="background-color: #f2f2f2; padding: 30px; margin: 20px 0; border-radius: 5px;">
    <h3>{final_cta.get("title", f"Pronto para Transformar o Seu Negócio com {topic['category']}?")}</h3>
    <p>{final_cta.get("description", "A Descomplicar está preparada para ajudar a sua empresa a alcançar resultados reais. Podemos começar com uma conversa para entender as suas necessidades específicas.")}</p>
    <div class="cta-buttons" style="margin-top: 20px;">
        <a href="https://descomplicar.pt/marcar-reuniao/" class="btn btn-primary">Agendar Consulta Gratuita</a>
        <a href="https://descomplicar.pt/contacto/" class="btn btn-secondary">Falar com Especialista</a>
    </div>
</div>
<!-- /wp:html -->
""")
    
    return "\n".join(html_content)

async def generate_article_content(titulo: str, categoria: str) -> str:
    """
    Gera o conteúdo do artigo.
    
    Args:
        titulo (str): Título do artigo
        categoria (str): Categoria do artigo
        
    Returns:
        str: Conteúdo HTML completo do artigo
    """
    # Definir informações do tema
    dify_client = DifyClient()
    
    try:
        # Tentar gerar keywords, estatísticas e outros dados via API
        topic_prompt = f"""
        Gere informações detalhadas para um artigo sobre "{titulo}" na categoria "{categoria}".
        
        Retorne apenas o JSON com a seguinte estrutura (sem texto adicional):
        {{
          "keywords": ["keyword1", "keyword2", "keyword3", "keyword4", "keyword5"],
          "subtitle": "Descrição curta do artigo em uma frase",
          "stats": {{
            "stat1_name": "valor estatístico 1",
            "stat2_name": "valor estatístico 2",
            "stat3_name": "valor estatístico 3",
            "stat4_name": "valor estatístico 4",
            "stat5_name": "valor estatístico 5"
          }},
          "tools": ["ferramenta1", "ferramenta2", "ferramenta3", "ferramenta4", "ferramenta5"],
          "examples": ["exemplo1", "exemplo2", "exemplo3", "exemplo4", "exemplo5"]
        }}
        
        As estatísticas devem ser relevantes para o tema em Portugal.
        """
        
        response = await dify_client.completion(prompt=topic_prompt)
        topic_data_text = response["choices"][0]["text"]
        
        # Limpar e processar JSON
        clean_text = topic_data_text.strip()
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
        clean_text = clean_text.strip()
        
        topic_data = json.loads(clean_text)
        
        # Criar o dicionário completo do tópico
        topic = {
            "title": titulo,
            "subtitle": topic_data.get("subtitle", f"Artigo completo sobre {titulo} com informações relevantes para o mercado português."),
            "category": categoria,
            "keywords": topic_data.get("keywords", [categoria, "Portugal", "Tendências", "Estratégias", "Soluções"]),
            "stats": topic_data.get("stats", {"estatística1": "valor1", "estatística2": "valor2"}),
            "tools": topic_data.get("tools", ["Ferramenta 1", "Ferramenta 2", "Ferramenta 3"]),
            "examples": topic_data.get("examples", ["Exemplo 1", "Exemplo 2", "Exemplo 3"])
        }
        
    except Exception as e:
        logging.error(f"Erro ao gerar dados do tópico: {str(e)}")
        # Fallback para dados básicos
        topic = {
            "title": titulo,
            "subtitle": f"Artigo completo sobre {titulo} com informações relevantes para o mercado português.",
            "category": categoria,
            "keywords": [categoria, "Portugal", "Tendências", "Estratégias", "Soluções"],
            "stats": {
                "mercado_portugal": "Dados do mercado português",
                "crescimento": "Taxa de crescimento estimada",
                "adocao": "Nível de adoção em Portugal",
                "impacto": "Impacto nos negócios",
                "investimento": "Investimento médio necessário"
            },
            "tools": [
                "Ferramenta 1",
                "Ferramenta 2",
                "Ferramenta 3",
                "Ferramenta 4",
                "Ferramenta 5"
            ],
            "examples": [
                "Exemplo 1",
                "Exemplo 2",
                "Exemplo 3",
                "Exemplo 4",
                "Exemplo 5"
            ]
        }
    
    # Gerar conteúdo estruturado
    return await generate_article_structure(topic)

async def main():
    """Função principal."""
    try:
        # Obter tema do artigo
        tema = input("Digite o tema do artigo (ou pressione Enter para usar o tema padrão): ")
        
        # Definir tema e categoria
        if tema:
            titulo = tema
            categoria = input("Digite a categoria do artigo: ")
        else:
            titulo = "Transformação Digital para Empresas Tradicionais em Portugal"
            categoria = "Transformação Digital"
        
        # Determinar o status da publicação
        status = input("Digite o status da publicação (draft/publish) ou Enter para draft: ").lower()
        if status != "publish":
            status = "draft"  # Padrão é publicar como rascunho
        
        # Gerar imagem destacada
        image_generator = ImageGenerator()
        image_path = image_generator.create_featured_image(
            title=titulo,
            category=categoria
        )
        
        # Gerar conteúdo do artigo
        content = await generate_article_content(titulo, categoria)
        
        # Publicar no WordPress
        wp_client = WordPressClient()
        
        # Upload da imagem destacada
        featured_image = wp_client.upload_image(
            image_path=image_path,
            title=f"Imagem destacada: {titulo}"
        )
        
        # Publicar o artigo
        result = wp_client.publish_article(
            title=titulo,
            content=content,
            category=categoria,
            featured_image=featured_image,
            status=status
        )
        
        # Verificar resultado da publicação
        if int(result['id']) > 0:
            logging.info(f"Artigo publicado com sucesso no WordPress! ID: {result['id']}")
            logging.info(f"URL: {result['url']}")
            logging.info(f"Status: {result['status']}")
            print(f"\nArtigo publicado com sucesso!")
            print(f"URL: {result['url']}")
            print(f"Status: {result['status']}")
        else:
            logging.error("Falha ao publicar artigo no WordPress.")
            print("\nFalha ao publicar artigo no WordPress.")
        
    except Exception as e:
        logging.error(f"Erro ao publicar artigo: {str(e)}")
        print(f"\nErro ao publicar artigo: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main()) 