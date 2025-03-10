#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para depurar a extração de tópicos numerados.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import sys
import os
from pathlib import Path
import re

# Adicionar diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generators.content_generator import ContentGenerator
from src.integrations.dify_client import DifyClient

# Inicializar o gerador de conteúdo
dify_client = DifyClient()
content_generator = ContentGenerator(dify_client)

# Gerar o artigo
article = content_generator.generate_article('Marketing Digital para Pequenas Empresas', 'blog-marketing-digital')

# Verificar o conteúdo das seções de interesse e decisão
interest_content = article.sections.get('interest', '')
decision_content = article.sections.get('decision', '')

print('======= CONTEÚDO BRUTO DA SEÇÃO DE INTERESSE =======')
print(interest_content[:2000])
print('\n')

print('======= CONTEÚDO BRUTO DA SEÇÃO DE DECISÃO =======')
print(decision_content[:2000])
print('\n')

# Definir padrões para identificar tópicos numerados
patterns = [
    r'<strong>(\d+)[\.:\)]?\s+(.*?)</strong>',  # <strong>1. Título</strong>
    r'<b>(\d+)[\.:\)]?\s+(.*?)</b>',            # <b>1. Título</b>
    r'<p>(\d+)[\.:\)]?\s+(.*?)</p>',            # <p>1. Título</p>
    r'<h3>(\d+)[\.:\)]?\s+(.*?)</h3>'           # <h3>1. Título</h3>
]

# Tentar extrair tópicos numerados da seção de interesse
print('======= TÓPICOS NUMERADOS NA SEÇÃO DE INTERESSE =======')
interest_topics = []
for pattern in patterns:
    matches = re.finditer(pattern, interest_content)
    for match in matches:
        num = match.group(1)
        title = match.group(2).strip()
        interest_topics.append((int(num), title))
        print(f"Encontrado com padrão '{pattern}': {num}. {title}")

# Tentar extrair tópicos numerados da seção de decisão
print('\n======= TÓPICOS NUMERADOS NA SEÇÃO DE DECISÃO =======')
decision_topics = []
for pattern in patterns:
    matches = re.finditer(pattern, decision_content)
    for match in matches:
        num = match.group(1)
        title = match.group(2).strip()
        decision_topics.append((int(num), title))
        print(f"Encontrado com padrão '{pattern}': {num}. {title}")

print('\n======= RESUMO =======')
print(f"Total de tópicos numerados na seção de interesse: {len(interest_topics)}")
print(f"Total de tópicos numerados na seção de decisão: {len(decision_topics)}")

# Verificar se o HTML gerado tem os tópicos
html = article.to_html()
h3_tags = re.findall(r'<h3>(\d+\.\s+.*?)</h3>', html)
print(f"\nTotal de tags H3 numeradas no HTML final: {len(h3_tags)}")
if h3_tags:
    print("Primeiras 3 tags H3:")
    for i, tag in enumerate(h3_tags[:3]):
        print(f"  {i+1}. {tag}") 