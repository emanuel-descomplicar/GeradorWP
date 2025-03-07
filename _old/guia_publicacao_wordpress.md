# Guia de Publicação de Artigos no WordPress com Melhorias de Naturalidade

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */

## Introdução

Este guia explica como utilizar o script `publish_improved_article.py` para gerar e publicar artigos no WordPress com as melhorias de naturalidade implementadas. O script combina a geração de conteúdo natural e fluido com a publicação automática no WordPress, incluindo imagem destacada e otimização SEO.

## Pré-requisitos

Antes de utilizar o script, certifique-se de que:

1. O ambiente virtual Python está ativado: `source venv/bin/activate`
2. As credenciais do WordPress estão configuradas no arquivo `.env`
3. As credenciais da API Dify estão configuradas no arquivo `.env`
4. Os diretórios `output/published_articles` e `logs` existem

## Como Utilizar o Script

### Comando Básico

```bash
python src/publish_improved_article.py --title "Título do Artigo" --category "Categoria" --status draft
```

### Parâmetros Disponíveis

- `--title`: Título do artigo (obrigatório)
- `--category`: Categoria do artigo (padrão: "Marketing Digital")
- `--tags`: Tags do artigo separadas por vírgula (padrão: "Marketing Digital, PME, Estratégia, 2025")
- `--status`: Status da publicação (opções: draft, publish, pending; padrão: draft)
- `--output-dir`: Diretório de saída para o conteúdo gerado (padrão: "output/published_articles")

### Exemplos de Uso

1. **Publicar um artigo como rascunho:**

```bash
python src/publish_improved_article.py --title "Como Criar Conteúdo Natural e Envolvente para o Seu Blog em 2025" --category "Marketing Digital" --status draft
```

2. **Publicar um artigo com tags personalizadas:**

```bash
python src/publish_improved_article.py --title "Estratégias de SEO para E-commerce em 2025" --category "E-commerce" --tags "SEO, E-commerce, Vendas Online, Otimização" --status draft
```

3. **Publicar um artigo diretamente (sem revisão):**

```bash
python src/publish_improved_article.py --title "Tendências de Inteligência Artificial para PMEs em 2025" --category "Inteligência Artificial" --status publish
```

## O Que o Script Faz

O script `publish_improved_article.py` realiza as seguintes operações:

1. **Geração de Conteúdo:**
   - Gera um outline para o artigo
   - Cria conteúdo para cada seção do modelo ACIDA (Atenção, Confiança, Interesse, Decisão, Ação)
   - Garante que o conteúdo tenha pelo menos 2000 palavras
   - Aplica as melhorias de naturalidade em cada seção

2. **Geração de Recursos:**
   - Cria uma imagem destacada personalizada com o título e categoria
   - Gera uma meta descrição otimizada para SEO
   - Gera metadados para o plugin Rank Math SEO

3. **Publicação no WordPress:**
   - Verifica e obtém o ID da categoria
   - Verifica e cria tags se necessário
   - Cria o post com o conteúdo gerado
   - Faz upload da imagem destacada
   - Configura os metadados SEO

4. **Salvamento Local:**
   - Salva o outline em arquivo de texto
   - Salva o conteúdo gerado em arquivo JSON
   - Gera logs detalhados do processo

## Melhorias de Naturalidade Aplicadas

O script aplica as seguintes melhorias para tornar o texto mais natural e fluido:

### 1. Linguagem Conversacional
- Uso de expressões como "Imagine que...", "Considere o seguinte cenário..."
- Inclusão de perguntas retóricas distribuídas pelo texto
- Uso de frases como "É interessante notar que...", "Vale a pena mencionar..."

### 2. Fluidez e Ritmo
- Variação no comprimento das frases (curtas, médias e longas)
- Uso de conectores de transição entre parágrafos
- Criação de um ritmo natural com perguntas e respostas

### 3. Português Europeu Autêntico
- Uso de expressões idiomáticas portuguesas
- Referências a entidades e contextos portugueses
- Consistência no uso da 3ª pessoa

### 4. Estrutura Envolvente
- Início com factos surpreendentes ou estatísticas impactantes
- Inclusão de pequenas histórias ou cenários hipotéticos
- Adição de elementos de empatia e compreensão

## Verificação e Revisão

Após a publicação, recomendamos:

1. Aceder ao WordPress e verificar o artigo publicado
2. Revisar o conteúdo para garantir qualidade e precisão
3. Verificar a imagem destacada e os metadados SEO
4. Publicar o artigo quando estiver satisfeito com o resultado

## Resolução de Problemas

### Categoria não encontrada
Verifique se a categoria existe no WordPress e se está a usar o nome exato. As categorias de blog devem ter o prefixo "blog-" (ex: "blog-marketing-digital").

### Falha na geração de imagem destacada
Verifique se o diretório `templates` contém os templates de imagem necessários para a categoria especificada.

### Erro de conexão com o WordPress
Verifique as credenciais no arquivo `.env` e se o site WordPress está acessível.

### Erro na API Dify
Verifique as credenciais da API Dify no arquivo `.env` e se o serviço está disponível.

## Logs e Depuração

Os logs detalhados são salvos no diretório `logs` com o formato `publish_improved_article_YYYYMMDD_HHMMSS.log`. Consulte estes logs para obter informações detalhadas sobre o processo de geração e publicação.

## Conclusão

O script `publish_improved_article.py` simplifica o processo de geração e publicação de artigos no WordPress, garantindo que o conteúdo seja natural, fluido e otimizado para SEO. Utilize-o para criar artigos de alta qualidade com menos esforço e tempo. 