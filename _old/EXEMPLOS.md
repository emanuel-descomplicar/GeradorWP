# Exemplos de Uso do Gerador de Conteúdos

Este documento contém exemplos práticos de como utilizar o gerador de conteúdos para WordPress em diferentes cenários.

## Geração de Artigo Individual

### Exemplo Básico
Para gerar um artigo simples em modo rascunho:

```bash
python src/test_article.py --title "Estratégias de SEO para E-commerce em Portugal" --category "Marketing Digital" --status draft
```

### Com Tags
Para incluir tags no artigo:

```bash
python src/test_article.py --title "Como Criar uma Estratégia de Email Marketing Eficaz" --category "Marketing Digital" --status draft --tags "email-marketing,estrategia,portugal,marketing"
```

### Artigo Pronto para Publicação
Para gerar um artigo e publicá-lo imediatamente:

```bash
python src/test_article.py --title "Tendências de Marketing Digital para 2025" --category "Marketing Digital" --status publish --tags "tendencias,2025,marketing-digital,portugal"
```

### Apenas Geração Local
Para gerar o artigo sem publicar no WordPress:

```bash
python src/test_article.py --title "Guia de Redes Sociais para PMEs" --category "Redes Sociais" --apenas-local --tags "redes-sociais,pmes,facebook,instagram"
```

## Processamento em Lote

### Criação do Arquivo CSV
Crie um arquivo CSV com os artigos a serem gerados:

**artigos.csv**
```csv
titulo,categoria,tags
"Estratégias de SEO para E-commerce em Portugal","Marketing Digital","seo,ecommerce,portugal,marketing"
"Como Criar uma Estratégia de Email Marketing Eficaz","Marketing Digital","email-marketing,estrategia,portugal,marketing"
"Tendências de Marketing Digital para 2025","Marketing Digital","tendencias,2025,marketing-digital,portugal"
"Guia de Redes Sociais para PMEs","Redes Sociais","redes-sociais,pmes,facebook,instagram"
"Otimização de Conversão para Lojas Online","E-commerce","conversao,otimizacao,lojas-online,vendas"
```

### Processamento do Lote
Para processar todos os artigos do CSV:

```bash
python src/process_batch.py --input artigos.csv --status draft
```

### Processamento Parcial
Para processar apenas alguns artigos do lote:

```bash
python src/process_batch.py --input artigos.csv --status draft --start 2 --limit 3
```

## Verificação de Categorias

Para listar todas as categorias disponíveis no WordPress:

```bash
python list_categories.py
```

Exemplo de saída:
```
2025-03-03 15:22:46,910 - INFO - Encontradas 28 categorias:
2025-03-03 15:22:46,910 - INFO - ID: 66, Nome: AcceleratorX
2025-03-03 15:22:46,910 - INFO - ID: 74, Nome: Automação
2025-03-03 15:22:46,911 - INFO - ID: 14, Nome: Blog
2025-03-03 15:22:46,911 - INFO - ID: 64, Nome: Comunicação
2025-03-03 15:22:46,911 - INFO - ID: 368, Nome: E-commerce
2025-03-03 15:22:46,911 - INFO - ID: 375, Nome: Empreendedorismo
2025-03-03 15:22:46,911 - INFO - ID: 69, Nome: Essentials
2025-03-03 15:22:46,912 - INFO - ID: 63, Nome: Estratégia
2025-03-03 15:22:46,912 - INFO - ID: 13, Nome: formulários
2025-03-03 15:22:46,912 - INFO - ID: 374, Nome: Gestão de PMEs
2025-03-03 15:22:46,912 - INFO - ID: 372, Nome: Inteligência Artificial
2025-03-03 15:22:46,912 - INFO - ID: 67, Nome: Management
2025-03-03 15:22:46,912 - INFO - ID: 62, Nome: Marketing
2025-03-03 15:22:46,913 - INFO - ID: 68, Nome: Marketing
2025-03-03 15:22:46,913 - INFO - ID: 65, Nome: Marketing Digital
```

## Verificação de Posts

Para verificar os posts existentes no WordPress:

```bash
python check_posts.py
```

Exemplo de saída:
```
2025-03-03 15:08:49,485 - INFO - Cliente WordPress inicializado com URL: https://descomplicar.pt
2025-03-03 15:08:49,485 - INFO - Inicializando sessão para https://descomplicar.pt
2025-03-03 15:08:49,486 - INFO - Sessão inicializada com sucesso para https://descomplicar.pt
2025-03-03 15:08:49,486 - INFO - Conectado ao WordPress
2025-03-03 15:08:49,486 - INFO - Obtendo 5 posts com status draft
2025-03-03 15:08:50,914 - INFO - Encontrados 1 posts em rascunho:
2025-03-03 15:08:50,915 - INFO - ID: 51832, Título: Inteligência Artificial para Pequenas Empresas em Portugal
```

## Verificação de Conteúdo de Post

Para verificar o conteúdo de um post específico:

```bash
python check_post_content.py
```

Exemplo de saída:
```
2025-03-03 15:09:17,147 - INFO - Cliente WordPress inicializado com URL: https://descomplicar.pt
2025-03-03 15:09:17,147 - INFO - Inicializando sessão para https://descomplicar.pt
2025-03-03 15:09:17,147 - INFO - Sessão inicializada com sucesso para https://descomplicar.pt
2025-03-03 15:09:17,148 - INFO - Conectado ao WordPress
2025-03-03 15:09:17,148 - INFO - Obtendo post 51832
2025-03-03 15:09:18,472 - INFO - Post encontrado: Inteligência Artificial para Pequenas Empresas em Portugal
2025-03-03 15:09:18,474 - INFO - Conteúdo salvo em post_content.html
2025-03-03 15:09:18,477 - INFO - Data de criação: 2025-03-03T15:08:14
2025-03-03 15:09:18,477 - INFO - Status: draft
2025-03-03 15:09:18,477 - INFO - Link: https://descomplicar.pt/?p=51832
2025-03-03 15:09:18,478 - INFO - ID da imagem destacada: 51831
```

## Análise de Links

Para analisar os links em um artigo gerado:

```bash
# Verificar links internos
find . -name "artigo_Marketing_Digital_*.html" | sort -r | head -n 1 | xargs cat | grep -o '<a href="https://descomplicar.pt[^"]*"' | sort | uniq

# Verificar links externos
find . -name "artigo_Marketing_Digital_*.html" | sort -r | head -n 1 | xargs cat | grep -o '<a href="https://[^d][^"]*"' | sort | uniq
```

## Fluxo de Trabalho Completo

Um fluxo de trabalho completo para geração de conteúdo pode incluir:

1. Verificar categorias disponíveis:
```bash
python list_categories.py
```

2. Criar um arquivo CSV com os artigos a serem gerados:
```csv
titulo,categoria,tags
"Estratégias de SEO para E-commerce em Portugal","Marketing Digital","seo,ecommerce,portugal,marketing"
"Como Criar uma Estratégia de Email Marketing Eficaz","Marketing Digital","email-marketing,estrategia,portugal,marketing"
```

3. Gerar um artigo de teste para verificar a qualidade:
```bash
python src/test_article.py --title "Estratégias de SEO para E-commerce em Portugal" --category "Marketing Digital" --status draft --tags "seo,ecommerce,portugal,marketing"
```

4. Verificar o artigo gerado:
```bash
python check_posts.py
python check_post_content.py
```

5. Processar o lote completo:
```bash
python src/process_batch.py --input artigos.csv --status draft
```

6. Publicar os artigos após revisão:
```bash
# Atualizar o status dos artigos para "publish"
# (Implementar um script para isso ou fazer manualmente no WordPress)
```

## Dicas e Boas Práticas

1. **Títulos Eficazes**: Use títulos específicos e relevantes para o público português.
2. **Categorias Corretas**: Verifique sempre se a categoria existe antes de gerar o artigo.
3. **Tags Relevantes**: Use tags específicas e relevantes para melhorar a SEO.
4. **Revisão Manual**: Sempre revise os artigos antes de publicá-los.
5. **Imagens Personalizadas**: Considere substituir as imagens geradas por imagens personalizadas.
6. **Verificação de Links**: Verifique se os links internos e externos estão funcionando corretamente.
7. **Monitoramento de Desempenho**: Acompanhe o desempenho dos artigos publicados para ajustar a estratégia.

## Resolução de Problemas

### Erro de Categoria Não Encontrada
Se receber um erro de categoria não encontrada, verifique as categorias disponíveis:
```bash
python list_categories.py
```

### Erro de Conexão com WordPress
Verifique as credenciais no arquivo `.env` e certifique-se de que a API REST do WordPress está ativa.

### Erro na Geração de Conteúdo
Verifique os logs em `logs/` para identificar o problema específico.

### Artigo Muito Curto
Ajuste o prompt no arquivo `src/dify_client.py` para gerar conteúdo mais extenso.

### Links Internos Incorretos
Verifique a lista de links internos válidos no método `_get_section_prompts` do arquivo `src/dify_client.py`. 