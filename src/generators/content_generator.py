"""
Gerador de conteúdo para artigos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import time
import logging
from typing import Dict, List, Optional, Tuple

from src.config.content_config import (METRICS, QUALITY_METRICS, 
                                      SECTION_REQUIREMENTS, WP_CATEGORIES)
from src.integrations.dify_client import DifyClient

# Configuração do logging
logger = logging.getLogger(__name__)

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
        logger.info(f"ContentGenerator inicializado com knowledge_base_id: {self.knowledge_base_id}")
    
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
        
        # Buscar conteúdo similar
        logger.info(f"Buscando conteúdo similar para o tópico: '{topic}'")
        similar_content = self.dify_client.get_similar_content(
            query=topic,
            knowledge_base_id=self.knowledge_base_id
        )
        logger.info(f"Conteúdo similar encontrado")
        
        # Gerar seções
        logger.info(f"Gerando seções do artigo...")
        article_dict = {}
        
        try:
            # Criar pré-CTA (serviços)
            article_dict["pre_cta"] = self._generate_pre_cta(topic, category)
            
            # Gerar cada seção do modelo ACIDA
            article_dict["attention"] = self._generate_attention(topic, similar_content)
            article_dict["confidence"] = self._generate_confidence(topic, similar_content)
            article_dict["interest"] = self._generate_interest(topic, category, similar_content)
            article_dict["decision"] = self._generate_decision(topic, category, similar_content)
            article_dict["action"] = self._generate_action(topic)
            
            # Criando objeto Article
            article = Article(
                title=topic,
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
        prompt = self._create_section_prompt("ATTENTION", topic, similar_content=similar_content)
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
        prompt = self._create_section_prompt("CONFIDENCE", topic, similar_content=similar_content)
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
        prompt = self._create_section_prompt("INTEREST", topic, category, similar_content)
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
        prompt = self._create_section_prompt("DECISION", topic, category, similar_content)
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
        prompt = self._create_section_prompt("ACTION", topic)
        return self.dify_client.generate_content(
            prompt=prompt,
            min_words=150,
            max_words=200,
            temperature=0.7
        )
    
    def _create_section_prompt(
        self,
        section: str,
        topic: str,
        category: str = None,
        similar_content: Dict = None
    ) -> str:
        """Cria o prompt para geração de uma seção.
        
        Args:
            section: Nome da seção (ATTENTION, CONFIDENCE, etc.)
            topic: Tópico do artigo
            category: Categoria do artigo (opcional)
            similar_content: Conteúdo similar para referência (opcional)
            
        Returns:
            Prompt formatado
        """
        # Obter requisitos da seção
        requirements = SECTION_REQUIREMENTS.get(section, {})
        min_words = requirements.get('min_words', 100)
        max_words = requirements.get('max_words', 500)
        elements = requirements.get('elements', [])
        
        # Formatar prompt base
        prompt = f"""
        Gere conteúdo para a seção {section} de um artigo sobre {topic}.
        
        Requisitos:
        - Use português de Portugal (não brasileiro)
        - Inclua {', '.join(elements)}
        - Use dados de INE - Instituto Nacional de Estatística, ACEPI - Associação da Economia Digital, IDC Portugal, Comissão Europeia, Instituto Superior Técnico, Universidade do Porto, APDC - Associação Portuguesa para o Desenvolvimento das Comunicações
        - Mínimo de {min_words} palavras
        - Máximo de {max_words} palavras
        - Mantenha um tom profissional e persuasivo
        - Use exemplos específicos do mercado português
        """
        
        # Adicionar serviços e métricas relevantes para seções específicas
        if section in ["INTEREST", "DECISION"] and category:
            # Obter serviços da categoria
            services = WP_CATEGORIES.get(category, {}).get('services', [])
            prompt += f"\nServiços relevantes: {', '.join(services)}\n"
            
            # Adicionar métricas relevantes
            metrics_list = []
            for metric_category in ['produtividade', 'digital']:
                if metric_category in METRICS:
                    metrics_list.extend(METRICS[metric_category])
            
            if metrics_list:
                prompt += f"Métricas a mencionar: {', '.join(metrics_list)}\n"
        
        # Adicionar conteúdo similar, se disponível
        if similar_content and 'results' in similar_content:
            prompt += "\nConteúdo similar para referência:\n"
            for item in similar_content['results'][:1]:  # Limitar a 1 resultado
                if 'content' in item:
                    # Limitar o tamanho do conteúdo similar
                    prompt += f"- {item['content'][:1000]}..."
        
        return prompt
    
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
        category_name = WP_CATEGORIES.get(self.category, {}).get('name', 'Categoria Desconhecida')
        
        # Construir o HTML
        html_parts = [
            '<!DOCTYPE html>',
            '<html>',
            '<head>',
            f'<title>{self.title}</title>',
            '<meta charset="UTF-8">',
            '<style>',
            'body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }',
            'h1 { color: #333; }',
            '.section { margin-bottom: 30px; }',
            '.section-title { color: #666; font-size: 0.8em; text-transform: uppercase; }',
            '.services { background-color: #f5f5f5; padding: 15px; border-radius: 5px; }',
            '.services ul { padding-left: 20px; }',
            '</style>',
            '</head>',
            '<body>',
            f'<h1>{self.title}</h1>',
            f'<p><em>Categoria: {category_name}</em></p>'
        ]
        
        # Adicionar cada seção na ordem ACIDA
        sections_order = ["attention", "confidence", "interest", "pre_cta", "decision", "action"]
        section_titles = {
            "attention": "Atenção",
            "confidence": "Confiança",
            "interest": "Interesse",
            "pre_cta": "Serviços Descomplicar",
            "decision": "Decisão",
            "action": "Ação"
        }
        
        for section_name in sections_order:
            if section_name in self.sections and self.sections[section_name]:
                html_parts.append('<div class="section">')
                html_parts.append(f'<div class="section-title">{section_titles[section_name]}</div>')
                
                if section_name == "pre_cta":
                    html_parts.append('<div class="services">')
                    html_parts.append('<ul>')
                    html_parts.append(self.sections[section_name])
                    html_parts.append('</ul>')
                    html_parts.append('</div>')
                else:
                    html_parts.append(f'<div>{self.sections[section_name]}</div>')
                
                html_parts.append('</div>')
        
        # Fechar o HTML
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
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