#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Exemplo de geração de artigo com publicação opcional no WordPress.

Este script demonstra como gerar um artigo utilizando o ContentGenerator e
opcionalmente publicá-lo diretamente no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import logging
import argparse
import requests
import random
import re

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.config.content_config import WP_CATEGORIES
from src.generators.content_generator import ContentGenerator
from src.integrations.dify_client import DifyClient
from src.integrations.wordpress_client import WordPressClient
from src.utils.image_generator import ImageGenerator

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se as credenciais do WordPress estão configuradas
if not all([
    os.getenv('WP_URL'),
    os.getenv('WP_USERNAME'),
    os.getenv('WP_PASSWORD')
]):
    logger.error("Credenciais do WordPress não configuradas no arquivo .env")
    sys.exit(1)

def print_available_categories():
    """Imprime as categorias disponíveis para o artigo."""
    logger.info("Categorias disponíveis para o artigo:")
    for slug, info in WP_CATEGORIES.items():
        logger.info(f"  - {info['name']} ({slug})")

def generate_featured_image(title: str, category: str) -> str:
    """
    Gera uma imagem de destaque personalizada para o artigo.
    
    Args:
        title: Título do artigo
        category: Categoria do artigo
        
    Returns:
        Caminho para a imagem gerada ou None em caso de erro
    """
    try:
        # Criar instância do gerador de imagens
        image_generator = ImageGenerator()
        
        # Gerar a imagem
        logger.info(f"Gerando imagem de destaque para: '{title}'")
        image_path = image_generator.create_featured_image(title, category)
        
        if image_path:
            logger.info(f"Imagem gerada com sucesso: {image_path}")
            return image_path
        else:
            logger.error("Falha ao gerar imagem de destaque")
            return None
            
    except Exception as e:
        logger.error(f"Erro ao gerar imagem de destaque: {str(e)}")
        return None

def sanitize_title(title: str) -> str:
    """
    Remove datas e palavras temporais do título para evitar obsolescência.
    
    Args:
        title: Título original
        
    Returns:
        Título sanitizado
    """
    import re
    
    # Preservar o título original para comparação
    original_title = title.strip()
    
    # Remover anos (2023, 2024, etc.)
    title = re.sub(r'\b20\d{2}\b', '', title)
    
    # Remover referências a "em 2023", "para 2024", etc.
    title = re.sub(r'\b(em|para|de|no|na)\s+20\d{2}\b', '', title, flags=re.IGNORECASE)
    
    # Remover palavras sobre tendências específicas do ano
    title = re.sub(r'\b(tendências|novidades|previsões|perspectivas)(\s+de|\s+para)?\s+20\d{2}\b', 'Tendências Atuais', title, flags=re.IGNORECASE)
    
    # Remover palavras sobre eventos de tempo limitado
    temporal_patterns = [
        r'\bpara este ano\b', 
        r'\bdo ano\b',
        r'\bdeste ano\b',
        r'\batuais\b',
        r'\brecentes\b'
    ]
    
    for pattern in temporal_patterns:
        title = re.sub(pattern, '', title, flags=re.IGNORECASE)
    
    # Limpar espaços extras e pontução
    title = re.sub(r'\s+', ' ', title)
    title = re.sub(r'\s+([,.!?])', r'\1', title)
    
    # Remover preposições soltas no final do título
    title = re.sub(r'\b(em|para|de|do|da|dos|das|no|na|nos|nas)\s*$', '', title, flags=re.IGNORECASE)
    
    # Garantir primeira letra maiúscula
    title = title.strip().capitalize()
    
    # Se o título ficar muito curto após as remoções, usar o original sem o ano
    if len(title) < 20:
        # Remover apenas o ano, mantendo o resto intacto
        safe_title = re.sub(r'\b20\d{2}\b', '', original_title)
        safe_title = re.sub(r'\s+', ' ', safe_title).strip()
        
        # Remover preposições soltas no final
        safe_title = re.sub(r'\b(em|para|de|do|da|dos|das|no|na|nos|nas)\s*$', '', safe_title, flags=re.IGNORECASE)
        
        if len(safe_title) >= 20:
            title = safe_title
        else:
            # Adicionar um sufixo genérico se ainda for muito curto
            title += " - Guia Completo"
    
    # Verificar se título termina corretamente
    if not re.search(r'[.!?]$', title):
        # Garantir que há um fechamento adequado do título
        title += ""
    
    return title

def suggest_tags_for_topic(topic: str, category: str) -> list:
    """
    Sugere tags relevantes para o tópico e categoria.
    
    Args:
        topic: Tópico do artigo
        category: Categoria do artigo
        
    Returns:
        Lista de tags sugeridas
    """
    # Base de tags para cada categoria
    category_tags = {
        "blog-e-commerce": ["e-commerce", "vendas online", "loja virtual", "comércio eletrónico"],
        "blog-empreendedorismo": ["empreendedorismo", "negócios", "startups", "inovação"],
        "blog-gestao-pmes": ["pme", "gestão", "pequenas empresas", "médias empresas"],
        "blog-inteligencia-artificial": ["inteligência artificial", "ia", "automação", "machine learning"],
        "blog-marketing-digital": ["marketing digital", "marketing online", "estratégia digital", "publicidade online"],
        "blog-tecnologia": ["tecnologia", "inovação tecnológica", "digital", "tendências tech"],
        "blog-transformacao-digital": ["transformação digital", "digitalização", "indústria 4.0", "inovação digital"],
        "blog-vendas": ["vendas", "estratégia comercial", "negociação", "cliente"]
    }
    
    # Tags que não devem ser usadas (palavras muito comuns ou que causam erros)
    blacklisted_tags = [
        "para", "como", "com", "dos", "das", "por", "mais", "menos", "seu", "sua", "seus", "suas",
        "este", "esta", "estes", "estas", "isso", "aquilo", "que", "qual", "quais", "quando", "onde",
        "porque", "pois", "marketing", "digital", "online", "internet", "web", "site", "blog"
    ]
    
    # Obter tags base da categoria
    tags = category_tags.get(category, [])
    
    # Extrair possíveis tags do tópico
    words = [word.lower() for word in topic.split() if len(word) > 3]
    phrases = []
    
    # Criar frases relevantes do tópico (2-3 palavras consecutivas)
    for i in range(len(words) - 1):
        phrases.append(f"{words[i]} {words[i+1]}")
        if i < len(words) - 2:
            phrases.append(f"{words[i]} {words[i+1]} {words[i+2]}")
    
    # Adicionar palavras e frases relevantes que não estão na blacklist
    for item in phrases + words:
        if item not in tags and not any(word in blacklisted_tags for word in item.split()):
            tags.append(item)
    
    # Adicionar o nome da categoria como tag
    category_name = WP_CATEGORIES.get(category, {}).get('name', '').lower()
    if category_name and category_name not in tags:
        tags.append(category_name)
    
    # Adicionar palavras-chave específicas para o tópico
    if "pequenas empresas" in topic.lower() and "pequenas empresas" not in tags:
        tags.append("pequenas empresas")
    
    # Limitar a 5 tags para melhor foco
    return tags[:5]

def generate_article(topic, category, output_dir='output', validate_content=True, publish=False):
    """
    Gera um artigo sobre o tópico especificado na categoria selecionada.
    
    Args:
        topic: Tópico do artigo
        category: Categoria para o artigo
        output_dir: Diretório para salvar o artigo
        validate_content: Se True, valida o conteúdo antes de salvar
        publish: Se True, publica no WordPress após gerar
        
    Returns:
        Tuple com (status, link_do_artigo)
    """
    try:
        # Validar categoria
        if category not in WP_CATEGORIES:
            logger.error(f"Categoria inválida: {category}")
            logger.info("Categorias disponíveis:")
            for cat_slug, cat_info in WP_CATEGORIES.items():
                logger.info(f"  - {cat_info['name']} ({cat_slug})")
            return False, None
        
        # Inicializar o gerador de conteúdo
        logger.info(f"Gerando artigo sobre: {topic}")
        logger.info(f"Categoria: {category} ({WP_CATEGORIES[category]['name']})")
        
        # Criar instância do DifyClient usando as variáveis de ambiente
        dify_client = DifyClient()
        
        # Criar instância do ContentGenerator
        content_generator = ContentGenerator(dify_client)
        
        # Gerar o artigo
        article = content_generator.generate_article(topic, category)
        
        # Validar o artigo
        if validate_content and not article.is_valid():
            logger.error("Artigo gerado é inválido:")
            for section_name, errors in article.validation_errors.items():
                logger.error(f"  - {section_name}: {', '.join(errors)}")
            return False, None
        
        # Publicar no WordPress
        try:
            # Inicializar cliente WordPress
            wp_client = WordPressClient()
            
            # Preparar título limpo
            clean_title = sanitize_title(article.title)
            logger.info(f"Título sanitizado: '{clean_title}'")
            
            # Gerar HTML do artigo
            html_content = article.to_html()
            
            # Processar o HTML antes de publicar
            html_content = process_html_content(html_content, clean_title)
            
            # Gerar imagem de destaque personalizada
            featured_image_path = generate_featured_image(clean_title, category)
            
            # Se falhar em gerar a imagem, tentar usar imagens locais como fallback
            if not featured_image_path:
                logger.warning("Usando imagens locais como fallback")
                local_images = [
                    os.path.join('assets', 'images', f'{category}.jpg'),
                    os.path.join('assets', 'images', f'{category}.png'),
                    os.path.join('assets', 'images', 'default.jpg')
                ]
                
                # Se houver uma imagem no .env, usar como fallback
                env_image = os.getenv('WP_FEATURED_IMAGE_PATH')
                if env_image and os.path.exists(env_image):
                    featured_image_path = env_image
                    logger.info(f"Usando imagem de destaque do .env: {env_image}")
                else:
                    # Procurar imagens locais
                    for img_path in local_images:
                        if os.path.exists(img_path):
                            featured_image_path = img_path
                            logger.info(f"Usando imagem local: {img_path}")
                            break
            
            # Gerar tags relevantes
            tags = suggest_tags_for_topic(topic, category)
            logger.info(f"Tags sugeridas: {tags}")
            
            # Publicar o artigo
            result = wp_client.publish_article_from_html(
                html_content=html_content,
                category_slug=category,
                featured_image_path=featured_image_path,
                title=clean_title,
                tags=tags,
                auto_tags=True,
                status=os.getenv('WP_POST_STATUS', 'draft')
            )
            
            if result:
                logger.info(f"Artigo publicado com sucesso: {result.get('link')}")
                return True, result.get('link')
            else:
                logger.error("Falha ao publicar o artigo no WordPress")
                return False, None
                
        except Exception as e:
            logger.error(f"Erro ao publicar artigo: {str(e)}")
            import traceback
            traceback.print_exc()
            return False, None
    
    except Exception as e:
        logger.error(f"Erro ao gerar artigo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False, None

def process_html_content(html_content: str, title: str) -> str:
    """
    Processa o conteúdo HTML antes da publicação.
    
    Args:
        html_content: Conteúdo HTML original
        title: Título do artigo
        
    Returns:
        Conteúdo HTML processado
    """
    # Remover tags HTML desnecessárias
    html_content = re.sub(r'<!DOCTYPE.*?>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'<html>.*?<body>', '', html_content, flags=re.DOTALL)
    html_content = re.sub(r'</body>.*?</html>', '', html_content, flags=re.DOTALL)
    
    # Remover completamente o título principal do corpo do artigo
    title_pattern = f'<h[1-6]>.*?{re.escape(title)}.*?</h[1-6]>'
    html_content = re.sub(title_pattern, '', html_content, flags=re.IGNORECASE)
    
    # Remover títulos de seção indesejados e texto de instrução
    unwanted_titles = [
        'Atenção',
        'Confiança',
        'Interesse',
        'Decisão',
        'Ação',
        'Confiança na Descomplicar',
        'Marketing Digital para Pequenas Empresas',
        'Como Implementar'
    ]
    for word in unwanted_titles:
        # Remover o título completo
        pattern = f'<h[1-6]>{word}</h[1-6]>'
        html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE)
    
    # Remover textos de instrução que podem ter vazado para o conteúdo
    instruction_patterns = [
        r'Este conteúdo estabelece a Descomplicar como uma autoridade.*?</p>',
        r'<p>Este conteúdo foi estruturado para.*?</p>',
        r'<p>Nesta seção,.*?</p>',
        r'<p>Esta seção apresenta.*?</p>',
        r'<p>Para concluir,.*?</p>'
    ]
    for pattern in instruction_patterns:
        html_content = re.sub(pattern, '', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    # Remover categoria duplicada (manter apenas a primeira ocorrência)
    category_pattern = r'<p.*?>\s*<em>Categoria:.*?</em>\s*</p>'
    category_matches = re.findall(category_pattern, html_content, flags=re.IGNORECASE)
    if len(category_matches) > 1:
        for match in category_matches[1:]:
            html_content = html_content.replace(match, '', 1)
    
    # Remover seções duplicadas completas
    section_pattern = r'<div class="article-section.*?>.*?</div>'
    sections = re.finditer(section_pattern, html_content, re.DOTALL)
    seen_sections = set()
    for section in sections:
        section_text = section.group(0)
        # Criar um hash simplificado do conteúdo para detectar duplicações
        section_hash = hash(re.sub(r'\s+', '', section_text.lower()[:300]))
        if section_hash in seen_sections:
            html_content = html_content.replace(section_text, '', 1)
        else:
            seen_sections.add(section_hash)
    
    # Remover parágrafos duplicados que possam ter sido gerados pelo LLM
    paragraph_pattern = r'<p>.*?</p>'
    paragraphs = re.finditer(paragraph_pattern, html_content, re.DOTALL)
    seen_paragraphs = set()
    for para in paragraphs:
        para_text = para.group(0)
        # Ignorar parágrafos que contêm links, pois não queremos remover links importantes
        if "<a href" in para_text:
            continue
        # Criar um hash do conteúdo do parágrafo para detectar duplicações
        para_hash = hash(re.sub(r'\s+', '', para_text.lower()))
        if para_hash in seen_paragraphs:
            html_content = html_content.replace(para_text, '', 1)
        else:
            seen_paragraphs.add(para_hash)
    
    # Preservar links internos e externos
    # Garantir que todos os links tenham target="_blank" para links externos
    def add_target_blank(match):
        link = match.group(0)
        if 'descomplicar.pt' not in link and 'target=' not in link:
            return link.replace('<a ', '<a target="_blank" rel="noopener noreferrer" ')
        return link
    
    html_content = re.sub(r'<a\s+href="https?://.*?".*?>', add_target_blank, html_content)
    
    # Corrigir links quebrados
    def fix_broken_links(match):
        url = match.group(1)
        text = match.group(2)
        
        # Verificar se é um link externo ou interno
        if url.startswith('http') and 'descomplicar.pt' not in url:
            return f'<a href="{url}" target="_blank" rel="noopener noreferrer">{text}</a>'
        else:
            return f'<a href="{url}">{text}</a>'
    
    html_content = re.sub(r'<a href="(.*?)">(.*?)</a>', fix_broken_links, html_content)
    
    # Garantir que a seção de FAQ tenha o formato correto para o Yoast
    faq_section_pattern = r'<div class="faq-section">(.*?)</div>'
    faq_match = re.search(faq_section_pattern, html_content, re.DOTALL)
    if faq_match:
        faq_content = faq_match.group(1)
        
        # Garantir que o título FAQ é formatado corretamente
        faq_content = re.sub(r'<h[2-6][^>]*>.*?Perguntas\s+Frequentes.*?</h[2-6]>', '<h2>Perguntas Frequentes</h2>', faq_content, flags=re.IGNORECASE)
        
        # Adicionar schema-faq-code class para o Yoast FAQ Schema
        updated_faq = f'<div class="faq-section schema-faq-code">{faq_content}</div>'
        html_content = html_content.replace(faq_match.group(0), updated_faq)
        
        # Garantir que cada pergunta/resposta está no formato correto
        html_content = re.sub(r'<h3([^>]*)>(.*?)</h3>\s*<p>(.*?)</p>', 
                             r'<div class="schema-faq-section">\n<strong class="schema-faq-question">\2</strong>\n<p class="schema-faq-answer">\3</p>\n</div>', 
                             html_content, flags=re.DOTALL)
    
    # Garantir que parágrafos estejam corretamente formatados
    html_content = re.sub(r'<p>\s*</p>', '', html_content)
    html_content = re.sub(r'<p>(\s*<br\s*/>\s*)*</p>', '', html_content)
    
    # Manter apenas um nível de cabeçalho h2 (converter h1, h3-h6 para h2 ou h3)
    def normalize_headings(match):
        tag = match.group(1)
        content = match.group(2)
        # Verificar se o conteúdo do cabeçalho não é um dos títulos indesejados
        if any(word.lower() in content.lower() for word in unwanted_titles):
            return ''  # Remover completamente
        if tag == '1':  # h1 não deve existir no corpo
            return f'<h2>{content}</h2>'
        elif tag in ['2', '3']:  # h2 e h3 são mantidos
            return match.group(0)
        else:  # h4, h5, h6 viram h3
            return f'<h3>{content}</h3>'
    
    html_content = re.sub(r'<h([1-6])>(.*?)</h\1>', normalize_headings, html_content)
    
    # Limpar espaços extras e quebras de linha
    html_content = re.sub(r'\s+', ' ', html_content)
    html_content = re.sub(r'>\s+<', '><', html_content)
    
    # Adicionar quebras de linha para melhor legibilidade
    html_content = re.sub(r'</div><div', '</div>\n<div', html_content)
    html_content = re.sub(r'</h([1-6])><', r'</h\1>\n<', html_content)
    html_content = re.sub(r'</p><', '</p>\n<', html_content)
    
    # Limpar títulos repetitivos de FAQ
    html_content = re.sub(r'<h[2-3]>Perguntas Frequentes</h[2-3]>.*?<h[2-3]>Perguntas Frequentes</h[2-3]>', 
                          '<h2>Perguntas Frequentes</h2>', html_content, flags=re.IGNORECASE | re.DOTALL)
    
    return html_content.strip()

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Listar categorias disponíveis
    print_available_categories()
    
    # Configurações padrão para o artigo
    DEFAULT_TOPIC = "Inteligência Artificial para Pequenas e Médias Empresas"
    DEFAULT_CATEGORY = "blog-inteligencia-artificial"
    
    # Verificar argumentos da linha de comando
    parser = argparse.ArgumentParser(description='Gerar um artigo para WordPress')
    parser.add_argument('--topic', default=DEFAULT_TOPIC, help='Tópico do artigo')
    parser.add_argument('--category', default=DEFAULT_CATEGORY, help='Categoria do artigo')
    parser.add_argument('--publish', action='store_true', help='Publicar no WordPress após gerar')
    
    args = parser.parse_args()
    
    # Gerar e publicar o artigo
    success, article_link = generate_article(
        topic=args.topic,
        category=args.category,
        publish=True  # Sempre publicar
    )
    
    if success and article_link:
        logger.info(f"Artigo publicado com sucesso: {article_link}")
    
    # Sair com código apropriado
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 