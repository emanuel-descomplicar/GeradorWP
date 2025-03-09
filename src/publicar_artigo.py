#!/usr/bin/env python3
"""
Script para publicação de artigos no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import re
import json
import time
import logging
import asyncio
import random
import sys
import unicodedata
from typing import Dict, List, Any, Optional
from pathlib import Path
from dotenv import load_dotenv
from slugify import slugify

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Corrigir caminho para permitir importações relativas
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Importar módulos locais
try:
    # Primeiro tentar importar diretamente (quando chamado de dentro de src/)
    try:
        from integrations.dify_client import DifyClient
        from integrations.wordpress_client import WordPressClient
        from image_generator import ImageGenerator
        logging.info("Módulos importados usando caminhos relativos")
    except ImportError:
        # Se falhar, tentar com prefixo src (quando chamado da raiz)
        from src.integrations.dify_client import DifyClient
        from src.integrations.wordpress_client import WordPressClient
        from src.image_generator import ImageGenerator
        logging.info("Módulos importados usando prefixo src")
except ImportError as e:
    logging.error(f"Erro ao importar módulos locais: {str(e)}")
    sys.exit(1)

# Carregar variáveis de ambiente
load_dotenv()

# IDs das categorias do blog
BLOG_CATEGORIES = {
    'e_commerce': 368,          # blog-e-commerce
    'empreendedorismo': 375,    # blog-empreendedorismo
    'gestao_pmes': 374,         # blog-gestao-pmes
    'ia': 372,                  # blog-inteligencia-artificial
    'marketing_digital': 369,   # blog-marketing-digital
    'tecnologia': 371,          # blog-tecnologia
    'transformacao_digital': 373,# blog-transformacao-digital
    'vendas': 370               # blog-vendas
}

print("=== SCRIPT DE PUBLICAÇÃO INICIADO ===")

print("Importações básicas bem-sucedidas")

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("Importações de módulos locais bem-sucedidas")

print("Inicialização do script concluída")

async def generate_section_content(section_title: str, topics: list, topic_data: dict) -> str:
    """
    Gera o conteúdo detalhado para uma seção do artigo.
    
    Args:
        section_title (str): Título da seção
        topics (list): Lista de tópicos da seção
        topic_data (dict): Dados do tema principal
        
    Returns:
        str: Conteúdo HTML da seção
    """
    # Evitar títulos duplicados removendo o título principal do artigo se estiver no título da seção
    main_title = topic_data.get('title', '')
    section_id = slugify(section_title.lower())
    
    # Inicializar cliente Dify
    dify_client = DifyClient()
    
    # Converter título da seção para não ter o mesmo texto que o título principal
    if main_title in section_title and section_title != main_title:
        display_title = section_title.replace(main_title, '').strip()
        if not display_title:
            display_title = section_title
    else:
        display_title = section_title
    
    # Gerar prompt para o Dify
    prompt = f"""
    Gere conteúdo detalhado para a seção "{display_title}" de um artigo sobre {topic_data.get('title')}.
    
    Tópicos a serem abordados:
    {json.dumps(topics, ensure_ascii=False)}
    
    Dados disponíveis:
    {json.dumps(topic_data, ensure_ascii=False)}
    
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
        response = await dify_client.completion(prompt)
        html_content = response['choices'][0]['text']
        
        # Extrair o conteúdo HTML da resposta
        html_content = extract_html_from_response(html_content)
        
        # Remover os blocos de código e tags HTML visíveis
        html_content = html_content.replace('```html', '').replace('```', '')
        
        # Se não tiver uma tag section, adicionar
        if not html_content.strip().startswith('<section'):
            html_content = f'<section id="{section_id}" class="article-section">\n{html_content}\n</section>'
        
        return html_content
    except Exception as e:
        logging.error(f"Erro ao gerar conteúdo da seção '{section_title}': {e}")
        return f"<section id='{section_id}' class='article-section'><h2>{display_title}</h2><p>Conteúdo indisponível.</p></section>"

def extract_html_from_response(response):
    """
    Extrai HTML de uma resposta de texto.
    
    Args:
        response (str): Resposta contendo HTML
        
    Returns:
        str: HTML extraído da resposta
    """
    # Tentar encontrar o HTML em diferentes formatos
    html_pattern = r'```html\s*(.*?)```'
    matches = re.findall(html_pattern, response, re.DOTALL)
    if matches:
        return matches[0]
    
    # Se não encontrar HTML específico, procurar qualquer código
    code_pattern = r'```(?:.*?)\s*(.*?)```'
    matches = re.findall(code_pattern, response, re.DOTALL)
    if matches:
        return matches[0]
    
    # Se não encontrar nada em blocos de código, retornar a resposta original
    return response

def slugify(text):
    """
    Converte texto para slug (para usar em IDs).
    
    Args:
        text (str): Texto a ser convertido
        
    Returns:
        str: Slug gerado a partir do texto
    """
    # Remover acentos
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('ASCII')
    # Converter para minúsculas e substituir espaços por hífens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    # Substituir múltiplos espaços por um único hífen
    text = re.sub(r'[-\s]+', '-', text).strip('-_')
    return text

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

async def generate_cta_content(topic_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Gera o conteúdo dos Call-to-Action (CTA) inicial e final.
    
    Args:
        topic_data (Dict[str, Any]): Dados do tópico para personalizar os CTAs
        
    Returns:
        Dict[str, str]: Dicionário com os CTAs inicial e final em HTML
    """
    dify_client = DifyClient()
    
    try:
        prompt = f"""
    Crie dois Call-to-Action (CTA) para um artigo sobre "{topic_data['title']}" para a empresa Descomplicar.
    
    Informações sobre o tema:
    - Título: {topic_data['title']}
    - Categoria: {topic_data['category']}
    
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
        
        response = await dify_client.completion(prompt=prompt)
        cta_text = response["choices"][0]["text"]
        
        # Limpar o texto do JSON
        clean_text = cta_text.strip()
        
        # Remover delimitadores de código
        if clean_text.startswith("```json"):
            clean_text = clean_text[7:]
        elif clean_text.startswith("```"):
            clean_text = clean_text[3:]
            
        if clean_text.endswith("```"):
            clean_text = clean_text[:-3]
            
        clean_text = clean_text.strip()
        
        # Tentar analisar o JSON
        try:
            cta_data = json.loads(clean_text)
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao fazer parse do JSON dos CTAs: {str(e)}")
            logging.error(f"Texto JSON recebido: {clean_text}")
            # Usar CTAs padrão em caso de erro
            cta_data = {
                "initial": {
                    "title": "Precisa de ajuda com a sua estratégia?",
                    "description": "A Descomplicar oferece serviços especializados para ajudar a sua empresa a crescer.",
                    "bullets": [
                        "Consultoria personalizada",
                        "Implementação de soluções",
                        "Formação da sua equipa",
                        "Suporte contínuo",
                        "Resultados mensuráveis"
                    ]
                },
                "final": {
                    "title": "Pronto para dar o próximo passo?",
                    "description": "Entre em contacto connosco hoje e veja como podemos ajudar a sua empresa a crescer."
                }
            }
        
        # Criar HTML para o CTA inicial
        initial_cta = f"""
        <div class="cta-box initial-cta">
            <h3>{cta_data['initial']['title']}</h3>
            <p>{cta_data['initial']['description']}</p>
            <ul>
                {''.join([f'<li>{bullet}</li>' for bullet in cta_data['initial']['bullets']])}
            </ul>
            <div class="cta-buttons">
                <a href="https://descomplicar.pt/contacto/" class="button primary">Marcar Reunião Gratuita</a>
                <a href="https://descomplicar.pt/orcamento/" class="button secondary">Pedir Orçamento</a>
            </div>
        </div>
        """
        
        # Criar HTML para o CTA final
        final_cta = f"""
        <div class="cta-box final-cta">
            <h3>{cta_data['final']['title']}</h3>
            <p>{cta_data['final']['description']}</p>
            <div class="cta-buttons">
                <a href="https://descomplicar.pt/contacto/" class="button primary">Agendar Consulta Gratuita</a>
                <a href="https://descomplicar.pt/contacto/" class="button secondary">Falar com Especialista</a>
            </div>
        </div>
        """
        
        return {
            "initial": initial_cta,
            "final": final_cta
        }
        
    except Exception as e:
        logging.error(f"Erro ao gerar CTAs: {str(e)}")
        # Retornar CTAs padrão em caso de erro
        return {
            "initial": """
            <div class="cta-box initial-cta">
                <h3>Precisa de ajuda com a sua estratégia?</h3>
                <p>A Descomplicar oferece serviços especializados para ajudar a sua empresa a crescer.</p>
                <ul>
                    <li>Consultoria personalizada</li>
                    <li>Implementação de soluções</li>
                    <li>Formação da sua equipa</li>
                    <li>Suporte contínuo</li>
                    <li>Resultados mensuráveis</li>
                </ul>
                <div class="cta-buttons">
                    <a href="https://descomplicar.pt/contacto/" class="button primary">Marcar Reunião Gratuita</a>
                    <a href="https://descomplicar.pt/orcamento/" class="button secondary">Pedir Orçamento</a>
                </div>
            </div>
            """,
            "final": """
            <div class="cta-box final-cta">
                <h3>Pronto para dar o próximo passo?</h3>
                <p>Entre em contacto connosco hoje e veja como podemos ajudar a sua empresa a crescer.</p>
                <div class="cta-buttons">
                    <a href="https://descomplicar.pt/contacto/" class="button primary">Agendar Consulta Gratuita</a>
                    <a href="https://descomplicar.pt/contacto/" class="button secondary">Falar com Especialista</a>
                </div>
            </div>
            """
        }

def clean_html_content(content: str, initial_cta: str) -> str:
    """
    Limpa o conteúdo HTML e adiciona o CTA inicial após a introdução.
    
    Args:
        content (str): O conteúdo HTML a ser limpo
        initial_cta (str): O CTA inicial a ser inserido após a introdução
        
    Returns:
        str: O conteúdo HTML limpo e estruturado
    """
    # Remover tags "`html" e "`" do conteúdo
    content = content.replace('```html', '')
    content = content.replace('```', '')
    
    # Substituir títulos de "Introdução" e "Conclusão" se existirem
    content = content.replace('<h2>Introdução à Transformação Digital</h2>', 
                             '<h2>O Caminho para a Digitalização Empresarial</h2>')
    content = content.replace('<h2>Conclusão e Próximos Passos</h2>', 
                             '<h2>Rumo ao Futuro Digital</h2>')
    
    # Verificar se o conteúdo está vazio ou muito curto
    if not content or len(content.strip()) < 50:
        logging.warning("Conteúdo HTML muito curto ou vazio após limpeza.")
        return "<h2>Erro ao gerar conteúdo</h2><p>Não foi possível gerar o conteúdo do artigo.</p>"
    
    # Estruturar o conteúdo em seções se não estiver
    if '<section' not in content:
        content = f"<section class=\"main-content\">\n{content}\n</section>"
    
    # Dividir o conteúdo para inserir o CTA após a primeira seção (introdução)
    sections = content.split('</section>')
    
    if len(sections) > 1:
        # Inserir o CTA após a primeira seção
        sections[0] += '</section>'  # Fechar a primeira seção
        restructured_content = sections[0] + initial_cta + ''.join(sections[1:])
        
        # Garantir que todas as seções estão fechadas
        if not restructured_content.endswith('</section>'):
            restructured_content += '</section>'
    else:
        # Se não conseguir dividir em seções, inserir o CTA após o primeiro <h2>
        h2_parts = content.split('</h2>', 1)
        
        if len(h2_parts) > 1:
            restructured_content = h2_parts[0] + '</h2>' + initial_cta + h2_parts[1]
        else:
            # Última opção: inserir o CTA no início do conteúdo
            restructured_content = initial_cta + content
    
    # Garantir que não haja duplicação de tags e que o HTML seja válido
    restructured_content = restructured_content.replace('</section></section>', '</section>')
    
    return restructured_content

async def generate_article_structure(topic: dict) -> str:
    """
    Gera a estrutura do artigo com base no tema, com conteúdo completo para cada seção.
    
    Args:
        topic (dict): Informações do tema
        
    Returns:
        str: Estrutura HTML do artigo com conteúdo completo
    """
    dify_client = DifyClient()
    
    try:
        prompt = f"""
    Crie um artigo completo e detalhado sobre o tema: "{topic['title']}".
    
    Informações sobre o tema:
    - Título: {topic['title']}
    - Categoria: {topic['category']}
    - Palavras-chave: {', '.join(topic['keywords'])}
    - Estatísticas relevantes: {json.dumps(topic['stats'])}
    - Ferramentas: {', '.join(topic['tools'])}
    - Exemplos: {', '.join(topic['examples'])}
    
    O artigo deve ter 8-10 seções, cada uma com um título e conteúdo completo (parágrafos detalhados, não apenas tópicos).
    Retorne o resultado no seguinte formato JSON:
    
    [
      {{
        "title": "Título da Seção 1",
        "content": "Parágrafo completo com várias frases detalhando este tópico. Deve incluir informações relevantes, exemplos e dados estatísticos quando apropriado. O conteúdo deve ter pelo menos 3-4 parágrafos por seção, com informações úteis e práticas."
      }},
      {{
        "title": "Título da Seção 2",
        "content": "Parágrafo completo com várias frases detalhando este tópico. Deve incluir informações relevantes, exemplos e dados estatísticos quando apropriado. O conteúdo deve ter pelo menos 3-4 parágrafos por seção, com informações úteis e práticas."
      }}
    ]
    
    Lembre-se que o artigo deve ser:
    1. Relevante para o tema
    2. Otimizado para SEO
    3. Abrangente, cobrindo os principais aspectos do tema
    4. Focado no mercado português
    5. Prático e útil para o leitor
    6. Organizado em uma progressão lógica (introdução, contexto, métodos, aplicações, conclusões, etc.)
    7. Escrito em português de Portugal (não brasileiro)
    8. Com parágrafos completos e bem desenvolvidos
    9. Com exemplos práticos e casos de uso reais
    10. Com estatísticas e dados relevantes incorporados no texto
    
    Forneça apenas o JSON sem nenhum texto adicional.
    """
        
        response = await dify_client.completion(prompt=prompt)
        structure_text = response["choices"][0]["text"]
        
        # Limpar o texto do JSON
        clean_text = structure_text.strip()
        
        # Remover delimitadores de código e texto adicional
        if "```json" in clean_text:
            clean_text = clean_text.split("```json", 1)[1]
        if "```" in clean_text:
            clean_text = clean_text.split("```", 1)[0]
            
        clean_text = clean_text.strip()
        
        try:
            # Tentar fazer o parse do JSON
            sections = json.loads(clean_text)
            logging.info(f"Estrutura gerada com {len(sections)} seções")
            
            # Montar o HTML da estrutura do artigo com conteúdo completo
            html_structure = ""
            for section in sections:
                html_structure += f'<section class="article-section">\n'
                html_structure += f'<h2>{section["title"]}</h2>\n'
                
                # Adicionar o conteúdo completo em vez de lista de tópicos
                content_paragraphs = section["content"]
                
                # Se o conteúdo for uma string, dividir em parágrafos
                if isinstance(content_paragraphs, str):
                    # Dividir por quebras de linha ou pontos finais seguidos de espaço
                    paragraphs = [p.strip() for p in re.split(r'\n+', content_paragraphs) if p.strip()]
                    
                    # Se não houver parágrafos definidos, tentar dividir por frases longas
                    if len(paragraphs) <= 1:
                        paragraphs = [p.strip() + "." for p in re.split(r'(?<=[.!?])\s+', content_paragraphs) if p.strip()]
                    
                    # Se ainda assim tivermos apenas um parágrafo, usá-lo como está
                    for paragraph in paragraphs:
                        if paragraph:
                            html_structure += f'<p>{paragraph}</p>\n'
                # Se for uma lista, usar cada item como um parágrafo
                elif isinstance(content_paragraphs, list):
                    for paragraph in content_paragraphs:
                        if paragraph:
                            html_structure += f'<p>{paragraph}</p>\n'
                
                html_structure += f'</section>\n'
                
            return html_structure
            
        except json.JSONDecodeError as e:
            logging.error(f"Erro ao fazer parse do JSON da estrutura: {str(e)}")
            logging.error(f"Texto JSON recebido: {clean_text}")
            
            # Se falhar, usar uma estrutura padrão
            return generate_fallback_structure(topic)
    except Exception as e:
        logging.error(f"Erro ao gerar estrutura do artigo: {str(e)}")
        return generate_fallback_structure(topic)

def generate_fallback_structure(topic: dict) -> str:
    """
    Gera uma estrutura padrão para o artigo quando ocorrem erros, com conteúdo completo.
    
    Args:
        topic: Dados do tema
        
    Returns:
        str: Estrutura padrão do artigo em HTML com conteúdo completo
    """
    sections = [
        {
            "title": "Introdução",
            "content": f"<p>Neste artigo, vamos explorar em profundidade o tema {topic['title']}. Este é um assunto de grande relevância no contexto atual do mercado português, especialmente na área de {topic['category']}.</p><p>De acordo com dados recentes, {list(topic['stats'].values())[0] if topic['stats'] else 'o mercado tem mostrado um crescimento significativo nesta área'}. Isto demonstra a importância de compreender e implementar estratégias eficazes relacionadas a este tema.</p><p>Ao longo deste artigo, abordaremos os principais conceitos, metodologias e aplicações práticas, fornecendo exemplos concretos e dicas úteis para profissionais e empresas que desejam aprimorar seus conhecimentos e resultados nesta área.</p>"
        },
        {
            "title": f"O que é {topic['title']} e sua importância",
            "content": f"<p>{topic['title']} refere-se a um conjunto de práticas e estratégias fundamentais no contexto atual de {topic['category']}. A sua importância tem crescido significativamente nos últimos anos, especialmente em Portugal, onde {list(topic['stats'].values())[1] if len(topic['stats']) > 1 else 'empresas têm investido cada vez mais nesta área'}.</p><p>Entre os principais benefícios de implementar estas estratégias estão o aumento da eficiência operacional, a melhoria da experiência do cliente e o incremento nos resultados de negócio. Empresas que adotam estas práticas frequentemente reportam {list(topic['stats'].values())[2] if len(topic['stats']) > 2 else 'melhorias significativas nos seus indicadores de desempenho'}.</p><p>No contexto português, é especialmente relevante considerar as particularidades do mercado local e adaptar as estratégias globais às necessidades específicas das empresas e consumidores portugueses.</p>"
        },
        {
            "title": "Principais estratégias e metodologias",
            "content": f"<p>Para implementar {topic['title']} de forma eficaz, é essencial adotar metodologias comprovadas e estratégias bem definidas. Entre as abordagens mais eficazes, destacam-se a análise detalhada do contexto atual, o planeamento estratégico baseado em dados e a implementação faseada com monitorização contínua.</p><p>Ferramentas como {', '.join(topic['tools'][:3]) if topic['tools'] else 'diversas soluções tecnológicas disponíveis no mercado'} são fundamentais para suportar estas estratégias. Estas soluções permitem automatizar processos, analisar dados de forma eficiente e otimizar resultados.</p><p>Casos de sucesso como {topic['examples'][0] if topic['examples'] else 'várias empresas portuguesas'} demonstram que a aplicação correta destas metodologias pode resultar em {list(topic['stats'].values())[3] if len(topic['stats']) > 3 else 'ganhos significativos de produtividade e rentabilidade'}.</p>"
        },
        {
            "title": "Implementação prática em empresas portuguesas",
            "content": f"<p>A implementação de {topic['title']} em empresas portuguesas requer uma abordagem adaptada à realidade local. O processo geralmente começa com uma avaliação detalhada da situação atual, identificação de oportunidades de melhoria e definição de objetivos claros e mensuráveis.</p><p>Entre os desafios mais comuns enfrentados pelas empresas portuguesas estão a resistência à mudança, a limitação de recursos e a falta de conhecimento especializado. Para superar estes obstáculos, é recomendável investir em formação, buscar parcerias estratégicas e implementar mudanças de forma gradual e bem comunicada.</p><p>Empresas como {topic['examples'][1] if len(topic['examples']) > 1 else 'líderes do mercado português'} têm demonstrado que é possível superar estes desafios e alcançar resultados expressivos, mesmo em contextos desafiadores.</p>"
        },
        {
            "title": "Ferramentas e recursos essenciais",
            "content": f"<p>Para implementar {topic['title']} de forma eficaz, é fundamental contar com as ferramentas e recursos adequados. Entre as soluções mais recomendadas para o mercado português, destacam-se {', '.join(topic['tools']) if topic['tools'] else 'diversas plataformas e tecnologias especializadas'}.</p><p>Estas ferramentas oferecem funcionalidades como análise de dados, automação de processos, monitorização de resultados e otimização contínua. A escolha das soluções mais adequadas deve considerar fatores como o tamanho da empresa, o orçamento disponível, os objetivos específicos e a compatibilidade com sistemas existentes.</p><p>Além das ferramentas tecnológicas, é essencial investir em recursos humanos qualificados, seja através da contratação de especialistas, da formação da equipe atual ou da parceria com consultores externos especializados.</p>"
        },
        {
            "title": "Tendências e futuro",
            "content": f"<p>O futuro de {topic['title']} apresenta tendências promissoras e desafios significativos. Entre as principais tendências para os próximos anos, destacam-se a crescente integração com tecnologias emergentes como inteligência artificial e análise avançada de dados, a personalização cada vez mais refinada e a adoção de abordagens ágeis e adaptativas.</p><p>No contexto português, espera-se um crescimento contínuo na adoção destas práticas, impulsionado por {list(topic['stats'].values())[4] if len(topic['stats']) > 4 else 'fatores como a transformação digital acelerada e a necessidade de maior competitividade'}.</p><p>Empresas que se anteciparem a estas tendências e investirem de forma estratégica em {topic['title']} estarão melhor posicionadas para enfrentar os desafios futuros e aproveitar as oportunidades emergentes no mercado.</p>"
        },
        {
            "title": "Casos de sucesso em Portugal",
            "content": f"<p>Diversos casos de sucesso em Portugal demonstram o potencial transformador de {topic['title']} quando implementado de forma estratégica e consistente. {topic['examples'][0] if topic['examples'] else 'Empresas líderes em diversos setores'} conseguiram {list(topic['stats'].values())[0] if topic['stats'] else 'resultados expressivos'} após a implementação destas estratégias.</p><p>Por exemplo, {topic['examples'][1] if len(topic['examples']) > 1 else 'uma empresa do setor de serviços'} reportou {list(topic['stats'].values())[1] if len(topic['stats']) > 1 else 'melhorias significativas nos seus indicadores de desempenho'} após adotar uma abordagem estruturada baseada nas melhores práticas de {topic['title']}.</p><p>Estes casos demonstram que, independentemente do tamanho ou setor da empresa, é possível alcançar resultados expressivos com a implementação adequada destas estratégias, desde que haja comprometimento, planeamento e execução consistente.</p>"
        },
        {
            "title": "Erros comuns a evitar",
            "content": f"<p>Na implementação de estratégias de {topic['title']}, diversos erros comuns podem comprometer os resultados esperados. Entre os mais frequentes estão a falta de planeamento adequado, a ausência de objetivos claros e mensuráveis, a resistência à mudança não gerida adequadamente e a falta de monitorização e ajustes contínuos.</p><p>Outro erro significativo é a tentativa de implementar soluções genéricas sem adaptá-las ao contexto específico da empresa e do mercado português. Cada organização tem suas particularidades, e as estratégias devem ser personalizadas para atender às suas necessidades e objetivos específicos.</p><p>Para evitar estes erros, é recomendável investir em planeamento detalhado, envolver as partes interessadas desde o início, estabelecer métricas claras de sucesso e adotar uma abordagem iterativa que permita ajustes contínuos com base nos resultados obtidos.</p>"
        },
        {
            "title": "Conclusão",
            "content": f"<p>Ao longo deste artigo, exploramos diversos aspectos relacionados a {topic['title']}, desde conceitos fundamentais até aplicações práticas no contexto português. Ficou evidente a importância crescente deste tema para empresas que buscam manter-se competitivas e relevantes no cenário atual.</p><p>As estratégias, metodologias e ferramentas apresentadas oferecem um ponto de partida sólido para organizações que desejam implementar ou aprimorar suas iniciativas nesta área. Os casos de sucesso mencionados demonstram que, com a abordagem adequada, é possível alcançar resultados expressivos, mesmo em contextos desafiadores.</p><p>Recomendamos que empresas interessadas em explorar este tema comecem com uma avaliação detalhada da sua situação atual, definam objetivos claros e mensuráveis, e desenvolvam um plano de implementação faseado que considere as particularidades do seu negócio e do mercado português.</p>"
        }
    ]
    
    html_structure = ""
    for section in sections:
        html_structure += f'<section class="article-section">\n'
        html_structure += f'<h2>{section["title"]}</h2>\n'
        html_structure += f'{section["content"]}\n'
        html_structure += f'</section>\n'
        
    return html_structure

async def generate_article_content(titulo: str, categoria: str) -> str:
    """
    Gera o conteúdo completo do artigo.
    
    Args:
        titulo (str): O título do artigo
        categoria (str): A categoria do artigo
        
    Returns:
        str: O conteúdo HTML completo do artigo
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
    content = await generate_article_structure(topic)
    
    # Gerar os CTAs
    cta_content = await generate_cta_content(topic)
    
    # Construir o artigo completo
    article_html = f"""
    <article class="transformacao-digital-article">
        {content}
        {cta_content['final']}
    </article>
    <style>
    .cta-box {{
        background-color: #f8f9fa;
        border-left: 5px solid #0066cc;
        padding: 20px;
        margin: 30px 0;
        border-radius: 5px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }}
    
    .cta-box h3 {{
        color: #0066cc;
        margin-top: 0;
    }}
    
    .cta-buttons {{
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }}
    
    .cta-button {{
        display: inline-block;
        padding: 10px 20px;
        text-decoration: none;
        border-radius: 4px;
        font-weight: bold;
        text-align: center;
    }}
    
    .cta-button.primary {{
        background-color: #0066cc;
        color: white;
    }}
    
    .cta-button.secondary {{
        background-color: #ffffff;
        color: #0066cc;
        border: 1px solid #0066cc;
    }}
    </style>
    """
    
    # Limpar e estruturar o conteúdo
    cleaned_article = clean_html_content(article_html, cta_content['initial'])
    
    return cleaned_article

async def process_topic(tema: str, categoria: str, status: str = "draft") -> Dict[str, Any]:
    """
    Processa um tópico individual, gerando e publicando um artigo.
    
    Args:
        tema (str): Tema do artigo
        categoria (str): Categoria do artigo
        status (str): Status da publicação (draft/publish)
        
    Returns:
        Dict[str, Any]: Resultado da publicação
    """
    try:
        logging.info(f"Processando tópico: {tema} (Categoria: {categoria}, Status: {status})")
        
        # Gerar imagem destacada
        logging.info(f"Gerando imagem destacada para o tema: {tema}")
        img_generator = ImageGenerator()
        image_path = img_generator.create_featured_image(tema, categoria)
        logging.info(f"Imagem gerada em: {image_path}")
        
        # Gerar conteúdo do artigo
        logging.info("Gerando conteúdo do artigo...")
        content = await generate_article_content(tema, categoria)
        logging.info("Conteúdo do artigo gerado com sucesso.")
        
        # Obter palavras-chave e tags
        palavras_chave = []
        try:
            # Tentar extrair palavras-chave do conteúdo gerado
            match = re.search(r'keywords":\s*\[(.*?)\]', content, re.DOTALL)
            if match:
                keywords_str = match.group(1)
                # Extrair cada palavra-chave entre aspas
                palavras_chave = re.findall(r'"(.*?)"', keywords_str)
                logging.info(f"Palavras-chave extraídas: {palavras_chave}")
        except Exception as e:
            logging.warning(f"Não foi possível extrair palavras-chave: {e}")
        
        # Se não foi possível extrair, usar algumas padrão baseadas no tema
        if not palavras_chave:
            logging.info("Gerando palavras-chave alternativas...")
            # Gerar palavras-chave básicas baseadas no tema e categoria
            temas_base = [tema.lower(), categoria.lower()]
            palavras_chave = []
            for tema_base in temas_base:
                palavras_chave.extend(tema_base.split())
            # Remover duplicados e palavras muito curtas
            palavras_chave = list(set([p for p in palavras_chave if len(p) > 3]))[:5]
            logging.info(f"Palavras-chave alternativas geradas: {palavras_chave}")
        
        # Determinar categoria ID com base no nome
        categoria_id = None
        categoria_lower = categoria.lower().replace(' ', '_')
        
        # Tentar encontrar a categoria pelo nome no dicionário BLOG_CATEGORIES
        for cat_name, cat_id in BLOG_CATEGORIES.items():
            if cat_name in categoria_lower or categoria_lower in cat_name:
                categoria_id = cat_id
                logging.info(f"Categoria encontrada pelo nome: {cat_name} (ID: {cat_id})")
                break
        
        # Se não encontrar, usar 1 (padrão/sem categoria)
        if not categoria_id:
            categoria_id = 1
            logging.warning(f"Categoria não encontrada. Usando ID padrão: {categoria_id}")
        
        # Inicializar cliente WordPress
        wp_client = WordPressClient()
        
        # Fazer upload da imagem destacada
        logging.info("Fazendo upload da imagem destacada...")
        img_result = wp_client.upload_image(image_path, slugify(tema))
        
        if img_result and 'id' in img_result:
            featured_image_id = img_result['id']
            logging.info(f"Imagem carregada com sucesso. ID: {featured_image_id}, URL: {img_result.get('url', 'N/A')}")
        else:
            featured_image_id = None
            logging.warning("Não foi possível carregar a imagem destacada.")
        
        # Publicar artigo
        logging.info(f"Publicando artigo no WordPress com status: {status}")
        result = wp_client.publish_article(
            title=tema,
            content=content,
            category=categoria_id,  # Usar ID numérico
            featured_image=featured_image_id,
            status=status,
            tags=palavras_chave
        )
        
        # Verificar resultado
        if result and int(result.get('id', 0)) > 0:
            logging.info(f"Artigo publicado com sucesso. ID: {result['id']}, URL: {result.get('link', 'N/A')}")
            logging.info(f"Status: {status}")
            
            return {
                "success": True,
                "id": result['id'],
                "url": result.get('link', 'N/A'),
                "tema": tema,
                "categoria": categoria,
                "status": status
            }
        else:
            error_msg = result.get('error', 'Erro desconhecido')
            logging.error(f"Falha ao publicar artigo no WordPress: {error_msg}")
            
            return {
                "success": False,
                "error": error_msg,
                "tema": tema,
                "categoria": categoria,
                "status": status
            }
    except Exception as e:
        logging.error(f"Erro ao processar tópico {tema}: {str(e)}")
        return {
            "success": False,
            "error": str(e),
            "tema": tema,
            "categoria": categoria,
            "status": status
        }

async def process_topics_from_file(file_path: str, status: str = "draft") -> List[Dict[str, Any]]:
    """
    Processa uma lista de tópicos de um ficheiro CSV ou JSON.
    
    Formato do CSV esperado:
    tema,categoria
    "Transformação Digital para PMEs","Marketing Digital"
    "SEO para E-commerce","Marketing Digital"
    
    Formato do JSON esperado:
    [
      {"tema": "Transformação Digital para PMEs", "categoria": "Marketing Digital"},
      {"tema": "SEO para E-commerce", "categoria": "Marketing Digital"}
    ]
    
    Args:
        file_path (str): Caminho para o ficheiro CSV ou JSON
        status (str): Status da publicação (draft/publish)
        
    Returns:
        List[Dict[str, Any]]: Lista com os resultados de cada publicação
    """
    results = []
    
    if not os.path.exists(file_path):
        logging.error(f"Ficheiro não encontrado: {file_path}")
        return []
    
    logging.info(f"Processando tópicos do ficheiro: {file_path}")
    
    try:
        # Determinar o tipo de ficheiro pela extensão
        if file_path.lower().endswith('.json'):
            # Ler ficheiro JSON
            with open(file_path, 'r', encoding='utf-8') as f:
                topics = json.load(f)
                
            if not isinstance(topics, list):
                logging.error("Formato JSON inválido. Deve ser uma lista de objetos.")
                return []
            
            # Mostrar informação sobre o número de tópicos a processar
            total_topics = len(topics)
            print(f"\n=== Processando {total_topics} tópicos do ficheiro JSON ===\n")
            
            for i, item in enumerate(topics, 1):
                if not isinstance(item, dict) or 'tema' not in item or 'categoria' not in item:
                    logging.warning(f"Item ignorado por formato inválido: {item}")
                    continue
                    
                # Definir status específico por tópico se existir no item
                topic_status = item.get('status', status)
                
                # Mostrar progresso
                print(f"Processando tópico {i}/{total_topics}: {item['tema']}")
                
                # Processar o tópico
                result = await process_topic(item['tema'], item['categoria'], topic_status)
                results.append(result)
                
                # Pausa entre processamentos para não sobrecarregar a API (30 segundos)
                if i < total_topics:
                    logging.info(f"Pausa de 30 segundos antes do próximo tópico...")
                    print(f"Pausa de 30 segundos antes do próximo tópico... ", end="", flush=True)
                    
                    # Contador visual de espera
                    for j in range(30, 0, -1):
                        time.sleep(1)
                        if j % 5 == 0 or j <= 5:
                            print(f"{j}... ", end="", flush=True)
                    
                    print("Continuando!\n")
                
        elif file_path.lower().endswith('.csv'):
            # Ler ficheiro CSV
            import csv
            
            # Primeiro contar o número de linhas para saber o total
            with open(file_path, 'r', encoding='utf-8') as f:
                total_topics = sum(1 for _ in csv.reader(f)) - 1  # -1 para desconsiderar o cabeçalho
            
            print(f"\n=== Processando {total_topics} tópicos do ficheiro CSV ===\n")
            
            # Agora processar o CSV
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                header = next(reader, None)  # Pular cabeçalho
                
                for i, row in enumerate(reader, 1):
                    if len(row) < 2:
                        logging.warning(f"Linha ignorada por formato inválido: {row}")
                        continue
                        
                    tema = row[0].strip()
                    categoria = row[1].strip()
                    
                    # Usar o 3º campo como status, se existir
                    topic_status = row[2].strip() if len(row) > 2 else status
                    
                    # Mostrar progresso
                    print(f"Processando tópico {i}/{total_topics}: {tema}")
                    
                    result = await process_topic(tema, categoria, topic_status)
                    results.append(result)
                    
                    # Pausa entre processamentos para não sobrecarregar a API (30 segundos)
                    if i < total_topics:
                        logging.info(f"Pausa de 30 segundos antes do próximo tópico...")
                        print(f"Pausa de 30 segundos antes do próximo tópico... ", end="", flush=True)
                        
                        # Contador visual de espera
                        for j in range(30, 0, -1):
                            time.sleep(1)
                            if j % 5 == 0 or j <= 5:
                                print(f"{j}... ", end="", flush=True)
                        
                        print("Continuando!\n")
        else:
            logging.error(f"Formato de ficheiro não suportado: {file_path}")
            return []
            
    except Exception as e:
        logging.error(f"Erro ao processar ficheiro {file_path}: {str(e)}")
        
    logging.info(f"Processamento concluído. {len(results)} tópico(s) processados.")
    return results

async def main():
    """
    Função principal que coordena todo o processo de publicação de artigo.
    """
    # Verificar argumentos da linha de comando
    import argparse
    parser = argparse.ArgumentParser(description='Gerador de artigos para WordPress')
    parser.add_argument('--tema', '-t', help='Tema do artigo')
    parser.add_argument('--categoria', '-c', help='Categoria do artigo')
    parser.add_argument('--status', '-s', default='draft', help='Status da publicação (draft/publish)')
    parser.add_argument('--file', '-f', help='Caminho para ficheiro CSV/JSON com lista de tópicos')
    parser.add_argument('--batch', '-b', action='store_true', help='Modo de processamento em lote (interativo)')
    
    args = parser.parse_args()
    
    try:
        # 1. Modo de processamento em lote a partir de ficheiro
        if args.file:
            logging.info(f"Iniciando processamento em lote do ficheiro: {args.file}")
            results = await process_topics_from_file(args.file, args.status)
            
            # Mostrar resumo dos resultados
            print("\n=== Resumo do Processamento em Lote ===")
            print(f"Total de tópicos processados: {len(results)}")
            print(f"Publicações bem-sucedidas: {sum(1 for r in results if r.get('success', False))}")
            print(f"Falhas: {sum(1 for r in results if not r.get('success', False))}")
            
            # Mostrar detalhes
            print("\nDetalhes das publicações:")
            for i, result in enumerate(results, 1):
                status_text = "✅ Sucesso" if result.get('success', False) else "❌ Falha"
                print(f"{i}. {result.get('tema')}: {status_text}")
                if result.get('success', False):
                    print(f"   URL: {result.get('url', 'N/A')}")
                else:
                    print(f"   Erro: {result.get('error', 'Desconhecido')}")
                    
            return
            
        # 2. Modo de processamento individual com argumentos da linha de comando
        elif args.tema:
            categoria = args.categoria or "Marketing Digital"
            logging.info(f"Processando tópico individual: {args.tema} (Categoria: {categoria})")
            result = await process_topic(args.tema, categoria, args.status)
            
            if result.get('success', False):
                print(f"\nArtigo publicado com sucesso!")
                print(f"URL: {result.get('url', 'N/A')}")
                print(f"Status: {args.status}")
            else:
                print(f"\nFalha ao publicar artigo: {result.get('error', 'Erro desconhecido')}")
                
            return
            
        # 3. Modo de processamento em lote interativo
        elif args.batch:
            print("=== Modo de Processamento em Lote Interativo ===")
            print("Digite 'fim' no tema para encerrar.")
            
            results = []
            while True:
                print("\n--- Novo tópico ---")
                tema = input("Digite o tema do artigo (ou 'fim' para encerrar): ")
                if tema.lower() == 'fim':
                    break
                    
                categoria = input("Digite a categoria do artigo (ou Enter para usar 'Marketing Digital'): ") or "Marketing Digital"
                status_input = input("Digite o status da publicação (draft/publish) ou Enter para draft: ") or "draft"
                
                result = await process_topic(tema, categoria, status_input)
                results.append(result)
                
                if result.get('success', False):
                    print(f"\nArtigo publicado com sucesso!")
                    print(f"URL: {result.get('url', 'N/A')}")
                    print(f"Status: {status_input}")
                else:
                    print(f"\nFalha ao publicar artigo: {result.get('error', 'Erro desconhecido')}")
                
            # Mostrar resumo dos resultados
            if results:
                print("\n=== Resumo do Processamento em Lote ===")
                print(f"Total de tópicos processados: {len(results)}")
                print(f"Publicações bem-sucedidas: {sum(1 for r in results if r.get('success', False))}")
                print(f"Falhas: {sum(1 for r in results if not r.get('success', False))}")
            
            return
        
        # 4. Modo interativo simples (padrão)
        default_tema = "Transformação Digital para Empresas Tradicionais em Portugal"
        tema = input(f"Digite o tema do artigo (ou pressione Enter para usar o tema padrão): ") or default_tema
        
        categoria = input("Digite a categoria do artigo (ou pressione Enter para usar a categoria padrão): ") or "Marketing Digital"
        
        status = input("Digite o status da publicação (draft/publish) ou Enter para draft: ") or "draft"
        
        result = await process_topic(tema, categoria, status)
        
        if result.get('success', False):
            print(f"\nArtigo publicado com sucesso!")
            print(f"URL: {result.get('url', 'N/A')}")
            print(f"Status: {status}")
        else:
            print(f"\nFalha ao publicar artigo: {result.get('error', 'Erro desconhecido')}")
        
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo utilizador.")
    except Exception as e:
        logging.error(f"Erro ao executar o script: {str(e)}")
        print(f"\nErro ao executar o script: {str(e)}")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nOperação interrompida pelo utilizador.")
    except Exception as e:
        logging.error(f"Erro não tratado: {str(e)}")
        print(f"\nErro não tratado: {str(e)}")
        sys.exit(1) 