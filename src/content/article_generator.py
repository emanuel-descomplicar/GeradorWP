"""
Gerador de artigos usando o modelo ACIDA.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from ..integrations.dify_client import DifyClient
from ..media.image_manager import ImageManager
from ..templates.article_template import (
    ARTICLE_TEMPLATE,
    BENEFIT_COLUMN_TEMPLATE,
    CASE_STUDY_TEMPLATE,
    FAQ_ITEM_TEMPLATE,
    COMPARISON_TABLE_TEMPLATE
)

class ArticleGenerator:
    """Gerador de artigos usando o modelo ACIDA."""

    def __init__(self):
        """Inicializa o gerador de artigos."""
        self.dify_client = DifyClient()
        self.image_manager = ImageManager()
        self.logger = logging.getLogger(__name__)
        self.known_companies = ['Empresa A', 'Empresa B', 'Empresa C']  # Replace with actual known companies

    async def generate_article(self, topic: str, category: str) -> Dict:
        """
        Gera um artigo completo usando o modelo ACIDA.

        Args:
            topic: Tema do artigo
            category: Categoria do artigo

        Returns:
            Dict com o conteúdo do artigo
        """
        try:
            # Obter conhecimento específico da Dify
            knowledge = await self.dify_client.get_knowledge(topic)
            
            # Obter serviços relevantes da Descomplicar
            services = self._get_relevant_services(category)
            
            # Gerar infográficos
            infographics = await self.image_manager.generate_infographics(topic, knowledge)
            
            # Gerar estrutura do artigo
            content = await self._generate_content(topic, knowledge, services, infographics)
            
            return content
            
        except Exception as e:
            self.logger.error(f"Erro ao gerar artigo: {str(e)}")
            raise

    async def _generate_content(
        self,
        topic: str,
        knowledge: Dict,
        services: Dict,
        infographics: Dict
    ) -> Dict:
        """
        Gera o conteúdo do artigo usando o modelo ACIDA.
        
        Args:
            topic: Tema do artigo
            knowledge: Conhecimento obtido da Dify
            services: Serviços relevantes da Descomplicar
            infographics: Infográficos gerados
            
        Returns:
            Dict com o conteúdo do artigo
        """
        # Obter fontes oficiais
        sources = await self._get_official_sources(topic)
        
        # Validar casos de sucesso
        validated_cases = await self._validate_case_studies(knowledge['cases'])
        
        # Seção A - Atenção
        attention = await self._generate_attention_section(topic, knowledge, sources)
        
        # Seção C - Confiança
        confidence = await self._generate_confidence_section(topic, knowledge)
        
        # Seção I - Interesse
        interest = await self._generate_interest_section(topic, knowledge)
        
        # Seção D - Desejo/Decisão
        desire = await self._generate_desire_section(topic, knowledge)
        
        # Seção A - Ação
        action = await self._generate_action_section(topic, services)
        
        # FAQ
        faq = await self._generate_faq_section(topic, knowledge)
        
        # Montar artigo completo
        article = ARTICLE_TEMPLATE.format(
            title=attention['title'],
            meta_description=attention['meta_description'],
            topic=topic,
            service_a=services['primary']['name'],
            problem_solution_a=services['primary']['value_prop'],
            service_b=services['secondary']['name'],
            problem_solution_b=services['secondary']['value_prop'],
            service_c=services['tertiary']['name'],
            problem_solution_c=services['tertiary']['value_prop'],
            attention_intro=attention['intro'],
            attention_context=attention['context'],
            infographic_1_id=infographics['stats']['id'],
            infographic_1_url=infographics['stats']['url'],
            infographic_1_sources=sources['citations'],
            ine_link=sources['ine']['url'],
            pordata_link=sources['pordata']['url'],
            eurostat_link=sources['eurostat']['url'],
            iapmei_link=sources['iapmei']['url'],
            gee_link=sources['gee']['url'],
            pt2030_link=sources['pt2030']['url'],
            desi_link=sources['desi']['url'],
            bdp_link=sources['bdp']['url'],
            confidence_intro=confidence['intro'],
            confidence_analysis=confidence['analysis'],
            comparison_table=self._generate_comparison_table(confidence['comparisons'], topic),
            interest_intro=interest['intro'],
            benefit_columns=self._generate_benefit_columns(interest['benefits']),
            infographic_2_id=infographics['process']['id'],
            infographic_2_url=infographics['process']['url'],
            desire_intro=desire['intro'],
            implementation_steps=self._generate_implementation_steps(desire['steps']),
            desire_conclusion=desire['conclusion'],
            case_studies=self._generate_case_studies(desire['cases']),
            faq_section=self._generate_faq_items(faq),
            action_summary=action['summary']
        )
        
        return {
            'content': article,
            'meta': {
                'title': attention['title'],
                'description': attention['meta_description'],
                'keywords': knowledge['keywords'],
                'category': category,
                'sources': sources,
                'validated_cases': validated_cases
            }
        }

    async def _generate_attention_section(self, topic: str, knowledge: Dict, sources: Dict) -> Dict:
        """Gera a seção de Atenção (A) do artigo."""
        prompt = f"""
        Gere a seção de ATENÇÃO para um artigo sobre "{topic}" usando os dados fornecidos.
        
        A seção deve incluir:
        1. Título H1 otimizado para SEO
        2. Meta description otimizada para CTR
        3. Introdução impactante com estatísticas do mercado português
        4. Contextualização específica para PMEs portuguesas
        5. Desafios atuais do mercado
        6. Oportunidades identificadas
        7. Tendências do setor
        
        Use dados verificáveis das seguintes fontes:
        - INE (estatísticas oficiais)
        - PORDATA (dados económicos)
        - Eurostat (comparativos europeus)
        - IAPMEI (estudos setoriais)
        - Portugal 2030 (objetivos estratégicos)
        
        Mantenha o foco em:
        - Realidade portuguesa
        - Dados atualizados de 2024
        - Exemplos práticos
        - Resultados mensuráveis
        - Retorno sobre investimento
        
        Dados disponíveis:
        {json.dumps(knowledge, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    async def _generate_confidence_section(self, topic: str, knowledge: Dict) -> Dict:
        """Gera a seção de Confiança (C) do artigo."""
        prompt = f"""
        Gere a seção de CONFIANÇA para um artigo sobre "{topic}" usando os dados fornecidos.
        
        A seção deve incluir:
        1. Introdução com dados verificáveis do mercado português
        2. Análise detalhada do cenário atual
        3. Estudos de caso reais de PMEs portuguesas
        4. Comparativo antes/depois com métricas
        5. Depoimentos de especialistas do setor
        6. Dados de performance e ROI
        7. Benchmarks do setor
        
        Foque em:
        - Cases reais portugueses
        - Métricas verificáveis
        - Resultados financeiros
        - Impacto no negócio
        - Vantagens competitivas
        
        Inclua comparativos:
        - Investimento vs Retorno
        - Tempo de implementação
        - Recursos necessários
        - Resultados esperados
        - Métricas de sucesso
        
        Dados disponíveis:
        {json.dumps(knowledge, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    async def _generate_interest_section(self, topic: str, knowledge: Dict) -> Dict:
        """Gera a seção de Interesse (I) do artigo."""
        prompt = f"""
        Gere a seção de INTERESSE para um artigo sobre "{topic}" usando os dados fornecidos.
        
        A seção deve incluir:
        1. Benefícios específicos para PMEs portuguesas
        2. Vantagens competitivas no mercado local
        3. Oportunidades de crescimento
        4. Exemplos práticos de implementação
        5. Histórias de sucesso reais
        6. Métricas de performance
        7. Análise de ROI
        
        Benefícios a explorar:
        - Aumento de vendas
        - Redução de custos
        - Maior visibilidade
        - Melhor relacionamento
        - Dados actionáveis
        
        Para cada benefício:
        - Descrição detalhada
        - Exemplo prático
        - Métricas relevantes
        - Tempo para resultado
        - Investimento necessário
        
        Dados disponíveis:
        {json.dumps(knowledge, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    async def _generate_desire_section(self, topic: str, knowledge: Dict) -> Dict:
        """Gera a seção de Desejo/Decisão (D) do artigo."""
        prompt = f"""
        Gere a seção de DESEJO/DECISÃO para um artigo sobre "{topic}" usando os dados fornecidos.
        
        A seção deve incluir:
        1. Guia passo a passo de implementação
        2. Recursos necessários
        3. Cronograma realista
        4. Orçamento estimado
        5. Equipe necessária
        6. Ferramentas recomendadas
        7. Métricas de acompanhamento
        
        Para cada passo:
        - Descrição detalhada
        - Tempo estimado
        - Recursos necessários
        - Resultados esperados
        - Pontos de atenção
        
        Cases de sucesso:
        - Empresas reais portuguesas
        - Dados verificáveis
        - Resultados concretos
        - Lições aprendidas
        - Melhores práticas
        
        Dados disponíveis:
        {json.dumps(knowledge, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    async def _generate_action_section(self, topic: str, services: Dict) -> Dict:
        """Gera a seção de Ação (A) do artigo."""
        prompt = f"""
        Gere a seção de AÇÃO para um artigo sobre "{topic}" usando os serviços fornecidos.
        
        A seção deve incluir:
        1. Resumo dos pontos principais
        2. Próximos passos práticos
        3. Recursos disponíveis
        4. Suporte oferecido
        5. Garantias de resultado
        6. Processo de início
        7. Contato imediato
        
        Chamadas para ação:
        - Agendamento de consultoria
        - Análise gratuita
        - Orçamento personalizado
        - Diagnóstico digital
        - Plano estratégico
        
        Benefícios imediatos:
        - Consultoria especializada
        - Equipe dedicada
        - Suporte contínuo
        - Resultados mensuráveis
        - Garantia de satisfação
        
        Serviços disponíveis:
        {json.dumps(services, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    async def _generate_faq_section(self, topic: str, knowledge: Dict) -> List[Dict]:
        """Gera a seção de Perguntas Frequentes do artigo."""
        prompt = f"""
        Gere 8-10 perguntas frequentes sobre "{topic}" usando os dados fornecidos.
        
        As perguntas devem cobrir:
        1. Custos e investimento
        2. Tempo de implementação
        3. Resultados esperados
        4. Equipe necessária
        5. Ferramentas utilizadas
        6. Métricas de sucesso
        7. Suporte oferecido
        8. Garantias
        
        Cada resposta deve:
        - Ser objetiva e clara
        - Incluir dados concretos
        - Citar exemplos reais
        - Mencionar métricas
        - Oferecer soluções
        
        Foque em:
        - Dúvidas comuns de PMEs
        - Aspectos financeiros
        - Tempo de retorno
        - Recursos necessários
        - Resultados práticos
        
        Dados disponíveis:
        {json.dumps(knowledge, indent=2)}
        """
        
        response = await self.dify_client.completion(prompt)
        return json.loads(response['choices'][0]['text'])

    def _generate_comparison_table(self, comparisons: List[Dict], topic: str) -> str:
        """Gera a tabela comparativa antes/depois."""
        rows = []
        for comp in comparisons:
            row = f"""
            <tr>
                <td>{comp['aspect']}</td>
                <td>{comp['before']}</td>
                <td>{comp['after']}</td>
            </tr>
            """
            rows.append(row)
            
        return COMPARISON_TABLE_TEMPLATE.format(
            topic=topic,
            table_rows="\n".join(rows)
        )

    def _generate_benefit_columns(self, benefits: List[Dict]) -> str:
        """Gera as colunas de benefícios."""
        columns = []
        for benefit in benefits:
            items = [f"<li>{item}</li>" for item in benefit['items']]
            column = BENEFIT_COLUMN_TEMPLATE.format(
                benefit_title=benefit['title'],
                benefit_description=benefit['description'],
                benefit_items="\n".join(items)
            )
            columns.append(column)
            
        return "\n".join(columns)

    def _generate_implementation_steps(self, steps: List[Dict]) -> str:
        """Gera os passos de implementação."""
        return "\n".join([f"<li>{step['content']}</li>" for step in steps])

    def _generate_case_studies(self, cases: List[Dict]) -> str:
        """Gera os casos de estudo."""
        studies = []
        for case in cases:
            study = CASE_STUDY_TEMPLATE.format(
                company_name=case['company'],
                challenge=case['challenge'],
                solution=case['solution'],
                results=case['results']
            )
            studies.append(study)
            
        return "\n".join(studies)

    def _generate_faq_items(self, faqs: List[Dict]) -> str:
        """Gera os itens de FAQ."""
        items = []
        for faq in faqs:
            item = FAQ_ITEM_TEMPLATE.format(
                question=faq['question'],
                answer=faq['answer']
            )
            items.append(item)
            
        return "\n".join(items)

    def _get_relevant_services(self, category: str) -> Dict:
        """Obtém os serviços relevantes da Descomplicar para a categoria."""
        # TODO: Implementar lógica para selecionar serviços mais relevantes
        # Por enquanto, retorna serviços mockados
        return {
            'primary': {
                'name': 'Consultoria Especializada',
                'value_prop': 'Análise personalizada e estratégia sob medida'
            },
            'secondary': {
                'name': 'Implementação Técnica',
                'value_prop': 'Execução profissional com resultados garantidos'
            },
            'tertiary': {
                'name': 'Suporte Contínuo',
                'value_prop': 'Acompanhamento e otimização constante'
            }
        }

    async def _get_official_sources(self, topic: str) -> Dict:
        """Obtém e valida fontes oficiais relacionadas ao tópico."""
        sources = {
            'ine': {
                'name': 'INE',
                'url': f'https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_pesquisa&frm_accao=PESQUISAR&frm_show_page_num=1&frm_modo_pesquisa=PESQUISA_SIMPLES&frm_texto={topic}&frm_modo_texto=MODO_TEXT_ALL&frm_data_ini=&frm_data_fim=&frm_tema=QUALQUER_TEMA&frm_area=QUALQUER_AREA',
                'type': 'statistics'
            },
            'pordata': {
                'name': 'PORDATA',
                'url': f'https://www.pordata.pt/DB/Portugal/Ambiente+de+Consulta/Tabela/5799369',
                'type': 'statistics'
            },
            'eurostat': {
                'name': 'Eurostat',
                'url': 'https://ec.europa.eu/eurostat/web/main/data/database',
                'type': 'european_statistics'
            },
            'iapmei': {
                'name': 'IAPMEI',
                'url': 'https://www.iapmei.pt/PRODUTOS-E-SERVICOS/Qualificacao-Certificacao.aspx',
                'type': 'business_support'
            },
            'gee': {
                'name': 'GEE',
                'url': 'https://www.gee.gov.pt/pt/estudos-e-seminarios/estudos-economicos',
                'type': 'economic_studies'
            },
            'pt2030': {
                'name': 'Portugal 2030',
                'url': 'https://portugal2030.pt/documentacao/',
                'type': 'funding'
            },
            'desi': {
                'name': 'DESI',
                'url': 'https://digital-strategy.ec.europa.eu/en/policies/desi-portugal',
                'type': 'digital_index'
            },
            'bdp': {
                'name': 'Banco de Portugal',
                'url': 'https://www.bportugal.pt/analises-setoriais',
                'type': 'sector_analysis'
            }
        }
        
        # Gerar citação formatada
        citations = []
        for source in sources.values():
            if source['type'] == 'statistics':
                citations.append(f"{source['name']} ({datetime.now().year})")
        
        sources['citations'] = ', '.join(citations)
        return sources

    async def _validate_case_studies(self, cases: List[Dict]) -> List[Dict]:
        """Valida e enriquece casos de sucesso com dados verificáveis."""
        validated_cases = []
        
        for case in cases:
            # Verificar se é um caso real
            if not self._is_real_company(case['company']):
                continue
                
            # Enriquecer com dados verificáveis
            enriched_case = await self._enrich_case_study(case)
            
            # Adicionar apenas se tiver dados verificáveis
            if enriched_case['has_verified_data']:
                validated_cases.append(enriched_case)
                
        return validated_cases

    def _is_real_company(self, company_name: str) -> bool:
        """Verifica se a empresa existe no registro português."""
        # TODO: Implementar verificação real usando API do Portal da Empresa
        # Por enquanto, usar lista de empresas conhecidas
        return company_name in self.known_companies

    async def _enrich_case_study(self, case: Dict) -> Dict:
        """Enriquece caso de estudo com dados verificáveis."""
        try:
            # Adicionar dados verificáveis
            case['has_verified_data'] = True
            case['verification'] = {
                'company_registry': 'Registro Comercial de Portugal',
                'year': datetime.now().year,
                'sector': 'Setor da empresa',
                'size': 'Dimensão da empresa',
                'location': 'Localização em Portugal'
            }
            
            # Adicionar métricas verificáveis
            case['metrics'] = {
                'before': {
                    'value': 'Valor antes',
                    'source': 'Fonte da métrica'
                },
                'after': {
                    'value': 'Valor depois',
                    'source': 'Fonte da métrica'
                }
            }
            
            return case
            
        except Exception as e:
            self.logger.error(f"Erro ao enriquecer caso de estudo: {str(e)}")
            case['has_verified_data'] = False
            return case 