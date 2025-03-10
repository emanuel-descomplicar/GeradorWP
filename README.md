# GeradorWP

Gerador de conteúdo para WordPress com otimização SEO e geração de imagens.

## Autor
Descomplicar - Agência de Aceleração Digital  
https://descomplicar.pt

## Funcionalidades

- Geração de conteúdo estruturado no formato ACIDA
- Otimização SEO automática
- Geração de imagens destacadas personalizadas
- Publicação direta no WordPress
- Sistema de cache e logging
- Validações e tratamento de erros

## Estrutura do Projeto

```
src/              # Código principal
├── config/       # Configurações
│   ├── settings.py    # Configurações do projeto
│   └── templates.py   # Templates de prompts
├── utils/        # Utilitários
│   ├── wordpress.py   # Cliente WordPress
│   ├── image.py      # Gerador de imagens
│   ├── content.py    # Gerenciador de conteúdo
│   ├── seo.py        # Otimização SEO
│   ├── dify.py       # Cliente Dify
│   ├── exceptions.py # Exceções e validações
│   ├── logger.py     # Sistema de logging
│   └── cache.py      # Sistema de cache
└── main.py       # Ponto de entrada

tests/            # Testes
assets/           # Recursos estáticos
.cache/           # Cache
logs/             # Logs
backups/          # Backups
```

## Requisitos

- Python 3.10+
- WordPress com XML-RPC habilitado
- Chave de API Dify

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/descomplicar/geradorwp.git
cd geradorwp
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -e .
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Uso

1. Publicar um artigo:
```python
from src.utils.wordpress import WordPressClient
from src.utils.image import ImageGenerator
from src.utils.content import ContentManager
from src.utils.seo import SEOOptimizer

# Inicializar componentes
wp = WordPressClient()
image_gen = ImageGenerator()
content_manager = ContentManager()
seo = SEOOptimizer()

# Criar e publicar artigo
result = wp.create_post(
    title="Seu Título",
    content="Seu Conteúdo",
    status="draft",
    category="Sua Categoria",
    tags=["tag1", "tag2"]
)
```

## Desenvolvimento

1. Instale as dependências de desenvolvimento:
```bash
pip install -e ".[dev]"
```

2. Configure as ferramentas de qualidade:
```bash
# Formatar código
black src/ tests/

# Ordenar imports
isort src/ tests/

# Verificar tipos
mypy src/

# Executar testes
pytest
```

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.