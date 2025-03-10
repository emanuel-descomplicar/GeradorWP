#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para depurar geração de HTML do artigo.

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

# Obter o HTML
html = article.to_html()

# Salvar o HTML em um arquivo
with open('debug/html_output.html', 'w', encoding='utf-8') as f:
    f.write(html)

# Verificar tópicos numerados
h3_tags = re.findall(r'<h3>(.*?)</h3>', html)
print(f"Total de tags H3 encontradas: {len(h3_tags)}")
print("Primeiras 5 tags H3:")
for i, tag in enumerate(h3_tags[:5]):
    print(f"{i+1}. {tag}")

# Verificar seções principais
sections = re.findall(r'<div class="article-section (.*?)"><h2>(.*?)</h2>', html)
print("\nSeções principais:")
for section_type, title in sections:
    print(f"- {section_type}: {title}")

print("\nAnálise completa. HTML salvo em debug/html_output.html") 