# Modelo ACIDA para Geração de Conteúdo

## Introdução
O modelo ACIDA é uma estrutura avançada para criação de conteúdo persuasivo que visa maximizar o engajamento e a conversão. Este documento explica como o modelo ACIDA é implementado no gerador de conteúdos para WordPress.

## Estrutura ACIDA

### A - Atenção (200-300 palavras)
A primeira seção do artigo tem como objetivo capturar a atenção do leitor imediatamente.

**Características:**
- Abertura impactante com estatística ou facto surpreendente
- Apresentação clara do problema ou desafio
- Contextualização para o mercado português
- Introdução ao tema de forma envolvente
- Promessa de valor que será entregue no artigo

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "introduction":
        return f"""
        Escreva a introdução de um artigo sobre "{focus_keyword}".
        
        A introdução deve:
        1. Capturar a atenção do leitor com um facto surpreendente ou estatística impactante
        2. Apresentar o problema ou desafio que o artigo vai abordar
        3. Incluir pelo menos uma estatística relevante para o mercado português
        4. Contextualizar o tema para o público português
        5. Ter entre 200-300 palavras
        
        {general_instructions}
        """
```

### C - Confiança (400-500 palavras)
A segunda seção estabelece credibilidade e confiança através de dados, estatísticas e citações de especialistas.

**Características:**
- Fundamentação teórica sólida
- Dados estatísticos de fontes confiáveis
- Citações de especialistas reconhecidos
- Análise de tendências baseada em relatórios
- Exemplos de casos reais no contexto português

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "development":
        return f"""
        Escreva a seção de desenvolvimento teórico para um artigo sobre "{focus_keyword}".
        
        Esta seção deve:
        1. Fornecer fundamentação teórica sobre o tema
        2. Incluir dados estatísticos e análises de mercado
        3. Citar pelo menos um especialista ou estudo académico
        4. Apresentar tendências e casos reais no contexto português
        5. Ter entre 400-500 palavras
        
        {general_instructions}
        """
```

### I - Interesse (500-600 palavras)
A terceira seção desperta o interesse do leitor através de benefícios e aplicações práticas.

**Características:**
- Análise de conceitos fundamentais
- Explicação de diferentes abordagens e metodologias
- Exemplos práticos no contexto português
- Benefícios tangíveis e intangíveis
- Comparação de ferramentas ou técnicas
- Histórias de sucesso relevantes

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "benefits":
        return f"""
        Escreva a seção de benefícios e aplicações para um artigo sobre "{focus_keyword}".
        
        Esta seção deve:
        1. Analisar conceitos fundamentais relacionados ao tema
        2. Explicar diferentes abordagens e metodologias
        3. Fornecer exemplos práticos no contexto português
        4. Destacar benefícios tangíveis e intangíveis
        5. Comparar ferramentas ou técnicas relevantes
        6. Incluir pelo menos uma história de sucesso
        7. Ter entre 500-600 palavras
        
        {general_instructions}
        """
```

### D - Decisão (400-500 palavras)
A quarta seção ajuda o leitor a tomar uma decisão, fornecendo passos concretos para implementação.

**Características:**
- Passos práticos e acionáveis
- Soluções para desafios comuns
- Critérios de avaliação e recursos necessários
- Adaptações para diferentes perfis de empresas
- Recomendações de ferramentas e recursos

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "implementation":
        return f"""
        Escreva a seção de implementação prática para um artigo sobre "{focus_keyword}".
        
        Esta seção deve:
        1. Fornecer passos concretos para implementação
        2. Abordar desafios comuns e como superá-los
        3. Incluir critérios de avaliação e recursos necessários
        4. Sugerir adaptações para diferentes perfis de empresas
        5. Recomendar ferramentas ou recursos úteis
        6. Ter entre 400-500 palavras
        
        {general_instructions}
        """
```

### A - Ação (150-200 palavras)
A quinta seção motiva o leitor a agir, com uma conclusão persuasiva e call-to-action.

**Características:**
- Resumo dos principais pontos
- Reforço da importância do tema
- Próximos passos claros
- Call-to-action persuasivo e natural
- Incentivo para contactar a Descomplicar

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "conclusion":
        return f"""
        Escreva a conclusão para um artigo sobre "{focus_keyword}".
        
        Esta seção deve:
        1. Resumir os principais pontos abordados no artigo
        2. Reforçar a importância do tema para empresas portuguesas
        3. Sugerir próximos passos para o leitor
        4. Incluir uma call-to-action clara e persuasiva
        5. Ter entre 150-200 palavras
        
        IMPORTANTE: Inclua um parágrafo final persuasivo que integre naturalmente os links para ação, em vez de apresentá-los como uma lista. Por exemplo:
        
        <p>Para dar o próximo passo e melhorar a presença online da sua empresa, <a href="https://descomplicar.pt/marcar-reuniao" class="btn btn-primary">agende uma consulta gratuita</a> com os nossos especialistas. Prefere analisar opções específicas para o seu negócio? <a href="https://descomplicar.pt/pedido-de-orcamento" class="btn btn-secondary">Solicite um orçamento personalizado</a> ou <a href="https://descomplicar.pt/contacto" class="btn btn-secondary">entre em contacto</a> para esclarecer qualquer dúvida sobre os nossos serviços.</p>
        
        {general_instructions}
        """
```

### FAQ (300-400 palavras)
Além das seções ACIDA, o artigo inclui uma seção de Perguntas Frequentes para abordar dúvidas comuns.

**Características:**
- 5-6 perguntas relevantes sobre o tema
- Respostas detalhadas e informativas
- Abordagem de dúvidas comuns
- Inclusão de pergunta sobre custos ou ROI

**Implementação:**
```python
def _get_section_prompts(self, section_name: str, focus_keyword: str) -> str:
    # ...
    elif section_name == "faq":
        return f"""
        Escreva uma seção de Perguntas Frequentes (FAQ) para um artigo sobre "{focus_keyword}".
        
        Esta seção deve:
        1. Incluir 5-6 perguntas relevantes sobre o tema
        2. Fornecer respostas detalhadas e informativas
        3. Abordar dúvidas comuns do público-alvo
        4. Incluir pelo menos uma pergunta sobre custos ou ROI
        5. Ter entre 300-400 palavras no total
        
        {general_instructions}
        """
```

## Validação e Conformidade ACIDA

O sistema inclui um método `_ensure_acida_compliance` que verifica se o conteúdo gerado segue corretamente o modelo ACIDA:

```python
def _ensure_acida_compliance(self, sections: Dict[str, str]) -> Dict[str, str]:
    """
    Garante que o conteúdo gerado segue o modelo ACIDA.
    
    Args:
        sections: Dicionário com as seções do artigo
        
    Returns:
        Dicionário com as seções do artigo ajustadas
    """
    updated_sections = {}
    
    # Verificar e ajustar cada seção
    for section_name, content in sections.items():
        # Remover ocorrências de "você" e substituir por formas na 3ª pessoa
        content = self._remove_second_person(content)
        
        # Garantir que a seção tem o comprimento mínimo
        if section_name == "introduction" and len(content.split()) < 200:
            content = self._expand_section(content, "introduction", 250)
        elif section_name == "development" and len(content.split()) < 400:
            content = self._expand_section(content, "development", 450)
        elif section_name == "benefits" and len(content.split()) < 500:
            content = self._expand_section(content, "benefits", 550)
        elif section_name == "implementation" and len(content.split()) < 400:
            content = self._expand_section(content, "implementation", 450)
        elif section_name == "faq" and len(content.split()) < 300:
            content = self._expand_section(content, "faq", 350)
        elif section_name == "conclusion" and len(content.split()) < 150:
            content = self._expand_section(content, "conclusion", 175)
        
        # Adicionar a seção atualizada
        updated_sections[section_name] = content
    
    return updated_sections
```

## Características Adicionais

### Tratamento na 3ª Pessoa
Todo o conteúdo é gerado usando tratamento na 3ª pessoa, evitando o uso de "você" ou formas de tratamento na 2ª pessoa.

```python
def _remove_second_person(self, content: str) -> str:
    """
    Remove ocorrências de "você" e substitui por formas na 3ª pessoa.
    Também remove notas indesejáveis no final do artigo.
    
    Args:
        content: Conteúdo HTML
        
    Returns:
        Conteúdo HTML sem ocorrências de "você" e sem notas indesejáveis
    """
    # Substituições para remover "você" e formas na 2ª pessoa
    # ...
```

### Links Internos Validados
O sistema garante que apenas links internos válidos sejam incluídos no conteúdo.

```python
def _correct_internal_links(self, content: str) -> str:
    """
    Corrige links internos inventados no conteúdo.
    
    Args:
        content: Conteúdo HTML com links
        
    Returns:
        Conteúdo HTML com links internos corrigidos
    """
    # Lógica para corrigir links internos
    # ...
```

### Links Externos Diversificados
O sistema utiliza uma ampla variedade de fontes externas confiáveis para citação.

```python
# Lista de fontes externas diversificadas
external_sources = """
Diversifique os links externos, usando uma variedade de fontes confiáveis como:

### Estatísticas e Dados Oficiais
- INE (Instituto Nacional de Estatística): https://www.ine.pt
- PORDATA: https://www.pordata.pt
# ...
```

### Menção a Serviços Reais
O sistema menciona serviços reais da Descomplicar em vez de tecnologias fictícias.

```python
# Lista de serviços reais que podem ser mencionados
real_services = """
Serviços reais que pode mencionar (pelo menos 2):
- Estratégia de Marketing Digital (serviço de consultoria e implementação de estratégias de marketing)
- Descomplicar 360º (serviço completo de marketing digital e presença online)
# ...
```

## Conclusão

O modelo ACIDA implementado no gerador de conteúdos para WordPress permite a criação de artigos altamente persuasivos e otimizados para conversão. A estrutura ACIDA, combinada com as características adicionais como tratamento na 3ª pessoa, links validados e menção a serviços reais, resulta em conteúdo de alta qualidade que atende aos objetivos de marketing da Descomplicar. 