# Implementação do Prompt Melhorado

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */

## Visão Geral

Este documento contém instruções para implementar o prompt melhorado no gerador de conteúdos WordPress. As melhorias visam garantir que o conteúdo gerado atenda a todos os requisitos de qualidade, incluindo o mínimo de 2000 palavras, links internos e externos, e estrutura ACIDA completa.

## Arquivos a Modificar

1. `src/core/dify_client.py`

## Modificações Necessárias

### 1. Adicionar Método para Verificar e Expandir Conteúdo

Adicionar o seguinte método à classe `DifyClient` em `src/core/dify_client.py`:

```python
async def ensure_minimum_word_count(self, sections: Dict[str, str], min_words: int = 2000) -> Dict[str, str]:
    """
    Verifica se o conteúdo gerado atinge o mínimo de palavras e expande se necessário.
    
    Args:
        sections: Dicionário com as seções do artigo
        min_words: Número mínimo de palavras (padrão: 2000)
        
    Returns:
        Dict[str, str]: Dicionário com as seções do artigo, possivelmente expandidas
    """
    # Verificar contagem de palavras total
    total_words = sum(len(section.split()) for section in sections.values())
    logger.info(f"Contagem total de palavras: {total_words}")
    
    # Se já atingiu o mínimo, retornar as seções como estão
    if total_words >= min_words:
        logger.info(f"Conteúdo já atinge o mínimo de {min_words} palavras ({total_words} palavras)")
        return sections
    
    # Se não atingir o mínimo, expandir as seções
    logger.info(f"Conteúdo gerado tem apenas {total_words} palavras. Expandindo para atingir mínimo de {min_words}...")
    
    # Primeiro, tentar expandir a seção de desenvolvimento
    words_needed = min_words - total_words
    
    # Adicionar instruções para expandir o conteúdo
    expand_prompt = f"""
    Expanda o conteúdo abaixo para adicionar aproximadamente {words_needed} palavras, mantendo a qualidade e relevância.
    
    Adicione mais:
    - Exemplos práticos
    - Dados estatísticos com fontes
    - Citações de especialistas
    - Casos de uso específicos para o contexto português
    - Detalhes sobre implementação
    - Benefícios adicionais
    - Considerações importantes
    
    Mantenha o estilo e tom consistentes com o conteúdo original.
    Garanta que o conteúdo expandido seja informativo e útil, não apenas texto de preenchimento.
    
    Conteúdo original:
    {sections['development']}
    """
    
    # Expandir a seção de desenvolvimento (geralmente a mais adequada para expansão)
    expanded_development = await self._generate_section('Expansão de Conteúdo', expand_prompt)
    sections['development'] = expanded_development
    
    # Verificar novamente a contagem de palavras
    total_words = sum(len(section.split()) for section in sections.values())
    logger.info(f"Nova contagem total de palavras após expansão: {total_words}")
    
    # Se ainda não atingir o mínimo, expandir a seção de benefícios
    if total_words < min_words:
        words_needed = min_words - total_words
        logger.info(f"Ainda faltam {words_needed} palavras. Expandindo a seção de benefícios...")
        
        expand_benefits_prompt = f"""
        Expanda o conteúdo abaixo para adicionar aproximadamente {words_needed} palavras, mantendo a qualidade e relevância.
        
        Adicione mais:
        - Benefícios tangíveis e mensuráveis
        - Exemplos de casos de sucesso
        - Estatísticas que comprovam os benefícios
        - Comparações com abordagens alternativas
        - Dicas de implementação
        
        Mantenha o estilo e tom consistentes com o conteúdo original.
        Garanta que o conteúdo expandido seja informativo e útil, não apenas texto de preenchimento.
        
        Conteúdo original:
        {sections['benefits']}
        """
        
        expanded_benefits = await self._generate_section('Expansão de Benefícios', expand_benefits_prompt)
        sections['benefits'] = expanded_benefits
        
        # Verificar novamente a contagem de palavras
        total_words = sum(len(section.split()) for section in sections.values())
        logger.info(f"Nova contagem total de palavras após expansão de benefícios: {total_words}")
    
    # Se ainda não atingir o mínimo, expandir a seção de FAQ
    if total_words < min_words:
        words_needed = min_words - total_words
        logger.info(f"Ainda faltam {words_needed} palavras. Expandindo a seção de FAQ...")
        
        expand_faq_prompt = f"""
        Expanda a seção de FAQ abaixo para adicionar aproximadamente {words_needed} palavras, mantendo a qualidade e relevância.
        
        Adicione:
        - Mais perguntas e respostas relevantes
        - Respostas mais detalhadas para as perguntas existentes
        - Exemplos práticos nas respostas
        - Links para recursos adicionais
        
        Mantenha o estilo e tom consistentes com o conteúdo original.
        Garanta que o conteúdo expandido seja informativo e útil, não apenas texto de preenchimento.
        
        Conteúdo original:
        {sections['faq']}
        """
        
        expanded_faq = await self._generate_section('Expansão de FAQ', expand_faq_prompt)
        sections['faq'] = expanded_faq
        
        # Verificar novamente a contagem de palavras
        total_words = sum(len(section.split()) for section in sections.values())
        logger.info(f"Nova contagem total de palavras após expansão de FAQ: {total_words}")
    
    # Registrar a contagem final de palavras
    logger.info(f"Contagem final de palavras no conteúdo ACIDA: {total_words}")
    
    return sections
```

### 2. Modificar o Método `generate_article_content`

Modificar o método `generate_article_content` para utilizar o método `ensure_minimum_word_count`:

```python
# Após gerar todas as seções
sections['introduction'] = await self._generate_section('Introdução', prompt)
sections['development'] = await self._generate_section('Desenvolvimento', prompt)
sections['benefits'] = await self._generate_section('Benefícios', prompt)
sections['faq'] = await self._generate_section('Perguntas Frequentes', prompt)
sections['cta'] = await self._generate_section('Conclusão e CTA', prompt)

# Verificar e expandir o conteúdo se necessário para atingir 2000 palavras
sections = await self.ensure_minimum_word_count(sections, 2000)

return sections
```

### 3. Atualizar o Método `_get_section_prompts`

Substituir o método `_get_section_prompts` pelo seguinte:

```python
def _get_section_prompts(self, section_name: str, base_prompt: str) -> str:
    """
    Retorna o prompt específico para cada secção.
    
    Args:
        section_name: Nome da secção
        base_prompt: Prompt base
        
    Returns:
        Prompt específico para a secção
    """
    # Prompt base para todas as secções
    section_prompts = {
        "Introdução": f"""{base_prompt}

Gere apenas a INTRODUÇÃO (seção ATENÇÃO do modelo ACIDA) do artigo, seguindo estas diretrizes específicas:

1. Comece com um título H1 otimizado para SEO que inclua a palavra-chave principal
2. Inicie com uma estatística impactante e verificável sobre o mercado português/europeu
3. Contextualize o problema ou oportunidade para empresas portuguesas
4. Apresente claramente o valor que o leitor obterá ao ler o artigo completo
5. Inclua pelo menos 1 link interno para uma página relevante da Descomplicar
6. Inclua pelo menos 1 link externo para uma fonte estatística confiável (INE, PORDATA, Eurostat)
7. Mantenha esta seção entre 300-400 palavras
8. Inclua a palavra-chave principal pelo menos 2 vezes de forma natural
9. Use português europeu (evite brasileirismos e use 3ª pessoa)
10. Termine com uma transição para a próxima seção

IMPORTANTE: Esta seção deve captar a atenção do leitor e estabelecer o tom para o resto do artigo. Seja impactante, relevante e baseado em dados verificáveis.
""",

        "Desenvolvimento": f"""{base_prompt}

Gere apenas a seção de DESENVOLVIMENTO (seção CONFIANÇA do modelo ACIDA) do artigo, seguindo estas diretrizes específicas:

1. Comece com um subtítulo H2 relevante que inclua a palavra-chave principal ou secundária
2. Inclua dados verificáveis de pelo menos 2 fontes oficiais diferentes
3. Cite pelo menos 1 estudo académico ou relatório de pesquisa recente
4. Faça referência a pelo menos 1 autor ou livro reconhecido na área
5. Analise tendências atuais no mercado português/europeu
6. Inclua pelo menos 1 lista com marcadores destacando pontos-chave
7. Adicione pelo menos 1 link interno para uma página de serviço relevante da Descomplicar
8. Adicione pelo menos 1 link externo para um relatório ou estudo citado (com atributo nofollow)
9. Mantenha esta seção entre 500-600 palavras
10. Use português europeu (evite brasileirismos e use 3ª pessoa)
11. Organize o conteúdo com subtítulos H3 para melhor estrutura

IMPORTANTE: Esta seção deve estabelecer credibilidade através de dados verificáveis, citações e análises baseadas em evidências. Seja detalhado, informativo e focado em fatos.
""",

        "Benefícios": f"""{base_prompt}

Gere apenas a seção de BENEFÍCIOS (seção INTERESSE do modelo ACIDA) do artigo, seguindo estas diretrizes específicas:

1. Comece com um subtítulo H2 relevante que inclua uma palavra-chave secundária
2. Inclua pelo menos 2-3 subtítulos H3 para organizar o conteúdo
3. Explique detalhadamente os conceitos fundamentais
4. Inclua pelo menos 1 exemplo prático aplicável a empresas portuguesas
5. Destaque benefícios tangíveis e mensuráveis
6. Adicione pelo menos 1 lista numerada com passos ou processos
7. Inclua pelo menos 1 link interno para um case study ou artigo relacionado da Descomplicar
8. Adicione pelo menos 1 link externo para um recurso educacional relevante (com atributo nofollow)
9. Mantenha esta seção entre 500-600 palavras
10. Use português europeu (evite brasileirismos e use 3ª pessoa)
11. Inclua pelo menos 1 citação ou referência a um especialista na área

IMPORTANTE: Esta seção deve despertar o interesse do leitor através de benefícios concretos, exemplos práticos e aplicações reais. Seja específico, relevante e focado em valor para o leitor.
""",

        "Perguntas Frequentes": f"""{base_prompt}

Gere apenas a seção de PERGUNTAS FREQUENTES (complemento à seção DECISÃO do modelo ACIDA) do artigo, seguindo estas diretrizes específicas:

1. Comece com um subtítulo H2 "Perguntas Frequentes sobre [Tema]"
2. Inclua 5-6 perguntas relevantes formatadas como H3
3. Forneça respostas concisas e informativas (50-100 palavras cada)
4. Inclua pelo menos 1 pergunta sobre custos, ROI ou implementação
5. Inclua pelo menos 1 pergunta comparativa ou diferenciadora
6. Adicione pelo menos 1 link interno em uma das respostas
7. Adicione pelo menos 1 link externo em uma das respostas (com atributo nofollow)
8. Mantenha esta seção entre 300-400 palavras
9. Use português europeu (evite brasileirismos e use 3ª pessoa)
10. Inclua a palavra-chave principal pelo menos 1 vez de forma natural

IMPORTANTE: Esta seção deve ajudar o leitor a tomar decisões informadas respondendo às dúvidas mais comuns. Seja claro, direto e focado em resolver problemas reais.
""",

        "Conclusão e CTA": f"""{base_prompt}

Gere apenas a CONCLUSÃO com CALL-TO-ACTION do artigo (seção AÇÃO do modelo ACIDA), seguindo estas diretrizes específicas:

1. Comece com um subtítulo H2 "Conclusão" ou similar
2. Resuma os principais pontos abordados no artigo
3. Reforce a importância do tema para empresas portuguesas
4. Mencione pelo menos uma estatística ou dado relevante
5. Faça referência a pelo menos um autor, livro ou estudo citado no artigo
6. Inclua a palavra-chave principal pelo menos uma vez
7. Adicione pelo menos 1 pergunta reflexiva para engajar o leitor
8. Inclua pelo menos 1 link interno para página de contacto ou pedido de orçamento
9. Adicione pelo menos 1 link externo para uma fonte adicional de aprendizagem (com atributo nofollow)
10. Mantenha esta seção entre 300-400 palavras (excluindo o box de CTA)
11. Use português europeu (evite brasileirismos e use 3ª pessoa)

12. IMPORTANTE: Adicione o box de CTA EXATAMENTE neste formato:

<div class="cta-box">
    <h3>Precisa de ajuda com [tema principal]?</h3>
    <p>A <a href="https://descomplicar.pt">Descomplicar</a> oferece serviços especializados em [tema relacionado] para empresas portuguesas. Os nossos especialistas podem ajudar a sua empresa a:</p>
    <ul>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
    </ul>
    <p><strong>Agende uma consulta gratuita</strong> e descubra como podemos ajudar a sua empresa a implementar [tema principal] com sucesso.</p>
    <div class="cta-buttons">
        <a href="https://descomplicar.pt/marcar-reuniao" class="btn btn-primary">Agendar Consulta Gratuita</a>
        <a href="https://descomplicar.pt/pedido-de-orcamento" class="btn btn-secondary">Solicitar Orçamento</a>
        <a href="https://descomplicar.pt/contacto" class="btn btn-secondary">Entrar em Contacto</a>
    </div>
</div>

ATENÇÃO: É ABSOLUTAMENTE ESSENCIAL que você inclua o box de CTA exatamente como mostrado acima, substituindo apenas as partes entre colchetes []. Não modifique a estrutura HTML ou os links.

Lembre-se: A conclusão deve reforçar o valor do conteúdo, resumir os pontos principais baseados em evidências e incentivar o leitor a tomar uma ação específica.
""",

        "cta": f"""{base_prompt}

Gere apenas a CONCLUSÃO com CALL-TO-ACTION do artigo (seção AÇÃO do modelo ACIDA), seguindo estas diretrizes específicas:

1. Comece com um subtítulo H2 "Conclusão" ou similar
2. Resuma os principais pontos abordados no artigo
3. Reforce a importância do tema para empresas portuguesas
4. Mencione pelo menos uma estatística ou dado relevante
5. Faça referência a pelo menos um autor, livro ou estudo citado no artigo
6. Inclua a palavra-chave principal pelo menos uma vez
7. Adicione pelo menos 1 pergunta reflexiva para engajar o leitor
8. Inclua pelo menos 1 link interno para página de contacto ou pedido de orçamento
9. Adicione pelo menos 1 link externo para uma fonte adicional de aprendizagem (com atributo nofollow)
10. Mantenha esta seção entre 300-400 palavras (excluindo o box de CTA)
11. Use português europeu (evite brasileirismos e use 3ª pessoa)

12. IMPORTANTE: Adicione o box de CTA EXATAMENTE neste formato:

<div class="cta-box">
    <h3>Precisa de ajuda com [tema principal]?</h3>
    <p>A <a href="https://descomplicar.pt">Descomplicar</a> oferece serviços especializados em [tema relacionado] para empresas portuguesas. Os nossos especialistas podem ajudar a sua empresa a:</p>
    <ul>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
        <li>[Benefício específico relacionado ao tema do artigo - seja detalhado e específico]</li>
    </ul>
    <p><strong>Agende uma consulta gratuita</strong> e descubra como podemos ajudar a sua empresa a implementar [tema principal] com sucesso.</p>
    <div class="cta-buttons">
        <a href="https://descomplicar.pt/marcar-reuniao" class="btn btn-primary">Agendar Consulta Gratuita</a>
        <a href="https://descomplicar.pt/pedido-de-orcamento" class="btn btn-secondary">Solicitar Orçamento</a>
        <a href="https://descomplicar.pt/contacto" class="btn btn-secondary">Entrar em Contacto</a>
    </div>
</div>

ATENÇÃO: É ABSOLUTAMENTE ESSENCIAL que você inclua o box de CTA exatamente como mostrado acima, substituindo apenas as partes entre colchetes []. Não modifique a estrutura HTML ou os links.

Lembre-se: A conclusão deve reforçar o valor do conteúdo, resumir os pontos principais baseados em evidências e incentivar o leitor a tomar uma ação específica.
"""
    }
    
    # Retornar prompt específico ou prompt base se a secção não for reconhecida
    return section_prompts.get(section_name, base_prompt)
```

## Benefícios das Modificações

1. **Garantia de Contagem Mínima de Palavras**:
   - O método `ensure_minimum_word_count` verifica se o conteúdo gerado atinge o mínimo de 2000 palavras
   - Se não atingir, expande automaticamente as seções mais adequadas para expansão

2. **Prompts Melhorados para Cada Seção**:
   - Instruções mais detalhadas para cada seção do modelo ACIDA
   - Requisitos específicos para links internos e externos
   - Diretrizes para uso de português europeu e evitar brasileirismos
   - Instruções para inclusão de dados verificáveis e citações

3. **Estrutura ACIDA Completa**:
   - Cada seção tem instruções específicas para garantir que siga o modelo ACIDA
   - Requisitos de contagem de palavras para cada seção
   - Instruções para inclusão de elementos específicos em cada seção

4. **Call-to-Action Explícito**:
   - Formato padronizado para o CTA
   - Instruções detalhadas para personalização do CTA para o tema do artigo

## Implementação

1. Abra o arquivo `src/core/dify_client.py`
2. Adicione o método `ensure_minimum_word_count` após o método `generate_article_content`
3. Modifique o método `generate_article_content` para utilizar o método `ensure_minimum_word_count`
4. Substitua o método `_get_section_prompts` pelo novo método
5. Teste a implementação gerando um artigo completo

## Testes Recomendados

1. Gerar um artigo com o título "Estratégias de Marketing Digital para PMEs em 2025"
2. Verificar se o conteúdo gerado atinge pelo menos 2000 palavras
3. Verificar se todas as seções do modelo ACIDA estão presentes
4. Verificar se há pelo menos 3 links internos e 3 links externos
5. Verificar se o CTA está formatado corretamente
6. Verificar se o conteúdo está em português europeu sem brasileirismos 