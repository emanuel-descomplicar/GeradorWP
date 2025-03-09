"""
Prompts - Templates de prompts para os agentes

Este módulo contém os templates de prompts utilizados pelos agentes do sistema,
facilitando a centralização e manutenção dos mesmos.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
from pathlib import Path
from typing import Dict, Any

# Caminho para o diretório de prompts
PROMPTS_DIR = Path(os.path.dirname(os.path.abspath(__file__))) / '..' / 'prompts'

# Prompts para o ResearcherAgent
RESEARCH_PROMPTS = {
    "search_topic": """
    Realiza uma pesquisa completa sobre o tópico: {topic}.
    
    Foca nos seguintes aspectos:
    - Definição e conceitos-chave
    - Estatísticas e factos relevantes para o mercado português
    - Tendências atuais em Portugal
    - Desafios e oportunidades
    - Melhores práticas
    - Exemplos de casos de sucesso
    
    Palavras-chave relacionadas:
    {keywords}
    
    Mantém o foco no contexto português e europeu, privilegiando exemplos e estatísticas locais.
    Valoriza fontes credíveis e atualizadas.
    """,
    
    "analyze_sources": """
    Analisa as seguintes fontes de informação sobre o tópico {topic}:
    
    {sources}
    
    Para cada fonte, extrai:
    1. Principais factos e estatísticas
    2. Argumentos e insights relevantes
    3. Exemplos e casos práticos
    4. Credibilidade da fonte (alta, média, baixa)
    
    Organiza a informação por relevância e credibilidade.
    Identifica contradições ou informações inconsistentes entre as fontes.
    """
}

# Prompts para o WriterAgent
WRITING_PROMPTS = {
    "create_outline": """
    Cria uma estrutura ACIDA detalhada para um artigo sobre {topic}.
    
    O artigo deve seguir esta estrutura:
    
    1. ATTENTION (Atenção) - 250 palavras
    - Estatística impactante sobre {topic} em Portugal
    - Contexto atual do mercado português
    - Pergunta retórica que desperte o interesse
    
    2. CONFIDENCE (Confiança) - 450 palavras
    - Dados e fontes respeitáveis sobre {topic}
    - Citações de especialistas portugueses
    - Referências a instituições portuguesas
    
    3. INTEREST (Interesse) - 550 palavras
    - Benefícios tangíveis de {topic}
    - Exemplos práticos do mercado português
    - Casos de estudo relevantes
    
    4. DECISION (Decisão) - 450 palavras
    - Passos concretos para implementar {topic}
    - Recursos necessários
    - Considerações específicas para o mercado português
    
    5. ACTION (Ação) - 175 palavras
    - Conclusão persuasiva
    - Call-to-action claro
    - Próximos passos
    
    Usa os dados da pesquisa para fundamentar cada secção:
    {research_summary}
    
    Palavras-chave a incluir: {keywords}
    """,
    
    "generate_section": """
    Escreve a secção {section_name} (modelo ACIDA) do artigo sobre {topic}.
    
    Objetivo desta secção:
    {section_goal}
    
    Elementos a incluir:
    {section_elements}
    
    Número aproximado de palavras: {section_word_count}
    
    Dados relevantes da pesquisa:
    {section_research}
    
    Palavras-chave a incluir naturalmente: {keywords}
    
    Escreve no estilo:
    - Português de Portugal (não brasileiro)
    - Tom conversacional mas profissional
    - Frases diretas e de fácil compreensão
    - Parágrafos curtos (4-5 linhas máximo)
    - Escrita envolvente e persuasiva
    
    Formato: HTML com cabeçalhos apropriados (h2, h3) e formatação (strong, ul, ol) quando relevante.
    """
}

# Prompts para o PublisherAgent
PUBLISHING_PROMPTS = {
    "format_content": """
    Formata o seguinte conteúdo para publicação no WordPress:
    
    {content}
    
    Aplica estas otimizações:
    1. Verifica e corrige a estrutura HTML
    2. Adiciona cabeçalhos (h2, h3) de forma hierárquica
    3. Otimiza para leitura (parágrafos curtos, listas, destaques)
    4. Adiciona alt text em imagens
    5. Verifica links internos/externos
    6. Sugere pontos para adicionar imagens
    
    O resultado deve estar pronto para publicação no WordPress, seguindo as melhores práticas de SEO.
    """,
    
    "prepare_seo_meta": """
    Prepara os metadados SEO para o seguinte artigo sobre {topic}:
    
    Título: {title}
    Resumo: {excerpt}
    
    Gera:
    1. Meta description otimizada (150-160 caracteres)
    2. Slug URL (em português, sem acentos)
    3. Focus keyword principal
    4. 5-8 tags relevantes (em português)
    5. Título SEO otimizado (se diferente do título original)
    
    Considera estas palavras-chave:
    {keywords}
    """
}

def load_prompt_from_file(filename: str) -> str:
    """
    Carrega um prompt de um arquivo.
    
    Args:
        filename: Nome do arquivo (com extensão) no diretório de prompts
        
    Returns:
        Conteúdo do arquivo como string
    """
    try:
        prompt_path = PROMPTS_DIR / filename
        if not prompt_path.exists():
            return ""
        
        with open(prompt_path, 'r', encoding='utf-8') as f:
            return f.read()
            
    except Exception as e:
        print(f"Erro ao carregar prompt de {filename}: {str(e)}")
        return ""

# Carrega prompts de arquivos, se disponíveis
CONTENT_GENERATION_PROMPT = load_prompt_from_file("content_generation_prompt.md")

def get_prompt(prompt_key: str, prompt_vars: Dict[str, Any] = None) -> str:
    """
    Obtém um prompt por chave e formata com variáveis.
    
    Args:
        prompt_key: Chave do prompt (ex: "research.search_topic")
        prompt_vars: Variáveis para formatação do prompt
        
    Returns:
        Prompt formatado
    """
    prompt_vars = prompt_vars or {}
    
    # Resolver caminho da chave (ex: "research.search_topic" -> RESEARCH_PROMPTS["search_topic"])
    parts = prompt_key.split('.')
    
    if len(parts) == 1:
        # Prompt direto (ex: "CONTENT_GENERATION_PROMPT")
        prompt_template = globals().get(prompt_key, "")
    elif len(parts) == 2:
        # Prompt em dicionário (ex: "research.search_topic")
        category, key = parts
        prompts_dict = globals().get(f"{category.upper()}_PROMPTS", {})
        prompt_template = prompts_dict.get(key, "")
    else:
        prompt_template = ""
    
    # Se encontrou o template, formatar com as variáveis
    if prompt_template and prompt_vars:
        try:
            return prompt_template.format(**prompt_vars)
        except KeyError as e:
            print(f"Erro ao formatar prompt, variável em falta: {str(e)}")
            return prompt_template
    
    return prompt_template 