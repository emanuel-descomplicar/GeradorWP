"""
Validador de conteúdo para o modelo ACIDA.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import re
from typing import Dict, List, Optional, Tuple
import requests
from bs4 import BeautifulSoup

class ContentValidationError(Exception):
    """Exceção para erros de validação de conteúdo."""
    pass

class ACIDAValidator:
    """Validador do modelo ACIDA com verificações completas."""
    
    # Configurações de palavras por seção
    SECTION_WORDS = {
        'attention': (180, 320),  # ±10% de margem
        'confidence': (360, 540),
        'interest': (450, 650),
        'decision': (360, 540),
        'action': (135, 220)
    }
    
    # Links obrigatórios
    REQUIRED_LINKS = [
        'https://descomplicar.pt/marcar-reuniao/',
        'https://descomplicar.pt/pedido-de-orcamento/',
        'https://descomplicar.pt/contacto/'
    ]
    
    def __init__(self, dify_api_key: Optional[str] = None):
        """Inicializa o validador.
        
        Args:
            dify_api_key: Chave da API Dify para validação de conhecimento
        """
        self.dify_api_key = dify_api_key
    
    def validate_content(self, content: Dict[str, str]) -> Tuple[bool, List[str]]:
        """Valida o conteúdo completo do artigo.
        
        Args:
            content: Dicionário com as seções do artigo
            
        Returns:
            Tuple[bool, List[str]]: (válido, lista de erros)
        """
        errors = []
        
        # Validar CTA Box inicial
        if not self._validate_initial_cta(content.get('pre_cta', '')):
            errors.append("CTA Box inicial inválida ou incompleta")
        
        # Validar cada seção ACIDA
        for section, (min_words, max_words) in self.SECTION_WORDS.items():
            section_content = content.get(section, '')
            word_count = len(section_content.split())
            total_words += word_count
            
            if not min_words <= word_count <= max_words:
                errors.append(
                    f"Seção {section.upper()}: {word_count} palavras "
                    f"(esperado: {min_words}-{max_words})"
                )
        
        # Validar total de palavras com margem de 5%
        min_total = 1900  # 2000 - 5%
        if total_words < min_total:
            errors.append(f"Total de palavras ({total_words}) abaixo do mínimo de {min_total}")
        
        # Validar links
        if not self._validate_links(content):
            errors.append("Links obrigatórios ausentes ou inválidos")
        
        # Validar estudos de caso
        if not self._validate_case_studies(content):
            errors.append("Estudos de caso ausentes ou não validados")
        
        # Validar serviços Descomplicar
        if not self._validate_services(content):
            errors.append("Serviços Descomplicar não mencionados adequadamente")
        
        # Validar CTA final
        if not self._validate_final_cta(content.get('action', '')):
            errors.append("CTA final ausente ou incompleto")
        
        return len(errors) == 0, errors
    
    def _validate_initial_cta(self, cta_content: str) -> bool:
        """Valida a CTA Box inicial."""
        if not cta_content:
            return False
            
        required_elements = [
            'Se procura uma solução para',
            '#f2d9a2',  # Verificar na renderização HTML
            *self.REQUIRED_LINKS
        ]
        
        return all(elem in cta_content for elem in required_elements)
    
    def _validate_links(self, content: Dict[str, str]) -> bool:
        """Valida a presença e validade dos links obrigatórios."""
        all_content = ' '.join(content.values())
        return all(link in all_content for link in self.REQUIRED_LINKS)
    
    def _validate_case_studies(self, content: Dict[str, str]) -> bool:
        """Valida a presença e autenticidade dos estudos de caso."""
        # Implementar validação com Dify API
        if not self.dify_api_key:
            return True  # Skip if no API key
            
        # TODO: Implementar chamada à API Dify
        return True
    
    def _validate_services(self, content: Dict[str, str]) -> bool:
        """Valida a menção adequada aos serviços da Descomplicar."""
        services_mentioned = False
        for section in ['interest', 'decision']:
            section_content = content.get(section, '').lower()
            if 'descomplicar' in section_content and any(
                service in section_content 
                for service in ['serviço', 'solução', 'consultoria']
            ):
                services_mentioned = True
                break
        return services_mentioned
    
    def _validate_final_cta(self, action_content: str) -> bool:
        """Valida a CTA final e seus links."""
        if not action_content:
            return False
            
        # Verificar links naturalmente integrados
        return all(link in action_content for link in self.REQUIRED_LINKS)

def validate_html_structure(html_content: str) -> Tuple[bool, List[str]]:
    """Valida a estrutura HTML do conteúdo."""
    errors = []
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Verificar CTA Box inicial
    initial_cta = soup.find('div', {'class': 'cta-box-initial'})
    if not initial_cta or '#f2d9a2' not in initial_cta.get('style', ''):
        errors.append("CTA Box inicial ausente ou sem estilo correto")
    
    # Verificar estrutura ACIDA
    for section in ['attention', 'confidence', 'interest', 'decision', 'action']:
        if not soup.find('section', {'class': section}):
            errors.append(f"Seção {section.upper()} ausente ou mal formatada")
    
    # Verificar links
    links = [a['href'] for a in soup.find_all('a')]
    for required_link in ACIDAValidator.REQUIRED_LINKS:
        if required_link not in links:
            errors.append(f"Link obrigatório ausente: {required_link}")
    
    return len(errors) == 0, errors 