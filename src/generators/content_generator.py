#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de conteúdo para artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import time
import logging
import re
import random
from typing import Dict, List, Optional, Tuple

from src.config.content_config import (METRICS, QUALITY_METRICS, 
                                      SECTION_REQUIREMENTS, WP_CATEGORIES)
from src.integrations.dify_client import DifyClient

# Configuração do logging
logger = logging.getLogger(__name__)

# Padrões de título
TITLE_PATTERNS = [
    "Como {tema}: {subtitulo}",
    "{tema} para Empresas: {subtitulo}",
    "{tema}: {subtitulo}",
    "Guia de {tema}: {subtitulo}",
    "{tema} na Prática: {subtitulo}",
    "Estratégias de {tema}: {subtitulo}",
    "Tudo sobre {tema}: {subtitulo}",
    "{tema} para PMEs: {subtitulo}",
    "Manual de {tema}: {subtitulo}",
    "{tema} em Portugal: {subtitulo}"
]

# Padrões de subtítulo
SUBTITLE_PATTERNS = [
    "Guia Completo",
    "Tudo o que Precisa de Saber",
    "Estratégias Práticas",
    "Dicas e Boas Práticas",
    "O Guia Definitivo",
    "Passo a Passo",
    "Melhores Práticas",
    "Como Implementar",
    "Guia para Iniciantes",
    "Estratégias Avançadas"
]

class ContentGenerator:
    """Gerador de conteúdo para artigos."""
    
    def __init__(self, dify_client: DifyClient, knowledge_base_id: str = None):
        """Inicializa o gerador de conteúdo.
        
        Args:
            dify_client: Instância do cliente Dify
            knowledge_base_id: ID da base de conhecimento (se None, usa o valor do cliente Dify)
        """
        self.dify_client = dify_client
        self.knowledge_base_id = knowledge_base_id or dify_client.knowledge_base_id
        
        # Inicializar mapeamento de links internos
        self.internal_links = self._initialize_internal_links()
        
        logger.info(f"ContentGenerator inicializado com knowledge_base_id: {self.knowledge_base_id}")
    
    def _initialize_internal_links(self) -> Dict[str, List[Dict[str, str]]]:
        """
        Inicializa o mapeamento de links internos organizados por categoria.
        Cada link contém URL, título e uma breve descrição para incorporação natural.
        
        Returns:
            Dicionário com links internos por categoria
        """
        links = {
            # Links gerais relevantes para todas as categorias
            "general": [
                {
                    "url": "https://descomplicar.pt/transforme-o-seu-negocio-com-o-poder-do-marketing-digital/",
                    "title": "Transforme o seu negócio com o Poder do Marketing Digital",
                    "context": "transformação digital e crescimento de negócios",
                    "description": "artigo sobre como potencializar resultados através do marketing digital"
                },
                {
                    "url": "https://descomplicar.pt/optimizar-a-presenca-online-do-seu-negocio/",
                    "title": "Otimizar a Presença Online do Seu Negócio",
                    "context": "melhorar visibilidade e resultados online",
                    "description": "estratégias para otimização de presença digital"
                },
                {
                    "url": "https://descomplicar.pt/como-produzir-mais-resultados-com-menos-esforco/",
                    "title": "Como produzir mais resultados com menos esforço",
                    "context": "produtividade e eficiência",
                    "description": "métodos para aumentar produtividade e resultados"
                }
            ],
            
            # Links específicos para e-commerce
            "blog-e-commerce": [
                {
                    "url": "https://descomplicar.pt/e-commerce/",
                    "title": "Soluções de E-Commerce Descomplicar",
                    "context": "lojas online e vendas pela internet",
                    "description": "plataforma completa para vender produtos online"
                },
                {
                    "url": "https://descomplicar.pt/alavancar-vendas-com-e-mail-marketing/",
                    "title": "Alavancar Vendas com E-mail Marketing",
                    "context": "estratégias de email para e-commerce",
                    "description": "técnicas eficazes de email marketing para aumentar vendas"
                },
                {
                    "url": "https://descomplicar.pt/acceleratorx/",
                    "title": "AcceleratorX",
                    "context": "automação e otimização de lojas online",
                    "description": "ferramentas inteligentes para impulsionar o sucesso do seu e-commerce"
                }
            ],
            
            # Links específicos para empreendedorismo
            "blog-empreendedorismo": [
                {
                    "url": "https://descomplicar.pt/starter/",
                    "title": "Plano Starter",
                    "context": "iniciar um negócio digital",
                    "description": "solução inicial ideal para empreendedores que estão começando"
                },
                {
                    "url": "https://descomplicar.pt/pedido-de-orcamento/",
                    "title": "Consultoria Personalizada",
                    "context": "orientação especializada para empreendedores",
                    "description": "consultoria estratégica para novos negócios"
                },
                {
                    "url": "https://descomplicar.pt/anuncios-e-gestao-de-trafego/",
                    "title": "Anúncios e Gestão de Tráfego",
                    "context": "atrair clientes para novos negócios",
                    "description": "estratégias de aquisição de clientes para startups e novos empreendimentos"
                }
            ],
            
            # Links específicos para gestão de PMEs
            "blog-gestao-pmes": [
                {
                    "url": "https://descomplicar.pt/corporate/",
                    "title": "Plano Corporate",
                    "context": "soluções empresariais integradas",
                    "description": "plataforma completa para empresas estabelecidas"
                },
                {
                    "url": "https://descomplicar.pt/care-descomplicar/",
                    "title": "Care Descomplicar",
                    "context": "suporte e manutenção contínua",
                    "description": "serviço de suporte técnico e monitorização para garantir estabilidade"
                },
                {
                    "url": "https://descomplicar.pt/blog/",
                    "title": "Descomplicar 360º",
                    "context": "gestão integrada de presença digital",
                    "description": "solução completa para gestão digital de PMEs"
                }
            ],
            
            # Links específicos para inteligência artificial
            "blog-inteligencia-artificial": [
                {
                    "url": "https://descomplicar.pt/tecnologia/",
                    "title": "Soluções Tecnológicas Descomplicar",
                    "context": "inovação tecnológica e IA",
                    "description": "implementação de inteligência artificial nos negócios"
                },
                {
                    "url": "https://descomplicar.pt/challenge/",
                    "title": "Challenge",
                    "context": "projetos complexos de tecnologia",
                    "description": "programa para desafios tecnológicos avançados"
                },
                {
                    "url": "https://descomplicar.pt/o-papel-do-conteudo-visual-na-era-da-atencao-limitada/",
                    "title": "O Papel do Conteúdo Visual na Era da Atenção Limitada",
                    "context": "otimização de conteúdo com IA",
                    "description": "estratégias de conteúdo visual aprimoradas por tecnologia"
                }
            ],
            
            # Links específicos para marketing digital
            "blog-marketing-digital": [
                {
                    "url": "https://descomplicar.pt/marketing/",
                    "title": "Marketing Digital Descomplicar",
                    "context": "estratégias de marketing digital",
                    "description": "serviços completos de marketing digital para empresas"
                },
                {
                    "url": "https://descomplicar.pt/anuncios-e-gestao-de-trafego/",
                    "title": "Anúncios e Gestão de Tráfego",
                    "context": "campanhas de anúncios online",
                    "description": "estratégias de publicidade online para atrair clientes qualificados"
                },
                {
                    "url": "https://descomplicar.pt/websites-poderosos/",
                    "title": "Websites Poderosos",
                    "context": "plataformas web otimizadas para conversão",
                    "description": "sites profissionais que convertem visitantes em clientes"
                }
            ],
            
            # Links específicos para tecnologia
            "blog-tecnologia": [
                {
                    "url": "https://descomplicar.pt/tecnologia/",
                    "title": "Soluções Tecnológicas Descomplicar",
                    "context": "implementação tecnológica para empresas",
                    "description": "tecnologia avançada para impulsionar negócios"
                },
                {
                    "url": "https://descomplicar.pt/websites-poderosos/",
                    "title": "Websites Poderosos",
                    "context": "plataformas web avançadas",
                    "description": "sites multifuncionais com tecnologia de ponta"
                },
                {
                    "url": "https://descomplicar.pt/acceleratorx/",
                    "title": "AcceleratorX",
                    "context": "automação e otimização tecnológica",
                    "description": "conjunto de ferramentas tecnológicas para automação de negócios"
                }
            ],
            
            # Links específicos para transformação digital
            "blog-transformacao-digital": [
                {
                    "url": "https://descomplicar.pt/challenge/",
                    "title": "Challenge",
                    "context": "projetos complexos de transformação",
                    "description": "programa para transformação digital completa"
                },
                {
                    "url": "https://descomplicar.pt/corporate/",
                    "title": "Plano Corporate",
                    "context": "digitalização de empresas estabelecidas",
                    "description": "solução digital integrada para empresas em transformação"
                },
                {
                    "url": "https://descomplicar.pt/care-descomplicar/",
                    "title": "Care Descomplicar",
                    "context": "suporte na jornada de transformação digital",
                    "description": "acompanhamento contínuo durante o processo de digitalização"
                }
            ],
            
            # Links específicos para vendas
            "blog-vendas": [
                {
                    "url": "https://descomplicar.pt/alavancar-vendas-com-e-mail-marketing/",
                    "title": "Alavancar Vendas com E-mail Marketing",
                    "context": "estratégias de email para aumentar vendas",
                    "description": "técnicas de email marketing que impulsionam resultados comerciais"
                },
                {
                    "url": "https://descomplicar.pt/e-commerce/",
                    "title": "Soluções de E-Commerce",
                    "context": "plataformas de vendas online",
                    "description": "lojas virtuais otimizadas para maximizar conversões"
                },
                {
                    "url": "https://descomplicar.pt/anuncios-e-gestao-de-trafego/",
                    "title": "Anúncios e Gestão de Tráfego",
                    "context": "atração de clientes qualificados",
                    "description": "estratégias de aquisição de clientes através de anúncios online"
                }
            ]
        }
        
        return links
        
    def _get_relevant_links(self, section: str, topic: str, category: str) -> List[Dict[str, str]]:
        """
        Seleciona links internos relevantes para a seção e categoria específicas.
        
        Args:
            section: Seção do artigo (attention, confidence, interest, decision, action, faq)
            topic: Tópico do artigo
            category: Categoria do artigo
            
        Returns:
            Lista de links relevantes para incluir na seção
        """
        # Define quantos links incluir por seção
        links_per_section = {
            "attention": 0,  # Não incluir links na introdução
            "confidence": 1, # 1 link na seção de confiança
            "interest": 2,   # 2 links na seção principal
            "decision": 1,   # 1 link na seção de decisão
            "action": 0,     # Não incluir links na CTA final
            "faq": 1         # 1 link na seção de FAQ
        }
        
        # Obter links específicos da categoria
        category_links = self.internal_links.get(category, [])
        
        # Combinar com links gerais
        general_links = self.internal_links.get("general", [])
        
        # Priorizar links da categoria, complementar com gerais se necessário
        available_links = category_links + general_links
        
        # Determinar quantos links incluir
        num_links = links_per_section.get(section, 0)
        
        # Retornar uma seleção aleatória dos links disponíveis
        if num_links > 0 and available_links:
            return random.sample(available_links, min(num_links, len(available_links)))
        
        return []
    
    def format_title(self, topic: str) -> str:
        """
        Formata o título para seguir um padrão fixo.
        
        Args:
            topic: Tópico do artigo
            
        Returns:
            Título formatado
        """
        logger.info(f"Formatando título para o tópico: '{topic}'")
        
        # Extrair o tema principal e o subtítulo se houver
        if ":" in topic:
            main_topic, subtitle = topic.split(":", 1)
            main_topic = main_topic.strip()
            subtitle = subtitle.strip()
        else:
            main_topic = topic
            subtitle = ""
        
        # Normalizar o tema principal
        main_topic = main_topic.strip()
        
        # Lista de palavras-chave a serem verificadas por redundâncias
        keywords = ["para empresas", "para pequenas empresas", "para pmes", "para negócios"]
        
        # Evitar redundâncias nos padrões
        selected_patterns = list(TITLE_PATTERNS)
        
        for keyword in keywords:
            if keyword.lower() in main_topic.lower():
                # Se o tema já contém "para empresas" ou similar, remova padrões que adicionariam redundância
                selected_patterns = [p for p in selected_patterns if "para Empresas" not in p and "para PMEs" not in p]
                break
        
        # Se não houver padrões restantes, use os padrões sem "para Empresas"
        if not selected_patterns:
            selected_patterns = [
                "Como {tema}: {subtitulo}",
                "{tema}: {subtitulo}",
                "Guia de {tema}: {subtitulo}",
                "{tema} na Prática: {subtitulo}",
                "Estratégias de {tema}: {subtitulo}",
                "Tudo sobre {tema}: {subtitulo}",
                "Manual de {tema}: {subtitulo}",
                "{tema} em Portugal: {subtitulo}"
            ]
        
        # Escolher um padrão aleatório
        title_pattern = random.choice(selected_patterns)
        
        # Se não temos subtítulo, criar um baseado no padrão escolhido
        if not subtitle:
            if "Como" in title_pattern:
                subtitle = "Guia Completo"
            elif "Guia" in title_pattern:
                subtitle = "O que Precisa de Saber"
            elif "Manual" in title_pattern:
                subtitle = "Estratégias Práticas"
            elif "Tudo sobre" in title_pattern:
                subtitle = "O que Deve Conhecer"
            elif "Estratégias" in title_pattern:
                subtitle = "Como Implementar Eficazmente"
            else:
                subtitle = "O Essencial para o Sucesso"
        
        # Formatar o título
        formatted_title = title_pattern.format(
            tema=main_topic,
            subtitulo=subtitle
        )
        
        # Verificar e corrigir redundâncias no título formatado
        for phrase in ["para Empresas para Empresas", "para PMEs para PMEs", "para empresas para empresas"]:
            if phrase.lower() in formatted_title.lower():
                formatted_title = formatted_title.replace(phrase, phrase.split()[0] + " " + phrase.split()[1])
        
        return formatted_title
    
    def generate_article(self, topic: str, category: str) -> "Article":
        """Gera um artigo completo.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo (deve estar em WP_CATEGORIES)
            
        Returns:
            Instância de Article com o conteúdo gerado
            
        Raises:
            ValueError: Se a categoria não for válida
        """
        logger.info(f"Gerando artigo: '{topic}' na categoria '{category}'")
        
        if category not in WP_CATEGORIES:
            logger.error(f"Categoria '{category}' não encontrada. Categorias disponíveis: {list(WP_CATEGORIES.keys())}")
            raise ValueError(f"Categoria '{category}' não encontrada. Categorias disponíveis: {list(WP_CATEGORIES.keys())}")
        
        # Formatar o título no padrão correto
        formatted_topic = self.format_title(topic)
        logger.info(f"Título formatado: '{formatted_topic}'")
        
        # Buscar conteúdo similar
        logger.info(f"Buscando conteúdo similar para o tópico: '{formatted_topic}'")
        similar_content = self.dify_client.get_similar_content(
            query=formatted_topic,
            knowledge_base_id=self.knowledge_base_id
        )
        logger.info(f"Conteúdo similar encontrado")
        
        # Gerar seções
        logger.info(f"Gerando seções do artigo...")
        article_dict = {}
        
        try:
            # Criar pré-CTA (serviços)
            article_dict["pre_cta"] = self._generate_pre_cta(formatted_topic, category)
            
            # Gerar cada seção do modelo ACIDA
            article_dict["attention"] = self._generate_attention(formatted_topic, similar_content)
            article_dict["confidence"] = self._generate_confidence(formatted_topic, similar_content)
            article_dict["interest"] = self._generate_interest(formatted_topic, category, similar_content)
            article_dict["decision"] = self._generate_decision(formatted_topic, category, similar_content)
            article_dict["action"] = self._generate_action(formatted_topic)
            
            # Gerar FAQs
            article_dict["faq"] = self._generate_faq(formatted_topic, category, similar_content)
            
            # Criando objeto Article
            article = Article(
                title=formatted_topic,
                category=category,
                sections=article_dict
            )
            
            # Validar o artigo
            logger.info(f"Validando o artigo gerado")
            article.validate()
            
            logger.info(f"Artigo gerado com sucesso!")
            return article
            
        except Exception as e:
            logger.error(f"Erro ao gerar artigo: {str(e)}")
            raise
    
    def _generate_pre_cta(self, topic: str, category: str) -> str:
        """Gera o HTML para o pré-CTA com serviços relevantes.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo
            
        Returns:
            HTML com os serviços
        """
        logger.debug(f"_generate_pre_cta:")
        logger.debug(f"Topic: {topic}")
        logger.debug(f"Category: {category}")
        logger.debug(f"Categorias: {WP_CATEGORIES}")
        
        services = WP_CATEGORIES.get(category, {}).get('services', [])
        
        logger.debug(f"Serviços selecionados: {services}")
        
        # Gerar HTML com os serviços
        html = ""
        for service in services:
            html += f"<li>{service}</li>\n"
        
        logger.debug(f"HTML gerado: {html}")
        return html
    
    def _generate_attention(self, topic: str, similar_content: Dict) -> str:
        """Gera a seção ATTENTION do artigo.
        
        Args:
            topic: Tópico do artigo
            similar_content: Conteúdo similar para referência
            
        Returns:
            Texto da seção
        """
        prompt = self._create_section_prompt("attention", topic, similar_content=similar_content)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=200,
            max_words=300,
            temperature=0.7
        )
    
    def _generate_confidence(self, topic: str, similar_content: Dict) -> str:
        """Gera a seção CONFIDENCE do artigo.
        
        Args:
            topic: Tópico do artigo
            similar_content: Conteúdo similar para referência
            
        Returns:
            Texto da seção
        """
        prompt = self._create_section_prompt("confidence", topic, similar_content=similar_content)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=400,
            max_words=500,
            temperature=0.7
        )
    
    def _generate_interest(self, topic: str, category: str, similar_content: Dict) -> str:
        """Gera a seção INTEREST do artigo.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo
            similar_content: Conteúdo similar para referência
            
        Returns:
            Texto da seção
        """
        prompt = self._create_section_prompt("interest", topic, category, similar_content)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=500,
            max_words=600,
            temperature=0.7
        )
    
    def _generate_decision(self, topic: str, category: str, similar_content: Dict) -> str:
        """Gera a seção DECISION do artigo.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo
            similar_content: Conteúdo similar para referência
            
        Returns:
            Texto da seção
        """
        prompt = self._create_section_prompt("decision", topic, category, similar_content)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=400,
            max_words=500,
            temperature=0.7
        )
    
    def _generate_action(self, topic: str) -> str:
        """Gera a seção ACTION do artigo.
        
        Args:
            topic: Tópico do artigo
            
        Returns:
            Texto da seção
        """
        prompt = self._create_section_prompt("action", topic)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=150,
            max_words=200,
            temperature=0.7
        )
    
    def _generate_faq(self, topic: str, category: str, similar_content: Dict) -> str:
        """Gera as Perguntas Frequentes (FAQ) para o artigo.
        
        Args:
            topic: Tópico do artigo
            category: Categoria do artigo
            similar_content: Conteúdo similar para referência
            
        Returns:
            Texto HTML com as perguntas frequentes
        """
        prompt = self._create_section_prompt("faq", topic, category, similar_content)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=200,
            max_words=350,
            temperature=0.7
        )
    
    def _create_section_prompt(
        self,
        section: str,
        topic: str,
        category: str = None,
        similar_content: Dict = None
    ) -> str:
        """Cria o prompt para gerar uma seção específica do artigo.
        
        Args:
            section: Tipo de seção a ser gerada ('attention', 'confidence', 'interest', 'decision', 'action')
            topic: Tópico do artigo
            category: Categoria do artigo (opcional)
            similar_content: Conteúdo similar encontrado (opcional)
            
        Returns:
            Prompt formatado para a seção
        """
        # Obter links relevantes para esta seção
        relevant_links = self._get_relevant_links(section, topic, category)
        
        # Formatar os links como instruções para o modelo
        links_instructions = ""
        if relevant_links:
            links_instructions = "\n\nLinks específicos a incluir naturalmente no texto:\n"
            for i, link in enumerate(relevant_links, 1):
                links_instructions += f"{i}. Titulo: \"{link['title']}\"\n"
                links_instructions += f"   URL: {link['url']}\n"
                links_instructions += f"   Contexto: {link['context']}\n"
                links_instructions += f"   Exemplo de incorporação: \"Para mais informações sobre {link['context']}, recomendamos o nosso artigo <a href='{link['url']}'>{link['title']}</a>, que detalha {link['description']}.\"\n\n"
        
        # Base para todos os prompts
        base_prompt = f"""
        És um especialista em criar conteúdo de alta qualidade para blogs profissionais.
        
        A tua tarefa é criar a seção {section} para um artigo sobre "{topic}" para o blog da Descomplicar.
        
        Requisitos de estilo:
        1. Utiliza apenas Português Europeu (de Portugal) e nunca Português do Brasil.
        2. Mantém um tom profissional mas acessível.
        3. Inclui dados estatísticos atualizados e relevantes para o mercado português.
        4. Inclui exemplos específicos de empresas portuguesas sempre que possível.
        5. Evita frases feitas, clichés e linguagem excessivamente informal.
        6. Mantém um SEO natural, sem keyword stuffing, priorizando a qualidade.
        7. Utiliza listas numeradas ou marcadores para destacar pontos importantes.
        8. Cria parágrafos curtos e de fácil leitura (3-5 linhas).
        9. Utiliza subtítulos (h2 e h3) para estruturar o conteúdo.
        10. Usa linguagem afirmativa e evita o uso de condicionais sempre que possível.
        
        Requisitos de links:
        1. Inclui os links específicos mencionados no final deste prompt, incorporando-os naturalmente no texto.
        2. Utiliza o formato HTML completo: <a href="URL">texto âncora relevante</a>
        3. Para links externos (fora do domínio descomplicar.pt), adiciona target="_blank" e rel="noopener noreferrer".
        4. Não inventes links adicionais ou URLs que não foram fornecidos.
        5. Distribui os links de forma equilibrada ao longo do texto, em contextos relevantes.
        
        Fontes recomendadas para dados sobre Portugal:
        
        - Institutos e Organismos Governamentais:
          * IAPMEI - Agência para a Competitividade e Inovação (https://www.iapmei.pt)
          * Banco de Portugal (https://www.bportugal.pt)
          * INE - Instituto Nacional de Estatística (https://www.ine.pt)
          * AICEP Portugal Global (https://www.portugalglobal.pt)
          * Portugal Digital (https://portugaldigital.gov.pt)
          * Segurança Social (https://www.seg-social.pt)
          * Autoridade Tributária e Aduaneira (https://www.portaldasfinancas.gov.pt)
          * Comissão de Coordenação e Desenvolvimento Regional (CCDR)
        
        - Associações e Entidades Setoriais:
          * ACEPI - Associação da Economia Digital (https://www.acepi.pt)
          * APDC - Associação Portuguesa para o Desenvolvimento das Comunicações (https://www.apdc.pt)
          * AEP - Associação Empresarial de Portugal (https://www.aeportugal.pt)
          * ANJE - Associação Nacional de Jovens Empresários (https://www.anje.pt)
          * CCP - Confederação do Comércio e Serviços Portugal (https://www.ccp.pt)
          * ACEP - Associação Portuguesa das Agências de Publicidade (https://www.apap.pt)
          * AIP - Associação Industrial Portuguesa (https://www.aip.pt)
          * ANETIE - Associação Nacional das Empresas das Tecnologias de Informação e Eletrónica
          * APPM - Associação Portuguesa dos Profissionais de Marketing
        
        - Instituições Académicas e de Investigação:
          * NOVA IMS - Information Management School (https://www.novaims.unl.pt)
          * Universidade do Minho (https://www.uminho.pt)
          * ISCTE Business School (https://ibs.iscte-iul.pt)
          * Católica Lisbon School of Business & Economics (https://www.clsbe.lisboa.ucp.pt)
          * Porto Business School (https://www.pbs.up.pt)
          * COTEC Portugal (https://www.cotecportugal.pt)
          * LNEC - Laboratório Nacional de Engenharia Civil (https://www.lnec.pt)
        
        - Organizações Internacionais:
          * Comissão Europeia - Representação em Portugal (https://portugal.representation.ec.europa.eu)
          * OCDE - Organização para a Cooperação e Desenvolvimento Económico
          * World Economic Forum (https://www.weforum.org)
          * GEM Portugal - Global Entrepreneurship Monitor
        """
        
        # Adicionar fontes específicas da categoria
        category_sources = {
            "blog-e-commerce": """
            Dados específicos de E-commerce:
            * ACEPI - Observatório CTT/ACEPI - Economia Digital em Portugal
            * SIBS Market Report (https://www.sibsanalytics.com/)
            * Commerce Report Portugal (https://www.commercereport.pt/)
            * Eurostat - E-commerce statistics for individuals (dados para Portugal)
            * Estatísticas do e-commerce em Portugal (https://www.statista.com/markets/413/e-commerce/)
            """,
            
            "blog-empreendedorismo": """
            Dados específicos de Empreendedorismo:
            * GEM Portugal - Global Entrepreneurship Monitor Portugal
            * Startup Portugal (https://startupportugal.com/)
            * Portugal Startups (https://portugalstartups.com/)
            * Observatório do Empreendedorismo
            * PME Digital (programa do IAPMEI)
            * Web Summit (https://websummit.com/) - maior conferência de tecnologia, realizada em Lisboa
            """,
            
            "blog-gestao-pmes": """
            Dados específicos de Gestão de PMEs:
            * IAPMEI - Agência para a Competitividade e Inovação
            * Portugal 2020 e Portugal 2030 (https://portugal2030.pt/)
            * SABI - Sistema de Análise de Balanços Ibéricos (dados de empresas portuguesas)
            * AEP - Associação Empresarial de Portugal - Estudos e Estatísticas
            * Informa D&B - Barómetro Empresarial (https://biblioteca.informadb.pt/)
            * Observatório Racius - Estatísticas sobre empresas em Portugal
            """,
            
            "blog-inteligencia-artificial": """
            Dados específicos de Inteligência Artificial:
            * AI Portugal 2030 (https://www.incode2030.gov.pt/ai-portugal-2030)
            * Portugal AIR Center (https://www.air-centre.org/)
            * FCT - Fundação para a Ciência e Tecnologia - Iniciativas em IA
            * Laboratório Nacional de Inteligência Artificial
            * NOVA LINCS - Laboratório de Sistemas Informáticos da NOVA
            * INESC TEC - Instituto de Engenharia de Sistemas e Computadores
            """,
            
            "blog-marketing-digital": """
            Dados específicos de Marketing Digital:
            * Marktest - Bareme Internet e Estudos de Consumo Digital
            * Marktest Consulting - Estudos de Redes Sociais
            * Hootsuite - Digital Report Portugal
            * APAN - Associação Portuguesa de Anunciantes
            * WE ARE SOCIAL - Digital in Portugal Report
            * Google Trends Portugal (https://trends.google.pt/)
            * APPM - Associação Portuguesa dos Profissionais de Marketing
            """,
            
            "blog-tecnologia": """
            Dados específicos de Tecnologia:
            * INCoDe.2030 - Iniciativa Nacional em Competências Digitais
            * Portugal Tech League
            * TICE.PT - Polo das Tecnologias de Informação, Comunicação e Eletrónica
            * IDC Portugal - International Data Corporation
            * ANACOM - Autoridade Nacional de Comunicações
            * Jornal de Negócios - Secção de Tecnologia
            * Exame Informática - Revista e portal de tecnologia
            """,
            
            "blog-transformacao-digital": """
            Dados específicos de Transformação Digital:
            * Índice de Digitalidade da Economia e da Sociedade (IDES) - Portugal
            * Portugal Digital - Plano de Ação para a Transição Digital
            * COTEC Portugal - Barómetro de Inovação
            * Observatório para a Transformação Digital
            * IDC Portugal - Relatórios de Transformação Digital
            * Plataforma Portugal i4.0
            * ANETIE - Estudos sobre digitalização de empresas
            """,
            
            "blog-vendas": """
            Dados específicos de Vendas:
            * APED - Associação Portuguesa de Empresas de Distribuição
            * Nielsen Portugal - Estudos de Mercado
            * Kantar Worldpanel Portugal
            * APCMC - Associação Portuguesa dos Comerciantes de Materiais de Construção
            * CIP - Confederação Empresarial de Portugal - Relatórios Económicos
            * AICEP - Análises de Mercado e Estatísticas
            * Banco de Portugal - Indicadores de Conjuntura (vendas a retalho)
            """
        }
        
        # Adicionar fontes específicas da categoria ao prompt base
        if category and category in category_sources:
            base_prompt += "\n" + category_sources[category]
        
        # Prompts específicos para cada seção
        if section == "attention":
            section_prompt = f"""
            Esta é a seção de ATENÇÃO do artigo, que deverá:
            
            1. Identificar claramente o problema que as empresas portuguesas enfrentam relacionado com "{topic}".
            2. Quantificar o problema com dados estatísticos recentes e específicos de Portugal.
            3. Explicar as consequências negativas de não resolver este problema, destacando o custo de inação.
            4. Criar uma sensação de urgência, explicando por que é importante agir agora.
            5. Demonstrar compreensão da dor/frustração do leitor em relação a este tema.
            
            Formato: HTML com parágrafos (<p>). Não inclua títulos (h1, h2, h3) nesta seção.
            Estilo: Profissional, baseado em dados, focado em Portugal, sem alarmismo desnecessário.
            Tamanho: 4-5 parágrafos (250-350 palavras).
            
            Links: Inclui pelo menos 1 link externo para uma fonte de estatística relevante para o mercado português. Formata o link usando HTML: <a href="URL" target="_blank" rel="noopener noreferrer">texto âncora relevante</a>
            
            IMPORTANTE:
            1. Inclui pelo menos dois dados estatísticos relevantes e específicos do mercado português.
            2. NÃO inclua a palavra "Atenção" como título ou no início do texto.
            3. NÃO inclua meta-comentários sobre a estrutura do artigo ou o propósito desta seção.
            4. NÃO use frases como "nesta seção" ou "este artigo vai abordar".
            """
            
        elif section == "confidence":
            section_prompt = f"""
            Esta é a seção de CONFIANÇA do artigo, que deverá:
            
            1. Estabelecer a Descomplicar como autoridade no tema "{topic}", sem usar linguagem excessivamente promocional.
            2. Apresentar dados e experiência que demonstrem credibilidade (sem inventar dados falsos).
            3. Fornecer um resumo claro do que o leitor vai aprender neste artigo.
            4. Criar um "mapa do conteúdo" em formato de lista numerada, destacando os tópicos principais que serão abordados.
            5. Mencionar subtilmente como a Descomplicar já ajudou empresas semelhantes às do leitor.
            
            Formato: HTML com parágrafos (<p>) e uma lista (<ol> ou <ul>) dos tópicos que serão abordados. Não inclua títulos (h1, h2, h3) nesta seção.
            Estilo: Profissional, consultivo, educacional - como um consultor experiente falaria.
            Tamanho: 3-4 parágrafos + lista numerada com 4-6 pontos (200-300 palavras).
            
            Links: Inclui 1 link interno para um artigo relevante da Descomplicar, usando HTML: <a href="URL">texto âncora relevante</a>
            
            Inclui uma breve referência a resultados obtidos com empresas no mercado português, sem mencionar nomes específicos.
            
            IMPORTANTE: NÃO inclua frases como "Este conteúdo estabelece a Descomplicar como uma autoridade no tema" ou instruções meta sobre o objetivo da seção. Esse tipo de texto é apenas uma instrução para você, não deve aparecer no conteúdo final gerado.
            """
            
        elif section == "interest":
            section_prompt = f"""
            Esta é a seção de INTERESSE do artigo, que deverá:
            
            1. Desenvolver detalhadamente cada um dos pontos mencionados na seção de Confiança.
            2. Para cada ponto, explicar: o que é, porque é importante, como implementar, benefícios esperados.
            3. Incluir exemplos práticos relevantes para pequenas e médias empresas portuguesas.
            4. Fornecer dados estatísticos ou estudos de caso para apoiar cada ponto.
            5. Usar subtítulos (h2 ou h3) para organizar cada ponto principal.
            
            Formato: HTML com subtítulos (<h2> ou <h3>), parágrafos (<p>) e listas (<ul> ou <ol>) quando apropriado.
            Estilo: Educacional e prático, com foco em implementação e resultados tangíveis.
            Tamanho: Esta é a seção principal do artigo - 800-1000 palavras no total, com 150-200 palavras por ponto.
            
            Links: Inclui 1-2 links internos para artigos relevantes da Descomplicar e 1-2 links externos para fontes autoritativas que comprovem dados ou técnicas mencionadas.
            
            IMPORTANTE: 
            1. Utiliza exemplos concretos do mercado português, com dados atualizados. 
            2. Cada subtópico deve ensinar algo valioso e acionável, mesmo que o leitor não contrate a Descomplicar.
            3. NÃO inclua texto que explique a estrutura do artigo ou meta-comentários sobre o propósito desta seção.
            4. NÃO use "nesta seção" ou referências a seções. Escreva como se o artigo fosse um texto corrido.
            """
            
        elif section == "decision":
            section_prompt = f"""
            Esta é a seção de DECISÃO do artigo, que deverá:
            
            1. Apresentar um plano de ação claro e estruturado para implementar as estratégias discutidas no artigo.
            2. Organizar o plano em etapas sequenciais e numeradas (1, 2, 3...).
            3. Para cada etapa, explicar: o que fazer, como fazer, recursos necessários e resultados esperados.
            4. Incluir prazos realistas para cada etapa do plano.
            5. Antecipar possíveis obstáculos e como superá-los.
            
            Formato: HTML com subtítulo principal (<h2>), subtítulos para cada etapa (<h3>), e parágrafos (<p>).
            Estilo: Prático, direto, acionável - como um roteiro ou manual passo-a-passo.
            Tamanho: 400-500 palavras, distribuídas entre 4-6 etapas do plano.
            
            Links: Inclui pelo menos 1 link interno para um artigo da Descomplicar que possa ajudar a implementar alguma etapa específica do plano.
            
            IMPORTANTE: 
            1. Este plano deve ser implementável por uma PME portuguesa com recursos limitados.
            2. Cada etapa deve ser clara o suficiente para que o leitor possa começar a implementá-la imediatamente.
            3. NÃO inclua meta-comentários como "nesta seção" ou explicações sobre o propósito desta parte do artigo.
            4. NÃO inclua partes do prompt nas respostas (como "Etapa 1: O que fazer - Como fazer - Recursos necessários").
            """
            
        elif section == "action":
            section_prompt = f"""
            Esta seção encerra o artigo de forma dinâmica, com um título apelativo (NÃO uses o título "Conclusão", mas sim algo mais impactante como "O Futuro do {topic} Começa Hoje", "Como Transformar o Seu Negócio com {topic}", "O Próximo Passo para o Sucesso em {topic}" ou similar).

            Nesta seção deves:
            1. Resumir brevemente os principais pontos do artigo de forma dinâmica e orientada para a ação
            2. Enfatizar o valor estratégico de implementar as práticas discutidas
            3. Terminar com um call-to-action que encoraje os leitores a darem o próximo passo
            4. Incluir uma última frase motivadora que inspire o leitor a agir
            
            Esta seção deve ser persuasiva, inspiradora e memorável, destacando os benefícios de trabalhar com a Descomplicar como parceira para implementar as estratégias descritas no artigo.
            
            Lembra-te: Evita começar com "Em conclusão" ou usar "Conclusão" como título. Em vez disso, usa um título apelativo relacionado com o tema.
            """
            
        elif section == "faq":
            section_prompt = f"""
            Esta é a seção de PERGUNTAS FREQUENTES (FAQ) do artigo, que deverá:
            
            1. Responder de forma clara e objetiva a 4-6 perguntas frequentes sobre o tema "{topic}".
            2. Incluir perguntas que possam ser feitas por empresas, empreendedores ou profissionais do mercado.
            3. Fornecer respostas detalhadas e informativas para cada pergunta.
            4. Usar um formato organizado e fácil de entender.
            5. Incluir exemplos práticos e casos reais para ilustrar as respostas.
            
            Formato: HTML com perguntas em formato <h3> (não usar <h4> ou maior) e respostas em <p>.
            Estilo: Profissional, educacional e informativo, com foco em resolver dúvidas e fornecer informações precisas.
            Tamanho: 200-350 palavras no total, com respostas objetivas mas completas para cada pergunta.
            
            Links: Inclui pelo menos 1 link externo para uma fonte autoritativa que responda a uma das perguntas com mais profundidade.
            
            IMPORTANTE: 
            1. Cada pergunta deve ser formulada como uma pergunta real que um leitor faria (incluir ponto de interrogação).
            2. As perguntas devem ser relevantes para o tema e o mercado português.
            3. As respostas devem ser informativas e úteis, não apenas promocionais.
            4. NÃO inclua um título "Perguntas Frequentes" ou "FAQ" - apenas as perguntas e respostas.
            5. NÃO inclua texto introdutório antes das perguntas ou conclusivo após as respostas.
            """
        
        else:
            section_prompt = f"""
            Cria conteúdo HTML para a seção '{section}' do artigo sobre "{topic}".
            
            O conteúdo deve ser:
            - Em Português Europeu (de Portugal)
            - Profissional e informativo
            - Entre 200-300 palavras
            - Formatado com parágrafos HTML (<p>)
            - Sem títulos ou subtítulos
            """
        
        # Conteúdo similar para referência
        reference_content = ""
        if similar_content and similar_content.get('content'):
            # Limitar a quantidade de conteúdo de referência para não sobrecarregar
            reference_examples = similar_content.get('content', [])[:2]  # Limitar a 2 exemplos
            
            if reference_examples:
                reference_content = "Conteúdo similar para referência (não copie diretamente, apenas inspire-se na abordagem):\n\n"
                for i, example in enumerate(reference_examples, 1):
                    excerpt = example.get('text', '')[:500]  # Limitar tamanho do exemplo
                    reference_content += f"Exemplo {i}:\n{excerpt}\n\n"
        
        # Montar o prompt final
        full_prompt = base_prompt + "\n\n" + section_prompt
        
        # Adicionar links específicos para esta seção
        if links_instructions:
            full_prompt += "\n\n" + links_instructions
        
        # Adicionar conteúdo de referência, se disponível
        if reference_content:
            full_prompt += "\n\n" + reference_content
        
        # Adicionar instruções finais para garantir a inclusão dos links
        if relevant_links:
            full_prompt += "\n\nIMPORTANTE: Certifique-se de incluir OBRIGATORIAMENTE todos os links específicos mencionados acima, incorporando-os naturalmente no texto. A inclusão destes links é essencial para o SEO e a experiência do utilizador."
        
        return full_prompt
    
    def _validate_content(self, article: Dict[str, str]) -> List[str]:
        """Valida o conteúdo do artigo.
        
        Args:
            article: Dicionário com as seções do artigo
            
        Returns:
            Lista de erros encontrados (vazia se não houver erros)
        """
        errors = []
        
        # Validar contagem de palavras para cada seção
        for section, content in article.items():
            if section == "pre_cta":
                continue  # Pular validação do pré-CTA
                
            section_upper = section.upper()
            requirements = SECTION_REQUIREMENTS.get(section_upper, {})
            min_words = int(requirements.get('min_words', 100) * 0.9)  # 10% de tolerância para menos
            max_words = int(requirements.get('max_words', 500) * 1.2)  # 20% de tolerância para mais
            
            word_count = len(content.split())
            
            # Verificar se está dentro dos limites (com tolerância)
            if word_count < min_words or word_count > max_words:
                errors.append(f"Seção {section_upper}: {word_count} palavras (esperado: {min_words}-{max_words})")
        
        # Validar menção aos serviços da Descomplicar
        # (simplificado, apenas verifica se há alguma menção)
        category = self._extract_category(article)
        if category:
            services = WP_CATEGORIES.get(category, {}).get('services', [])
            services_mentioned = any(service.lower() in (article.get("interest", "") + article.get("decision", "")).lower() for service in services)
            
            if not services_mentioned:
                errors.append("Serviços Descomplicar não mencionados adequadamente")
        
        # Pode-se adicionar mais validações de qualidade aqui
        
        return errors
    
    def _fix_content_errors(self, article: Dict[str, str], errors: List[str]) -> Dict[str, str]:
        """Tenta corrigir erros de conteúdo.
        
        Args:
            article: Dicionário com as seções do artigo
            errors: Lista de erros encontrados
            
        Returns:
            Artigo corrigido
        """
        # Identificar seções com problemas de contagem de palavras
        sections_to_fix = []
        for error in errors:
            if "palavras (esperado:" in error:
                section = error.split(":", 1)[0].strip().lower()
                sections_to_fix.append(section)
        
        # Tentar corrigir problemas de serviços não mencionados
        services_error = any("Serviços Descomplicar não mencionados" in error for error in errors)
        
        # Nenhuma necessidade de corrigir se não há erros específicos
        if not sections_to_fix and not services_error:
            return article
        
        # Reconstruir artigo corrigido
        topic = self._extract_topic(article)
        category = self._extract_category(article)
        
        # Se não conseguir extrair o tema ou categoria, não pode corrigir
        if not topic or not category:
            return article
        
        return article  # Por enquanto, retorna sem modificações - implementação futura
    
    def _extract_topic(self, article: Dict[str, str]) -> str:
        """Extrai o tópico do artigo a partir do conteúdo.
        
        Args:
            article: Dicionário com as seções do artigo
            
        Returns:
            Tópico extraído ou string vazia
        """
        # Implementação simplificada
        # Em um caso real, usaria processamento de linguagem natural
        content = article.get("attention", "")
        if not content:
            return ""
            
        # Retorna as primeiras palavras como tópico
        words = content.split()[:5]
        return " ".join(words)
    
    def _extract_category(self, article: Dict[str, str]) -> str:
        """Tenta extrair a categoria do artigo.
        
        Args:
            article: Dicionário com as seções do artigo
            
        Returns:
            Categoria extraída ou string vazia
        """
        # Implementação simplificada
        # Em um caso real, usaria classificação de texto
        content = article.get("interest", "") + article.get("decision", "")
        
        # Verifica qual categoria tem mais serviços mencionados
        best_category = ""
        best_count = 0
        
        for category, data in WP_CATEGORIES.items():
            services = data.get('services', [])
            count = sum(service.lower() in content.lower() for service in services)
            
            if count > best_count:
                best_count = count
                best_category = category
        
        return best_category

class Article:
    """Representa um artigo gerado com todas as suas seções."""
    
    def __init__(self, title: str, category: str, sections: Dict[str, str]):
        """
        Inicializa um artigo.
        
        Args:
            title: Título do artigo
            category: Categoria do artigo
            sections: Dicionário com as seções do artigo
        """
        self.title = title
        self.category = category
        self.sections = sections
        self.validation_errors = {}
        
    def validate(self) -> bool:
        """
        Valida todas as seções do artigo de acordo com os requisitos.
        
        Returns:
            True se o artigo for válido, False caso contrário
        """
        self.validation_errors = {}
        
        # Verificar se todas as seções obrigatórias existem
        required_sections = ["attention", "confidence", "interest", "decision", "action", "pre_cta"]
        for section in required_sections:
            if section not in self.sections or not self.sections[section]:
                self.validation_errors[section] = ["Seção obrigatória ausente"]
        
        # Se alguma seção estiver faltando, não continua com a validação
        if self.validation_errors:
            return False
        
        # Validar cada seção
        for section_name, content in self.sections.items():
            if section_name == "pre_cta":
                continue  # Não validamos o pré-CTA da mesma forma
            
            errors = []
            
            # Verificar tamanho do conteúdo
            min_words = SECTION_REQUIREMENTS.get(section_name, {}).get("min_words", 0)
            max_words = SECTION_REQUIREMENTS.get(section_name, {}).get("max_words", float("inf"))
            
            word_count = len(content.split())
            if word_count < min_words:
                errors.append(f"Conteúdo muito curto: {word_count} palavras (mínimo: {min_words})")
            if max_words < float("inf") and word_count > max_words:
                errors.append(f"Conteúdo muito longo: {word_count} palavras (máximo: {max_words})")
                
            if errors:
                self.validation_errors[section_name] = errors
        
        return len(self.validation_errors) == 0
    
    def is_valid(self) -> bool:
        """
        Verifica se o artigo é válido.
        
        Returns:
            True se o artigo for válido, False caso contrário
        """
        return len(self.validation_errors) == 0
    
    def to_html(self) -> str:
        """
        Converte o artigo para HTML formatado.
        
        Returns:
            String HTML com o artigo completo
        """
        import re
        import random
        
        # ==================================
        # CONFIGURAÇÕES E PREPARAÇÃO
        # ==================================
        
        # Títulos aleatórios para cada seção principal
        section_titles = {
            "attention": [
                f"O Guia Definitivo sobre {self.title.split(':')[0]}",
                f"Tudo o Que Precisa Saber sobre {self.title.split(':')[0]}",
                f"Descubra o Potencial de {self.title.split(':')[0]}",
                f"Os Desafios e Oportunidades em {self.title.split(':')[0]}"
            ],
            "confidence": [
                "Como a Descomplicar Pode Ajudar o Seu Negócio",
                "Soluções Profissionais para o Seu Crescimento",
                "A Nossa Abordagem Especializada",
                "Porque Confiar na Nossa Experiência"
            ],
            "interest": [
                f"Estratégias Fundamentais para {self.title.split(':')[0]}",
                f"Componentes Essenciais de {self.title.split(':')[0]}",
                f"Como Implementar {self.title.split(':')[0]} Eficazmente",
                f"Melhores Práticas em {self.title.split(':')[0]}"
            ],
            "decision": [
                "Plano de Ação para Resultados Concretos",
                "Passos Importantes para o Seu Sucesso",
                "O Seu Roteiro para Implementação",
                "Como Começar Agora Mesmo"
            ],
            "action": [
                f"O Futuro do {self.title.split(':')[0]} Começa Hoje",
                f"Como Transformar o Seu Negócio com {self.title.split(':')[0]}",
                f"O Próximo Passo para o Sucesso em {self.title.split(':')[0]}",
                f"O Caminho para a Excelência em {self.title.split(':')[0]}"
            ]
        }
        
        # URLs dos serviços para CTAs
        service_urls = {
            "SEO e Content Marketing": "https://descomplicar.pt/servicos/marketing-conteudo/",
            "Gestão de Redes Sociais": "https://descomplicar.pt/servicos/redes-sociais/",
            "Marketing de Performance": "https://descomplicar.pt/servicos/performance/",
            "Design de Websites": "https://descomplicar.pt/servicos/websites-poderosos/",
            "E-commerce": "https://descomplicar.pt/servicos/e-commerce/",
            "Publicidade Online": "https://descomplicar.pt/servicos/anuncios-e-gestao-de-trafego/",
            "Automação de Marketing": "https://descomplicar.pt/servicos/automacao/",
            "Email Marketing": "https://descomplicar.pt/servicos/email-marketing/",
            "Branding e Identidade Visual": "https://descomplicar.pt/servicos/branding/",
            "Consultoria Digital": "https://descomplicar.pt/servicos/consultoria-digital/"
        }
        
        # FASE 1: EXTRAÇÃO E PREPARAÇÃO DOS CONTEÚDOS
        # ---------------------------------------------
        # Função para extrair tópicos numerados de um texto HTML usando BeautifulSoup
        def extract_numbered_topics(html_content):
            """Extrai tópicos numerados de um texto HTML"""
            # Padrões para identificação de tópicos
            patterns = [
                r'\b(\d+)[\.:\)]\s+(.*?)(?=<\/p>|<\/strong>|<\/b>)',  # Números com texto
                r'<(strong|b)>\s*(\d+)[\.:\)]\s+(.*?)<\/(strong|b)>',  # Números em negrito
                r'<h[2-3]>\s*(\d+)[\.:\)]\s+(.*?)<\/h[2-3]>'  # Números em h2/h3
            ]
            
            topics = []
            for pattern in patterns:
                matches = re.finditer(pattern, html_content, re.DOTALL)
                for match in matches:
                    if len(match.groups()) == 2:
                        num, title = match.groups()
                        topics.append((int(num), title.strip()))
                    elif len(match.groups()) == 3:
                        if match.group(1) in ['strong', 'b']:
                            num, title = match.group(2), match.group(3)
                else:
                            num, title = match.group(1), match.group(2)
                        topics.append((int(num), title.strip()))
                    
            return topics
        
        # Função para extrair perguntas FAQ
        def extract_faq_questions(html_content):
            """Extrai perguntas FAQ de um texto HTML"""
            # Padrões para identificação de perguntas
            patterns = [
                r'<(strong|b)>\s*(.*?\?)\s*<\/(strong|b)>',  # Perguntas em negrito
                r'<h[2-3]>\s*(.*?\?)\s*<\/h[2-3]>',  # Perguntas em h2/h3
                r'<p>\s*(Como|Quais|Qual|O que|Por que|Porque|Quando|Onde|Quem|Para que|É possível|Será que|De que forma)([^<>?]+\?)\s*<\/p>'  # Perguntas em formato normal
            ]
            
            questions = []
            for pattern in patterns:
                matches = re.finditer(pattern, html_content, re.DOTALL)
                for match in matches:
                    if len(match.groups()) == 1:
                        questions.append(match.group(1).strip())
                    elif len(match.groups()) == 2:
                        if match.group(1) in ['strong', 'b', 'h2', 'h3']:
                            questions.append(match.group(2).strip())
                        else:
                            questions.append((match.group(1) + match.group(2)).strip())
            
            return questions
        
        # Função para limpar texto HTML e extrair conteúdo principal
        def clean_html_content(html_content):
            """Remove tags HTML específicas e mantém apenas o conteúdo relevante"""
            # Remover tags h1, h2, h3 com seus conteúdos
            for tag in ['h1', 'h2', 'h3']:
                html_content = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_content, flags=re.DOTALL)
            
            # Remover tags de negrito, mas manter o conteúdo
            html_content = re.sub(r'<(strong|b)>(.*?)</(strong|b)>', r'\2', html_content, flags=re.DOTALL)
            
            # Remover tags de scripts e estilos com seus conteúdos
            for tag in ['script', 'style']:
                html_content = re.sub(f'<{tag}[^>]*>.*?</{tag}>', '', html_content, flags=re.DOTALL)
            
            # Limpar parágrafos vazios e quebras de linha múltiplas
            html_content = re.sub(r'<p>\s*</p>', '', html_content)
            html_content = re.sub(r'(<br>\s*){2,}', '<br>', html_content)
            
            return html_content
        
        # Preparar o conteúdo de cada seção
        attention_content = clean_html_content(self.sections.get("attention", ""))
        confidence_content = clean_html_content(self.sections.get("confidence", ""))
        interest_content = clean_html_content(self.sections.get("interest", ""))
        decision_content = clean_html_content(self.sections.get("decision", ""))
        action_content = clean_html_content(self.sections.get("action", ""))
        faq_content = clean_html_content(self.sections.get("faq", ""))
        
        # Extrair tópicos numerados das seções de interesse e decisão
        interest_topics = extract_numbered_topics(self.sections.get("interest", ""))
        decision_topics = extract_numbered_topics(self.sections.get("decision", ""))
        
        # Extrair perguntas FAQ
        faq_questions = extract_faq_questions(self.sections.get("faq", ""))
        
        # FASE 2: CONSTRUÇÃO ESTRUTURADA DO HTML
        # --------------------------------------
        final_html = []
        
        # 1. Seção de Atenção
        if attention_content:
            final_html.append('<div class="article-section attention">')
            final_html.append(f'<h2>{random.choice(section_titles["attention"])}</h2>')
            # Incluir parágrafos de introdução originais, mas sem os tópicos numerados
            paragraphs = re.findall(r'<p>(.*?)<\/p>', attention_content)
            for p in paragraphs:
                # Verifica se o parágrafo não é um tópico numerado
                if not re.match(r'^\s*\d+[\.:\)]', p):
                    final_html.append(f'<p>{p}</p>')
            final_html.append('</div>')
        
        # 2. Seção de Confiança
        if confidence_content:
            final_html.append('<div class="article-section confidence">')
            final_html.append(f'<h2>{random.choice(section_titles["confidence"])}</h2>')
            # Incluir parágrafos, mas sem os tópicos numerados
            paragraphs = re.findall(r'<p>(.*?)<\/p>', confidence_content)
            for p in paragraphs:
                if not re.match(r'^\s*\d+[\.:\)]', p):
                    final_html.append(f'<p>{p}</p>')
            
            # Adicionar lista de tópicos que serão abordados
            if interest_topics:
                final_html.append('<p>Ao longo deste artigo, abordaremos os seguintes tópicos:</p>')
                final_html.append('<ol>')
                for i, (_, title) in enumerate(interest_topics, 1):
                    final_html.append(f'<li>{title}</li>')
                final_html.append('</ol>')
            
            # Adicionar CTA A em destaque
            services = WP_CATEGORIES.get(self.category, {}).get('services', [])
            if services:
                final_html.append('<div class="cta-box primary-cta" style="background-color: #f2d9a2; border-radius: 8px; padding: 25px; margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">')
                final_html.append('<h3 style="margin-top: 0; margin-bottom: 15px; color: #333; font-size: 22px; font-weight: 600;">Precisa de ajuda profissional?</h3>')
                final_html.append(f'<p style="margin-bottom: 20px; font-size: 16px; line-height: 1.5;">A Descomplicar está especializada em {self.title.split(":")[0]}. Marque uma reunião gratuita com um dos nossos especialistas.</p>')
                
                # Serviços como botões em linha
                final_html.append('<div class="services-links" style="display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 30px;">')
                for service in services:
                    service_url = service_urls.get(service, "/servicos/")
                    final_html.append(f'<a href="{service_url}" class="service-link" style="display: inline-block; padding: 8px 15px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #ccc; font-weight: 500; font-size: 14px; margin-bottom: 5px;">{service}</a>')
                final_html.append('</div>')
                
                # Botões de CTA em linha
                final_html.append('<div class="cta-buttons" style="display: flex; flex-wrap: wrap; gap: 12px;">')
                final_html.append('<a href="https://descomplicar.pt/marcar-reuniao/" class="button primary" style="display: inline-block; padding: 12px 20px; background-color: #333; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center; min-width: 120px; margin-right: 10px;">Marcar Reunião</a>')
                final_html.append('<a href="https://descomplicar.pt/pedido-de-orcamento/" class="button secondary" style="display: inline-block; padding: 12px 20px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #333; font-weight: bold; text-align: center; min-width: 120px; margin-right: 10px;">Pedir Orçamento</a>')
                final_html.append('<a href="https://descomplicar.pt/contacto/" class="button secondary" style="display: inline-block; padding: 12px 20px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #333; font-weight: bold; text-align: center; min-width: 120px;">Contacto</a>')
                final_html.append('</div>')
                final_html.append('</div>')
            
            final_html.append('</div>')
        
        # 3. Seção de Interesse (com tópicos numerados)
        if interest_content or interest_topics:
            final_html.append('<div class="article-section interest">')
            final_html.append(f'<h2>{random.choice(section_titles["interest"])}</h2>')
            
            # Incluir introdução da seção (apenas parágrafos antes do primeiro tópico)
            paragraphs = re.findall(r'<p>(.*?)<\/p>', interest_content)
            for p in paragraphs[:2]:  # Primeiros parágrafos introdutórios
                if not re.match(r'^\s*\d+[\.:\)]', p):
                    final_html.append(f'<p>{p}</p>')
            
            # Adicionar tópicos numerados com formatação consistente
            # Reordenar e garantir numeração sequencial correta
            if interest_topics:
                # Ordenar por número original (primeiro elemento da tupla)
                interest_topics.sort(key=lambda x: x[0])
                
                # Dividir o conteúdo em blocos para cada tópico
                content_blocks = re.split(r'<h[2-3]>\s*\d+[\.:\)]\s+.*?<\/h[2-3]>', interest_content)
                
                # Garantir que temos conteúdo para cada tópico
                if len(content_blocks) > len(interest_topics):
                    content_blocks = content_blocks[1:]  # Remover o primeiro bloco (introdução)
                
                # Adicionar cada tópico com seu conteúdo
                for i, ((_, title), content) in enumerate(zip(interest_topics, content_blocks[:len(interest_topics)]), 1):
                final_html.append(f'<h3>{i}. {title}</h3>')
                
                    # Extrair o conteúdo relevante após o título
                    paragraphs = re.findall(r'<p>(.*?)<\/p>', content)
                    for p in paragraphs:
                            final_html.append(f'<p>{p}</p>')
                    
                    # Verificar se há listas e adicioná-las
                    lists = re.findall(r'<(ul|ol)>(.*?)<\/(ul|ol)>', content, re.DOTALL)
                    for list_type, list_content in lists:
                        final_html.append(f'<{list_type}>{list_content}</{list_type}>')
            
            final_html.append('</div>')
        
        # 4. Seção de Decisão (com tópicos numerados continuando a sequência)
        if decision_content or decision_topics:
            final_html.append('<div class="article-section decision">')
            final_html.append(f'<h2>{random.choice(section_titles["decision"])}</h2>')
            
            # Incluir introdução da seção
            paragraphs = re.findall(r'<p>(.*?)<\/p>', decision_content)
            for p in paragraphs[:2]:  # Primeiros parágrafos introdutórios
                if not re.match(r'^\s*\d+[\.:\)]', p):
                    final_html.append(f'<p>{p}</p>')
            
            # Adicionar tópicos numerados (continuando a sequência da seção de interesse)
            start_number = len(interest_topics) + 1
            if decision_topics:
                decision_topics.sort(key=lambda x: x[0])
                
                content_blocks = re.split(r'<h[2-3]>\s*\d+[\.:\)]\s+.*?<\/h[2-3]>', decision_content)
                if len(content_blocks) > len(decision_topics):
                    content_blocks = content_blocks[1:]  # Remover o primeiro bloco (introdução)
                
                for i, ((_, title), content) in enumerate(zip(decision_topics, content_blocks[:len(decision_topics)]), start_number):
                final_html.append(f'<h3>{i}. {title}</h3>')
                
                    paragraphs = re.findall(r'<p>(.*?)<\/p>', content)
                    for p in paragraphs:
                            final_html.append(f'<p>{p}</p>')
                    
                    lists = re.findall(r'<(ul|ol)>(.*?)<\/(ul|ol)>', content, re.DOTALL)
                    for list_type, list_content in lists:
                        final_html.append(f'<{list_type}>{list_content}</{list_type}>')
            
            final_html.append('</div>')
        
        # 5. Seção de Ação
        if action_content:
            final_html.append('<div class="article-section action">')
            final_html.append(f'<h2>{random.choice(section_titles["action"])}</h2>')
            
            # Incluir parágrafos, remover qualquer tópico numerado
            paragraphs = re.findall(r'<p>(.*?)<\/p>', action_content)
            for p in paragraphs:
                if not re.match(r'^\s*\d+[\.:\)]', p):
                    final_html.append(f'<p>{p}</p>')
            
            # Adicionar CTA final
            final_html.append('<div class="cta-box final-cta" style="background-color: #f2d9a2; border-radius: 8px; padding: 25px; margin: 30px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">')
            final_html.append('<h3 style="margin-top: 0; margin-bottom: 15px; color: #333; font-size: 22px; font-weight: 600;">Precisa de ajuda profissional?</h3>')
            final_html.append(f'<p style="margin-bottom: 20px; font-size: 16px; line-height: 1.5;">A Descomplicar está especializada em {self.title.split(":")[0]}. Marque uma reunião gratuita com um dos nossos especialistas.</p>')
            
            # Serviços como botões em linha
            services = WP_CATEGORIES.get(self.category, {}).get('services', [])
            final_html.append('<div class="services-links" style="display: flex; flex-wrap: wrap; gap: 12px; margin-bottom: 30px;">')
            for service in services:
                service_url = service_urls.get(service, "/servicos/")
                final_html.append(f'<a href="{service_url}" class="service-link" style="display: inline-block; padding: 8px 15px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #ccc; font-weight: 500; font-size: 14px; margin-bottom: 5px;">{service}</a>')
            final_html.append('</div>')
            
            # Botões de CTA em linha
            final_html.append('<div class="cta-buttons" style="display: flex; flex-wrap: wrap; gap: 12px;">')
            final_html.append('<a href="https://descomplicar.pt/marcar-reuniao/" class="button primary" style="display: inline-block; padding: 12px 20px; background-color: #333; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center; min-width: 120px; margin-right: 10px;">Marcar Reunião</a>')
            final_html.append('<a href="https://descomplicar.pt/pedido-de-orcamento/" class="button secondary" style="display: inline-block; padding: 12px 20px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #333; font-weight: bold; text-align: center; min-width: 120px; margin-right: 10px;">Pedir Orçamento</a>')
            final_html.append('<a href="https://descomplicar.pt/contacto/" class="button secondary" style="display: inline-block; padding: 12px 20px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 1px solid #333; font-weight: bold; text-align: center; min-width: 120px;">Contacto</a>')
            final_html.append('</div>')
            final_html.append('</div>')
            
            final_html.append('</div>')
        
        # 6. Seção de FAQ
        if faq_content and faq_questions:
            final_html.append('<div class="faq-section">')
            final_html.append('<h2>Perguntas Frequentes</h2>')
            
            # Dividir o conteúdo em blocos para cada pergunta
            content_blocks = re.split(r'<h[2-3]>.*?\?</h[2-3]>|<(strong|b)>.*?\?</(strong|b)>', faq_content)
            
            # Garantir que temos conteúdo para cada pergunta
            if len(content_blocks) > len(faq_questions):
                content_blocks = content_blocks[1:]  # Remover o primeiro bloco (introdução, se houver)
            
            # Adicionar cada pergunta com sua resposta
            for i, (question, content) in enumerate(zip(faq_questions, content_blocks[:len(faq_questions)])):
                final_html.append(f'<h3>{question}</h3>')
                
                # Extrair o conteúdo relevante após a pergunta
                paragraphs = re.findall(r'<p>(.*?)<\/p>', content)
                for p in paragraphs:
                    # Verificar se o parágrafo não é uma pergunta
                    if not re.search(r'\?', p) or len(p) < 15:
                            final_html.append(f'<p>{p}</p>')
                
                # Verificar se há listas e adicioná-las
                lists = re.findall(r'<(ul|ol)>(.*?)<\/(ul|ol)>', content, re.DOTALL)
                for list_type, list_content in lists:
                    final_html.append(f'<{list_type}>{list_content}</{list_type}>')
            
            # Adicionar CTA após FAQ
            final_html.append('<div class="cta-box post-faq-cta" style="background-color: #f2d9a2; border-radius: 8px; padding: 25px; margin: 40px 0; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">')
            final_html.append(f'<h3 style="margin-top: 0; margin-bottom: 15px; color: #333; font-size: 22px; font-weight: 600;">Pronto para Potenciar o Seu Negócio com {self.title.split(":")[0]}?</h3>')
            final_html.append(f'<p style="margin-bottom: 20px; font-size: 16px; line-height: 1.5;">Não deixe para amanhã o que pode transformar o seu negócio hoje. A Descomplicar oferece soluções personalizadas em {self.title.split(":")[0]} para ajudar o seu negócio a alcançar resultados concretos.</p>')
            
            # Botões de CTA em linha (maior destaque)
            final_html.append('<div class="final-cta-buttons" style="display: flex; flex-wrap: wrap; gap: 15px; justify-content: center;">')
            final_html.append('<a href="https://descomplicar.pt/marcar-reuniao/" class="button primary-large" style="display: inline-block; padding: 15px 30px; background-color: #333; color: white; text-decoration: none; border-radius: 5px; font-weight: bold; text-align: center; font-size: 18px; min-width: 200px; margin-right: 15px;">Agendar Consultoria Gratuita</a>')
            final_html.append('<a href="https://descomplicar.pt/pedido-de-orcamento/" class="button secondary-large" style="display: inline-block; padding: 15px 30px; background-color: white; color: #333; text-decoration: none; border-radius: 5px; border: 2px solid #333; font-weight: bold; text-align: center; font-size: 18px; min-width: 200px;">Solicitar Proposta Personalizada</a>')
            final_html.append('</div>')
            final_html.append('</div>')
            
            final_html.append('</div>')
        
        # FASE 3: LIMPEZA FINAL
        # --------------------
        html = '\n'.join(final_html)
        
        # Remover qualquer HTML malformado
        html = re.sub(r'<(?!(h2|h3|p|ul|ol|li|div|strong|b|i|em|a|br|span|img)\b)[^>]*>', '', html)
        
        # Remover duplicações de tags HTML
        html = re.sub(r'<([a-z0-9]+)[^>]*>\s*</\1>', '', html)
        
        # Remover parágrafos vazios
        html = re.sub(r'<p>\s*</p>', '', html)
        
        # Simplificar múltiplas quebras de linha
        html = re.sub(r'(\s*<br>\s*){2,}', '<br>', html)
        
        # Garantir abertura e fechamento correto de tags
        soup = BeautifulSoup(html, 'html.parser')
        html = str(soup)
        
        return html.strip()
    
    def get_word_count(self) -> int:
        """
        Obtém a contagem total de palavras no artigo.
        
        Returns:
            Número total de palavras
        """
        total = 0
        for section_name, content in self.sections.items():
            if section_name != "pre_cta":  # Não contamos o pré-CTA
                total += len(content.split())
        return total 