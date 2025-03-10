#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script para verificar se a solução para os tópicos numerados funcionou.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import sys
import os
import re
from pathlib import Path

# Adicionar diretório pai ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.generators.content_generator import ContentGenerator
from src.integrations.dify_client import DifyClient

# Inicializar o gerador de conteúdo
dify_client = DifyClient()
content_generator = ContentGenerator(dify_client)

# Gerar o artigo
print("Gerando artigo de teste...")
article = content_generator.generate_article('Marketing Digital para Pequenas Empresas', 'blog-marketing-digital')

# Obter o HTML
html = article.to_html()
print("HTML gerado com sucesso!")

# Extrair e contar os tópicos numerados no conteúdo bruto
print("\n=== VERIFICAÇÃO DOS DADOS ORIGINAIS ===")
interest_raw = article.sections.get('interest', '')
decision_raw = article.sections.get('decision', '')

# Padrão para encontrar tópicos numerados no formato <h3>1. Título</h3>
h3_pattern = r'<h3>(\d+)[\.:\)]?\s+(.*?)</h3>'

interest_h3_topics = re.findall(h3_pattern, interest_raw)
decision_h3_topics = re.findall(h3_pattern, decision_raw)

print(f"Tópicos H3 na seção de interesse: {len(interest_h3_topics)}")
for num, title in interest_h3_topics[:3]:  # Mostrar apenas os 3 primeiros
    print(f"  - {num}. {title}")

print(f"\nTópicos H3 na seção de decisão: {len(decision_h3_topics)}")
for num, title in decision_h3_topics[:3]:  # Mostrar apenas os 3 primeiros
    print(f"  - {num}. {title}")

# Verificar o HTML final para ver se os tópicos são transformados em H3
print("\n=== VERIFICAÇÃO DO HTML FINAL ===")
h3_tags_final = re.findall(r'<h3>(\d+\.\s+.*?)</h3>', html)
print(f"Total de tags H3 numeradas no HTML final: {len(h3_tags_final)}")

if h3_tags_final:
    print("\nPrimeiras tags H3 do HTML final:")
    for i, tag in enumerate(h3_tags_final[:6]):  # Mostrar os 6 primeiros
        print(f"  {i+1}. {tag}")
else:
    print("PROBLEMA: Nenhuma tag H3 com tópico numerado encontrada no HTML final!")

# Salvar HTML completo para análise
with open('debug/final_html.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("\nHTML completo salvo em 'debug/final_html.html'")

# Analisar o que pode estar acontecendo
print("\n=== DIAGNÓSTICO ===")
if len(h3_tags_final) == 0 and (len(interest_h3_topics) > 0 or len(decision_h3_topics) > 0):
    print("ERRO: Os tópicos são encontrados no conteúdo bruto, mas não são convertidos para o HTML final.")
    print("Problema pode estar na função extract_topics ou na montagem do HTML na seção de interesse/decisão.")
    
    # Verificar as funções auxiliares
    # Extrair manualmente os tópicos
    print("\nTestando extração manual:")
    
    # Recreate the extract_topics function
    def extract_topics_test(content):
        """Recria a função de extração para teste"""
        topics = []
        patterns = [
            r'<strong>(\d+)[\.:\)]?\s+(.*?)</strong>',
            r'<b>(\d+)[\.:\)]?\s+(.*?)</b>',
            r'<p>(\d+)[\.:\)]?\s+(.*?)</p>',
            r'<h3>(\d+)[\.:\)]?\s+(.*?)</h3>'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                num = match.group(1)
                title = match.group(2).strip()
                topics.append((int(num), title))
                print(f"Encontrado com padrão '{pattern}': {num}. {title}")
        
        return sorted(topics)
    
    print("\nTestando extração na seção de interesse:")
    interest_topics = extract_topics_test(interest_raw)
    print(f"\nTotal extraído: {len(interest_topics)}")
    
    print("\nTestando extração na seção de decisão:")
    decision_topics = extract_topics_test(decision_raw)
    print(f"\nTotal extraído: {len(decision_topics)}")
elif len(h3_tags_final) > 0:
    print("SUCESSO! Os tópicos numerados estão agora sendo exibidos corretamente no HTML final.")
    print(f"Total de tópicos no conteúdo bruto: {len(interest_h3_topics) + len(decision_h3_topics)}")
    print(f"Total de tópicos no HTML final: {len(h3_tags_final)}")
else:
    print("Não foram encontrados tópicos numerados nem no conteúdo bruto nem no HTML final.")
    print("O artigo pode não ter sido gerado com tópicos numerados nesta execução.") 