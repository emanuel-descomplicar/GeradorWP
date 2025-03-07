# Guia Rápido - Gerador de Conteúdos WordPress

## Autor
Descomplicar - Agência de Aceleração Digital  
https://descomplicar.pt

## Introdução

Este guia rápido fornece instruções passo a passo para utilizar o Gerador de Conteúdos WordPress. A ferramenta automatiza a criação e publicação de artigos de alta qualidade, otimizados para SEO, com imagens destacadas personalizadas e metadados completos.

## Configuração Inicial

1. **Configurar Variáveis de Ambiente**
   - Copie o ficheiro `.env.example` para `.env`
   - Preencha as seguintes variáveis:
     ```
     WP_URL=https://seu-site-wordpress.com
     WP_USERNAME=seu_usuario
     WP_APP_PASSWORD=sua_senha_de_aplicacao
     DIFY_API_KEY=sua_chave_api_dify
     DIFY_API_URL=https://api.dify.ai/v1
     ```

2. **Verificar Diretórios**
   - Certifique-se de que os seguintes diretórios existem:
     ```
     templates/       # Templates de imagens por categoria
     fonts/           # Fontes para texto nas imagens
     cache/           # Cache de imagens geradas
     output/images/   # Diretório para imagens geradas
     data/input/      # Arquivos CSV para processamento em lote
     logs/            # Logs de execução
     ```

3. **Verificar Templates e Fontes**
   - Adicione os templates de imagem para cada categoria em `templates/`
   - Certifique-se de que a fonte `Montserrat-Bold.ttf` está presente em `fonts/`

## Geração de Artigo Individual

Para gerar e publicar um único artigo:

```bash
python src/gerar_artigo.py --titulo "Título do Artigo" --categoria "Marketing Digital" --tags "marketing,digital,estratégia" [--publicar]
```

### Parâmetros:
- `--titulo`: Título do artigo (obrigatório)
- `--categoria`: Categoria do artigo (obrigatório)
- `--tags`: Tags separadas por vírgula (opcional)
- `--publicar`: Se presente, publica o artigo; caso contrário, salva como rascunho
- `--focus-keyword`: Palavra-chave principal para SEO (opcional)
- `--meta-description`: Descrição meta personalizada (opcional)
- `--output`: Caminho para salvar o artigo localmente (opcional)

## Processamento em Lote

Para processar múltiplos artigos a partir de um arquivo CSV:

```bash
python src/processar_lote.py --arquivo data/input/artigos.csv [--limite 5] [--publicar]
```

### Parâmetros:
- `--arquivo`: Caminho para o arquivo CSV com a lista de artigos (obrigatório)
- `--limite`: Número máximo de artigos a processar (opcional, padrão: todos)
- `--publicar`: Se presente, publica os artigos; caso contrário, salva como rascunho
- `--intervalo`: Intervalo em segundos entre processamentos (opcional, padrão: 5)

### Formato do CSV:
```csv
titulo,categoria,tags,focus_keyword
"Estratégias de Marketing Digital para 2025","Marketing Digital","marketing,digital,estratégia","marketing digital"
"Como Aumentar as Vendas do E-commerce","E-commerce","ecommerce,vendas,online","aumentar vendas ecommerce"
```

## Teste de Publicação

Para testar a publicação de um artigo de exemplo:

```bash
python src/publish_test_article.py
```

Este comando gera um artigo de teste sobre "Estratégias de Marketing Digital para Pequenas Empresas em 2025" e publica-o como rascunho no WordPress.

## Geração de Imagens

Para gerar apenas uma imagem destacada:

```bash
python src/image_generator.py "Título do Artigo" "Categoria"
```

### Exemplo:
```bash
python src/image_generator.py "Como Aumentar as Vendas do E-commerce em 2025" "E-commerce"
```

## Categorias Suportadas

O sistema suporta as seguintes categorias, cada uma com seu próprio template de imagem:

- Marketing Digital
- E-commerce
- Gestão de PMEs
- Inteligência Artificial
- Transformação Digital
- Vendas
- Empreendedorismo
- Tecnologia

**Importante**: Para artigos de blog, utilize apenas categorias com o prefixo "blog-" no WordPress. Por exemplo, "blog-marketing-digital".

## Estrutura do Conteúdo (Modelo ACIDA)

O conteúdo gerado segue o modelo ACIDA:

1. **Atenção** (200-300 palavras)
   - Estatística impactante
   - Facto surpreendente
   - Problema relevante
   - Contexto português

2. **Confiança** (400-500 palavras)
   - Dados estatísticos
   - Citações de especialistas
   - Estudos de mercado
   - Tendências atuais

3. **Interesse** (500-600 palavras)
   - Benefícios tangíveis
   - Casos de uso
   - Exemplos práticos
   - Histórias de sucesso

4. **Decisão** (400-500 palavras)
   - Passos de implementação
   - Recursos necessários
   - Desafios comuns
   - Soluções práticas

5. **Ação** (150-200 palavras)
   - Resumo dos pontos principais
   - Próximos passos
   - Call-to-action natural
   - Links para serviços relevantes

6. **FAQ** (300-400 palavras)
   - 5-6 perguntas relevantes
   - Pergunta sobre custos/ROI
   - Respostas detalhadas
   - Links para recursos adicionais

## Otimização SEO

O sistema configura automaticamente os seguintes metadados SEO:

### Rank Math SEO
- `rank_math_focus_keyword`: Palavra-chave principal
- `rank_math_title`: Título otimizado para SEO
- `rank_math_description`: Meta descrição otimizada

### Yoast SEO
- `_yoast_wpseo_focuskw`: Palavra-chave principal
- `_yoast_wpseo_title`: Título otimizado para SEO
- `_yoast_wpseo_metadesc`: Meta descrição otimizada

## Imagens Destacadas

As imagens destacadas são geradas com as seguintes características:

- **Formato**: WebP com qualidade 90%
- **Dimensões**: 1920x1080px
- **Texto**:
  - Fonte: Montserrat Bold (50px)
  - Cor: Preto (RGB: 0,0,0)
  - Largura máxima: 900px
  - Posição inicial: (100, 350)
  - Espaçamento: 6px entre linhas
  - Máximo de 6 linhas
  - Suporte para até 350 caracteres

## Resolução de Problemas

### Categoria não encontrada
- Verifique se está utilizando categorias com prefixo "blog-"
- Para a categoria "Marketing Digital", o sistema utiliza diretamente o ID 369

### Texto truncado nas imagens
- O sistema suporta até 350 caracteres e 6 linhas
- Títulos muito longos serão truncados com "..." no final

### Falha na publicação
- Verifique as credenciais no arquivo `.env`
- Confirme que o usuário tem permissões de administrador
- Verifique os logs em `logs/` para mais detalhes

### Imagem não gerada
- Verifique se os templates existem em `templates/`
- Confirme que a fonte Montserrat-Bold.ttf está em `fonts/`
- Verifique permissões de escrita nos diretórios `cache/` e `output/images/`

## Novas Funcionalidades (v1.0.4)

- **Verificação direta de categorias**: Uso direto do ID 369 para "Marketing Digital"
- **Suporte a títulos longos**: Até 350 caracteres nas imagens destacadas
- **Centralização vertical melhorada**: Posicionamento dinâmico baseado no número de linhas
- **Metadados SEO avançados**: Configuração completa para Rank Math e Yoast SEO
- **Algoritmo de quebra de texto aprimorado**: Evita truncamento inadequado
- **Logging detalhado**: Informações completas sobre cada etapa do processo

## Suporte

Para suporte, entre em contacto através de:
- Email: suporte@descomplicar.pt
- Website: https://descomplicar.pt/contacto/

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */ 