# GeradorWP - Sistema de Geração de Conteúdo para WordPress

## Descrição
GeradorWP é um sistema automatizado para gerar conteúdo de alta qualidade e publicá-lo diretamente no WordPress. Utilizando a API Dify para geração de conteúdo e a API REST do WordPress para publicação, o sistema cria artigos completos seguindo o modelo ACIDA (Attention, Confidence, Interest, Decision, Action).

## Funcionalidades
- Geração de conteúdo com base em tópicos e categorias específicas
- Estruturação de artigos no formato ACIDA
- Validação da qualidade do conteúdo gerado
- Publicação direta no WordPress via API REST
- Suporte para imagens destacadas
- Formatação do conteúdo para blocos Gutenberg

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

- Python 3.9 ou superior
- Acesso à API Dify
- Site WordPress com REST API habilitada
- Credenciais de acesso ao WordPress (nome de utilizador e senha)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/GeradorWP.git
cd GeradorWP
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
   - Copie o arquivo `.env.example` para `.env`
   - Preencha as informações de API da Dify e credenciais do WordPress

## Utilização

### Configuração
Configure o arquivo `.env` com suas credenciais:
```
# API Keys da Dify
DIFY_API_KEY=sua_chave_dify
DIFY_BASE_URL=https://api.dify.ai/v1  # ou URL personalizada
DIFY_KNOWLEDGE_BASE_ID=default

# Credenciais do WordPress
WP_URL=https://seu-site.com
WP_USERNAME=seu_utilizador
WP_PASSWORD=sua_senha_segura
WP_POST_STATUS=draft  # draft, publish, pending

# Caminho para a imagem destacada (opcional)
WP_FEATURED_IMAGE_PATH=/caminho/para/imagem.jpg
```

### Geração de Conteúdo
Para gerar um artigo, execute:
```bash
python -m src.examples.generate_article
```

Este comando irá:
1. Gerar um artigo sobre o tópico configurado
2. Validar a qualidade do conteúdo
3. Salvar o artigo como HTML na pasta `output/`

Você pode personalizar o tópico e a categoria editando o arquivo `src/examples/generate_article.py`.

### Publicação no WordPress
Para publicar o artigo gerado no WordPress, execute:
```bash
python -m src.examples.publish_to_wordpress
```

Este comando irá:
1. Procurar o arquivo HTML mais recente na pasta `output/`
2. Extrair a categoria do nome do arquivo
3. Publicar o artigo no WordPress com o status configurado (padrão: rascunho)

## Fluxo Completo de Trabalho
1. Configure suas credenciais no arquivo `.env`
2. Edite o tópico e categoria em `src/examples/generate_article.py`
3. Execute `python -m src.examples.generate_article` para gerar o artigo
4. Verifique o HTML gerado na pasta `output/`
5. Execute `python -m src.examples.publish_to_wordpress` para publicar no WordPress
6. Acesse o painel do WordPress para revisar e publicar o artigo

## Personalização
### Categorias do WordPress
O sistema suporta as seguintes categorias:
- blog-e-commerce
- blog-empreendedorismo
- blog-gestao-pmes
- blog-inteligencia-artificial
- blog-marketing-digital
- blog-tecnologia
- blog-transformacao-digital
- blog-vendas

Você pode adicionar mais categorias editando o arquivo `src/config/content_config.py`.

### Métricas e Prompts
As métricas e estruturas de prompts podem ser personalizadas editando:
- `src/config/content_config.py` - Definições de categorias e métricas
- `src/generators/content_generator.py` - Estrutura dos prompts

## Solução de Problemas
### Problemas de Conexão com WordPress
- Verifique se a REST API está habilitada no seu WordPress
- Confirme se o utilizador tem permissões para criar posts
- Teste a conexão com `curl` ou Postman para verificar as credenciais

### Problemas com a Geração de Conteúdo
- Verifique se a API Key da Dify é válida
- Aumente o tempo de espera entre as chamadas de API
- Reduza o número de palavras solicitado em cada seção

## Autor
Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt

## Licença

MIT License - veja o arquivo [LICENSE](LICENSE) para mais detalhes.