# Documentação da API

## Visão Geral

O GeradorWP é uma biblioteca Python que automatiza a geração e publicação de conteúdo no WordPress usando inteligência artificial. A biblioteca é composta por três agentes principais que trabalham em conjunto:

1. `ResearcherAgent`: Responsável por pesquisar e coletar informações
2. `WriterAgent`: Responsável por criar o conteúdo otimizado
3. `PublisherAgent`: Responsável por publicar no WordPress

## Instalação

```bash
pip install gerador-wp
```

## Configuração

A biblioteca requer algumas variáveis de ambiente para funcionar:

```env
# Configurações Dify
DIFY_API_KEY=sua_api_key
DIFY_API_URL=https://api.dify.ai/v1

# Configurações WordPress
WP_URL=https://seu-site.com
WP_USERNAME=seu_usuario
WP_PASSWORD=sua_senha
WP_APP_PASSWORD=sua_app_password
```

## Uso Básico

```python
from gerador_wp.agents import ResearcherAgent, WriterAgent, PublisherAgent

# Inicializa os agentes
researcher = ResearcherAgent()
writer = WriterAgent()
publisher = PublisherAgent()

# Define o tópico e palavras-chave
topic = "Marketing Digital"
keywords = ["seo", "marketing", "digital"]

# Fase 1: Pesquisa
research_data = researcher.research(topic, keywords)

# Fase 2: Escrita
content = writer.write(research_data, keywords)

# Fase 3: Publicação
result = publisher.publish(content, [])
```

## API de Referência

### ResearcherAgent

#### `research(topic: str, keywords: List[str]) -> Dict`

Realiza pesquisa completa sobre um tópico.

**Argumentos:**
- `topic`: Tópico principal para pesquisa
- `keywords`: Lista de palavras-chave relacionadas

**Retorno:**
```python
{
    "topic": str,
    "keywords": List[str],
    "web_results": Dict,
    "statistics": Dict,
    "related_content": List[Dict],
    "timestamp": str
}
```

### WriterAgent

#### `write(research_data: Dict, keywords: List[str]) -> Dict`

Cria conteúdo completo do artigo.

**Argumentos:**
- `research_data`: Dados da pesquisa
- `keywords`: Lista de palavras-chave para otimização

**Retorno:**
```python
{
    "titulo": str,
    "meta_description": str,
    "content": str,
    "excerpt": str,
    "keywords": List[str],
    "timestamp": str,
    "word_count": int,
    "reading_time": int
}
```

### PublisherAgent

#### `publish(content: Dict, media_files: List[str]) -> Dict`

Publica conteúdo no WordPress.

**Argumentos:**
- `content`: Conteúdo do artigo
- `media_files`: Lista de URLs de arquivos de mídia

**Retorno:**
```python
{
    "id": int,
    "title": str,
    "link": str,
    "status": str,
    "timestamp": str,
    "media_files": List[str]
}
```

## Utilitários

### Cache

```python
from gerador_wp.utils import Cache

cache = Cache()

# Armazena valor
cache.set("chave", {"valor": 123})

# Recupera valor
valor = cache.get("chave")

# Remove valor
cache.delete("chave")

# Limpa cache
cache.clear()
```

### Logger

```python
from gerador_wp.utils import Logger

logger = Logger(__name__)

# Registra mensagens
logger.info("Mensagem informativa")
logger.error("Mensagem de erro")
logger.debug("Mensagem de debug")

# Registra requisições
logger.log_request("GET", "https://api.exemplo.com", 200, 0.5)

# Registra erros
try:
    # código que pode gerar erro
    pass
except Exception as e:
    logger.log_error(e, "Contexto do erro")
```

### SEO

```python
from gerador_wp.utils import SEOOptimizer

seo = SEOOptimizer()

# Otimiza título
titulo = seo.optimize_title("Título Original", ["palavra-chave"])

# Otimiza meta description
desc = seo.optimize_meta_description("Conteúdo", ["palavra-chave"])

# Otimiza conteúdo
content = seo.optimize_content("Conteúdo", ["palavra-chave"])

# Gera slug
slug = seo.generate_slug("Título do Artigo")
```

### WordPress

```python
from gerador_wp.utils import WordPressClient

wp = WordPressClient()

# Cria post
post = wp.create_post(
    title="Título",
    content="Conteúdo",
    excerpt="Resumo",
    status="draft",
    category="Blog",
    tags=["tag1", "tag2"]
)

# Atualiza post
wp.update_post(
    post_id=123,
    title="Novo Título",
    content="Novo Conteúdo"
)

# Remove post
wp.delete_post(123)
```

### Imagens

```python
from gerador_wp.utils import ImageManager

image = ImageManager()

# Gera imagem
bytes = image.generate_image("Descrição da imagem")

# Faz download
bytes = image.download_image("https://exemplo.com/imagem.jpg")

# Otimiza imagem
bytes = image.optimize_image(image_bytes)

# Cria miniatura
bytes = image.create_thumbnail(image_bytes)
```

## Tratamento de Erros

A biblioteca define exceções personalizadas para cada tipo de erro:

```python
from gerador_wp.utils.exceptions import (
    ResearchError,
    WritingError,
    PublishingError,
    ValidationError,
    APIError
)

try:
    result = researcher.research(topic, keywords)
except ResearchError as e:
    print(f"Erro na pesquisa: {e}")
except WritingError as e:
    print(f"Erro na escrita: {e}")
except PublishingError as e:
    print(f"Erro na publicação: {e}")
```

## Exemplos

Veja a pasta `examples/` para exemplos completos de uso da biblioteca:

- `basic_usage.py`: Uso básico da biblioteca
- `custom_workflow.py`: Fluxo personalizado
- `error_handling.py`: Tratamento de erros
- `media_handling.py`: Gerenciamento de mídia
- `seo_optimization.py`: Otimização SEO avançada 