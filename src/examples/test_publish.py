#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Teste de publicação com conteúdo estático.

Este script gera um artigo com conteúdo estático (sem chamar APIs externas)
e o publica no WordPress para testar o fluxo de publicação.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import logging
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Adicionar o diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.config.content_config import WP_CATEGORIES
from src.generators.content_generator import Article

# Importar o cliente WordPress
try:
    from src.integrations.wordpress_client import WordPressClient
except ImportError as e:
    logger.error(f"Erro ao importar WordPressClient: {e}")
    sys.exit(1)

def create_dummy_article(title="Transformação Digital para PMEs em 2024", 
                        category="blog-transformacao-digital") -> Article:
    """
    Cria um artigo com conteúdo estático para teste.
    
    Args:
        title: Título do artigo
        category: Categoria do artigo
        
    Returns:
        Artigo com conteúdo estático
    """
    logger.info(f"Criando artigo dummy: {title}")
    
    # Verificar categoria
    if category not in WP_CATEGORIES:
        logger.error(f"Categoria '{category}' não encontrada. Usando fallback 'blog-transformacao-digital'")
        category = "blog-transformacao-digital"
    
    # Criar seções de conteúdo
    sections = {
        "attention": """
        <p>As pequenas e médias empresas (PMEs) portuguesas enfrentam um desafio sem precedentes em 2024: adaptar-se rapidamente à transformação digital ou arriscar perder competitividade num mercado cada vez mais tecnológico. Segundo dados recentes da ACEPI, apenas 46% das PMEs em Portugal têm uma estratégia digital bem definida, apesar de 78% dos consumidores portugueses preferirem interagir com empresas que oferecem soluções digitais integradas.</p>
        <p>Esta disparidade representa tanto um risco significativo como uma oportunidade extraordinária. Enquanto gigantes tecnológicos e startups disruptivas redefinem as expectativas dos clientes, muitas PMEs tradicionais questionam: Como podemos implementar a transformação digital de forma eficaz com recursos limitados? Que tecnologias devemos priorizar? E qual é o verdadeiro retorno deste investimento?</p>
        <p>A Comissão Europeia estima que as empresas que implementam estratégias digitais adequadas aumentam a sua produtividade em até 20% e reduzem custos operacionais em 15-30%. No entanto, o caminho para a transformação digital não é igual para todas as organizações, especialmente para PMEs com orçamentos restritos e equipas reduzidas.</p>
        """,
        
        "confidence": """
        <p>Para compreender verdadeiramente o impacto da transformação digital nas PMEs portuguesas, é essencial analisar casos concretos e dados específicos do nosso mercado. De acordo com o estudo "Economia Digital em Portugal" da IDC Portugal, as PMEs que investiram em tecnologias digitais registaram um aumento médio de 18% no volume de negócios, mesmo durante períodos de instabilidade económica.</p>
        <p>A Magnitonline, uma PME de Aveiro especializada em mobiliário, é um exemplo notável. Após implementar uma estratégia de transformação digital abrangente em 2022, a empresa reportou um aumento de 35% nas vendas online e uma redução de 22% nos custos de aquisição de clientes. "A nossa transição para o digital não foi apenas sobre tecnologia, mas sobre repensar todo o nosso modelo de negócio", explica João Martins, CEO da empresa.</p>
        <p>O Instituto Superior Técnico, em colaboração com a COTEC Portugal, analisou mais de 200 PMEs nacionais que implementaram iniciativas de transformação digital nos últimos dois anos. Os resultados são esclarecedores:</p>
        <ul>
            <li>87% relataram melhorias significativas na experiência do cliente</li>
            <li>73% conseguiram reduzir os seus custos operacionais</li>
            <li>62% identificaram novas oportunidades de negócio através das tecnologias digitais</li>
            <li>91% consideram que a transformação digital foi essencial para manterem a sua competitividade</li>
        </ul>
        <p>Paulo Nunes, especialista em transformação digital do IAPMEI, afirma: "As PMEs portuguesas estão a perceber que a digitalização não é uma opção, mas uma necessidade urgente. A boa notícia é que, com a abordagem certa, mesmo empresas com recursos limitados podem implementar mudanças impactantes."</p>
        <p>Vale destacar também o caso da Farmácia Silva, uma pequena farmácia familiar em Lisboa que, através da implementação de um sistema integrado de gestão de inventário e uma presença digital estratégica, conseguiu expandir a sua base de clientes em 40% e reduzir o desperdício de produtos em 25% em apenas um ano.</p>
        """,
        
        "interest": """
        <p>A implementação estratégica da transformação digital oferece às PMEs portuguesas benefícios tangíveis e mensuráveis que vão muito além da simples adoção de novas tecnologias. Vamos explorar os impactos práticos em diferentes áreas do negócio:</p>
        
        <h3>1. Eficiência Operacional e Redução de Custos</h3>
        <p>As ferramentas digitais permitem automatizar processos manuais repetitivos, reduzindo erros e libertando recursos humanos para tarefas de maior valor acrescentado. A Metalúrgica Progresso, uma PME do Porto, implementou um sistema ERP personalizado que reduziu o tempo de processamento de encomendas em 68% e diminuiu os erros administrativos em 83%.</p>
        <p>De acordo com o INE, as PMEs portuguesas que automatizaram os seus processos financeiros e administrativos registaram uma redução média de custos operacionais de 17,5% em 2023.</p>
        
        <h3>2. Melhoria na Experiência e Fidelização do Cliente</h3>
        <p>A presença digital omnicanal permite às empresas oferecer experiências personalizadas e convenientes. A Pastelaria Tradicional, uma pequena empresa familiar em Braga, desenvolveu uma app móvel simples que permite aos clientes encomendar antecipadamente e acumular pontos de fidelidade. O resultado? Um aumento de 28% nas compras repetidas e um crescimento da receita média por cliente de 15%.</p>
        <p>Um estudo da ACEPI revelou que 72% dos consumidores portugueses estão dispostos a pagar mais por produtos/serviços de empresas que oferecem experiências digitais superiores.</p>
        
        <h3>3. Expansão de Mercado e Novos Canais de Venda</h3>
        <p>As ferramentas digitais eliminam barreiras geográficas e abrem novos mercados potenciais. A Corticeira Amorim, uma PME do setor tradicional da cortiça, expandiu as suas vendas internacionais em 47% após desenvolver uma estratégia de marketing digital direcionada e implementar uma plataforma de e-commerce B2B.</p>
        <p>De acordo com dados da Comissão Europeia, as PMEs portuguesas que vendem online para outros países da UE têm uma taxa de crescimento 22% superior às que operam apenas no mercado nacional.</p>
        
        <h3>4. Tomada de Decisão Baseada em Dados</h3>
        <p>As tecnologias de análise de dados permitem decisões mais informadas e estratégicas. A Quinta do Vallado, produtora vinícola do Douro, implementou sensores IoT nos seus vinhedos e sistemas de análise de dados que permitiram otimizar o uso de recursos hídricos (redução de 30%) e aumentar a qualidade da produção (crescimento de 18% no preço médio de venda).</p>
        <p>Um relatório do IDC Portugal indica que as PMEs que utilizam análise de dados para as suas decisões estratégicas têm uma probabilidade 23% maior de superar os seus objetivos financeiros anuais.</p>
        """,
        
        "pre_cta": "\n".join([f"<li>{service}</li>" for service in WP_CATEGORIES.get(category, {}).get('services', [])]),
        
        "decision": """
        <p>Implementar a transformação digital na sua PME não precisa de ser um processo avassalador ou excessivamente dispendioso. Apresentamos um roteiro prático e progressivo, especialmente adaptado à realidade das pequenas e médias empresas portuguesas:</p>
        
        <h3>1. Avaliação e Diagnóstico Digital</h3>
        <p>Antes de investir em qualquer tecnologia, é fundamental compreender o seu ponto de partida:</p>
        <ul>
            <li>Realize uma auditoria digital para identificar lacunas e oportunidades</li>
            <li>Avalie a maturidade digital da sua equipa</li>
            <li>Identifique os processos prioritários para digitalização</li>
            <li>Analise os recursos tecnológicos existentes que podem ser otimizados</li>
        </ul>
        <p>Ferramentas como o Índice de Maturidade Digital do IAPMEI ou a autoavaliação digital da COTEC Portugal podem ajudar neste diagnóstico inicial.</p>
        
        <h3>2. Desenvolvimento de uma Estratégia Digital Alinhada com o Negócio</h3>
        <p>Defina objetivos claros e mensuráveis para a sua transformação digital:</p>
        <ul>
            <li>Estabeleça KPIs específicos para cada iniciativa digital</li>
            <li>Crie um roadmap faseado com marcos alcançáveis</li>
            <li>Priorize iniciativas com base no potencial ROI e complexidade de implementação</li>
            <li>Aloque um orçamento realista para cada fase</li>
        </ul>
        <p>A estratégia deve considerar os apoios disponíveis no PRR e Portugal 2030 para a digitalização das PMEs, que podem financiar até 75% dos investimentos elegíveis.</p>
        
        <h3>3. Implementação Progressiva de Soluções Digitais</h3>
        <p>Comece por implementar soluções de alto impacto e baixa complexidade:</p>
        <ul>
            <li>Sistema de CRM para gestão de relacionamento com clientes</li>
            <li>Ferramentas de marketing digital e presença online otimizada</li>
            <li>Automação de processos administrativos e financeiros</li>
            <li>Sistemas de colaboração e trabalho remoto</li>
            <li>Análise de dados para decisões informadas</li>
        </ul>
        <p>Plataformas como o Microsoft 365 Business, Salesforce Essentials ou Zoho One oferecem soluções escaláveis e acessíveis para PMEs.</p>
        
        <h3>4. Capacitação e Gestão da Mudança</h3>
        <p>O sucesso da transformação digital depende fundamentalmente das pessoas:</p>
        <ul>
            <li>Desenvolva um plano de formação digital para toda a equipa</li>
            <li>Identifique e prepare "campeões digitais" internos</li>
            <li>Comunique claramente os benefícios e objetivos das mudanças</li>
            <li>Incentive a experimentação e aprendizagem contínua</li>
        </ul>
        <p>Programas como o Emprego + Digital ou as formações do IEFP oferecem recursos formativos subsidiados para PMEs.</p>
        """,
        
        "action": """
        <p>A transformação digital não é um destino, mas uma jornada contínua que permite às PMEs portuguesas competir e prosperar num mundo cada vez mais tecnológico. Como vimos ao longo deste artigo, os benefícios são tangíveis e mensuráveis, desde a redução de custos até à conquista de novos mercados.</p>
        
        <p>Para dar os primeiros passos nesta jornada, recomendamos três ações imediatas:</p>
        
        <ol>
            <li><strong>Realize o diagnóstico digital da sua empresa</strong> para identificar pontos fortes e oportunidades de melhoria.</li>
            <li><strong>Identifique um processo específico</strong> que, se digitalizado, traria benefícios rápidos e visíveis para o seu negócio.</li>
            <li><strong>Invista na capacitação digital</strong> da sua equipa, o ativo mais valioso na sua jornada de transformação.</li>
        </ol>
        
        <p>A Descomplicar está pronta para apoiar a sua empresa em cada etapa deste processo, oferecendo soluções personalizadas que respeitam o seu orçamento e as especificidades do seu negócio.</p>
        
        <p>Não deixe o futuro da sua empresa para amanhã. A transformação digital não é uma opção, mas uma necessidade para garantir a relevância e competitividade no mercado atual.</p>
        
        <p><strong>Contacte-nos hoje</strong> para uma consulta gratuita e descubra como podemos ajudar a sua PME a prosperar na era digital.</p>
        """
    }
    
    # Criar o artigo
    article = Article(
        title=title,
        category=category,
        sections=sections
    )
    
    # Validar o artigo
    article.validate()
    
    return article

def save_article_to_file(article: Article, output_dir: str = "output") -> str:
    """
    Salva o artigo em arquivo HTML.
    
    Args:
        article: Instância do artigo a ser salvo
        output_dir: Diretório de saída
        
    Returns:
        Caminho do arquivo salvo
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Criar nome do arquivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    sanitized_title = article.title.lower().replace(' ', '-').replace('/', '-')
    output_file = os.path.join(
        output_dir, 
        f"{article.category}_{sanitized_title}_{timestamp}.html"
    )
    
    # Salvar o HTML
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(article.to_html())
    
    logger.info(f"Artigo salvo em: {output_file}")
    return output_file

def publish_article_to_wordpress(article: Article, html_file: str) -> bool:
    """
    Publica o artigo no WordPress.
    
    Args:
        article: Instância do artigo a ser publicado
        html_file: Caminho do arquivo HTML
        
    Returns:
        True se o artigo foi publicado com sucesso
    """
    logger.info(f"Publicando artigo no WordPress: {article.title}")
    
    try:
        # Inicializar cliente WordPress
        wp_client = WordPressClient()
        
        # Ler o conteúdo HTML
        with open(html_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Publicar o artigo
        result = wp_client.publish_article_from_html(
            html_content=html_content,
            category_slug=article.category,
            featured_image_path=os.getenv('WP_FEATURED_IMAGE_PATH'),
            title=article.title
        )
        
        if result:
            logger.info(f"Artigo publicado com sucesso: {result.get('link')}")
            return True
        else:
            logger.error("Falha ao publicar o artigo")
            return False
            
    except Exception as e:
        logger.error(f"Erro ao publicar artigo: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Função principal"""
    # Carregar variáveis de ambiente
    load_dotenv()
    
    # Criar um artigo dummy
    try:
        article = create_dummy_article()
        
        # Salvar o artigo
        html_file = save_article_to_file(article)
        
        # Publicar o artigo
        if publish_article_to_wordpress(article, html_file):
            logger.info("Processo completo executado com sucesso!")
            sys.exit(0)
        else:
            logger.error("Falha na publicação do artigo")
            sys.exit(1)
    
    except Exception as e:
        logger.error(f"Erro no processo: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main() 