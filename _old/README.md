# Gerador de Conteúdos WordPress

## Autor
Descomplicar - Agência de Aceleração Digital  
https://descomplicar.pt

## Descrição
O Gerador de Conteúdos WordPress é uma ferramenta avançada para automatizar a criação e publicação de artigos de alta qualidade para blogs WordPress. Utilizando o modelo ACIDA (Atenção, Confiança, Interesse, Decisão, Ação), a ferramenta gera conteúdo otimizado para SEO, com imagens destacadas personalizadas e metadados completos.

## Funcionalidades

- **Geração de Conteúdo Estruturado**: Criação de artigos seguindo o modelo ACIDA para máximo impacto
- **Otimização SEO**: Integração com plugins Rank Math e Yoast SEO para metadados completos
- **Geração de Imagens Destacadas**: Criação automática de imagens com templates por categoria
- **Validação de Conteúdo**: Verificação automática de qualidade, links e contagem de palavras
- **Publicação Automática**: Integração direta com a API WordPress para publicação
- **Processamento em Lote**: Capacidade de processar múltiplos artigos em sequência
- **Categorização Inteligente**: Sistema avançado de correspondência de categorias
- **Tratamento de Erros**: Mecanismos robustos de recuperação e fallback
- **Logging Detalhado**: Informações completas sobre cada etapa do processo
- **Personalização por Categoria**: Templates e estilos específicos para cada categoria
- **Verificação de Brasileirismos**: Detecção e correção automática de termos brasileiros
- **Tratamento na 3ª Pessoa**: Garantia de uso consistente da 3ª pessoa em todo o conteúdo
- **Links Internos e Externos**: Adição automática de links relevantes ao conteúdo
- **Imagens Otimizadas**: Geração de imagens em formato WebP com compressão adequada
- **Cache de Imagens**: Sistema de cache para evitar regeneração desnecessária
- **Validação de Categorias**: Verificação e criação automática de categorias no WordPress
- **Suporte a Títulos Longos**: Algoritmo avançado para acomodar títulos extensos em imagens
- **Centralização Vertical**: Posicionamento dinâmico de texto em imagens
- **Metadados SEO Completos**: Configuração automática de focus keyword, meta description e title

## Requisitos

- Python 3.8 ou superior
- Biblioteca Pillow para manipulação de imagens
- Biblioteca Requests para comunicação com APIs
- Acesso à API WordPress com credenciais de administrador
- Diretório de templates com imagens por categoria
- Fontes instaladas (Montserrat-Bold.ttf)
- Variáveis de ambiente configuradas (.env)

## Instalação

1. Clone o repositório:
```bash
git clone https://github.com/descomplicar/gerador-conteudos-wp.git
cd gerador-conteudos-wp
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o arquivo .env com suas credenciais
```

5. Crie os diretórios necessários:
```bash
mkdir -p output/images templates fonts cache logs
```

6. Adicione as fontes necessárias:
```bash
# Copie a fonte Montserrat-Bold.ttf para o diretório fonts/
```

7. Adicione templates de imagens:
```bash
# Adicione imagens de template para cada categoria no diretório templates/
```

## Utilização

### Geração de Artigo Individual

```bash
python src/gerar_artigo.py --titulo "Título do Artigo" --categoria "Marketing Digital" --tags "marketing,digital,estratégia" --publicar
```

### Processamento em Lote

```bash
python src/processar_lote.py --arquivo data/input/artigos.csv --limite 5
```

### Teste de Publicação

```bash
python src/publish_test_article.py
```

## Estrutura do Projeto

```
gerador-conteudos-wp/
├── src/                    # Código-fonte principal
│   ├── core/               # Classes principais
│   │   ├── dify_client.py  # Cliente para API Dify
│   │   ├── wordpress_client.py  # Cliente para API WordPress
│   │   ├── content_validator.py  # Validador de conteúdo
│   │   └── image_generator.py  # Gerador de imagens
│   ├── gerar_artigo.py     # Script para geração individual
│   ├── processar_lote.py   # Script para processamento em lote
│   └── publish_test_article.py  # Script de teste
├── data/                   # Diretório para dados
│   └── input/              # Arquivos CSV de entrada
├── output/                 # Diretório para saída
│   └── images/             # Imagens geradas
├── templates/              # Templates de imagens
├── fonts/                  # Fontes para imagens
├── cache/                  # Cache de imagens
├── logs/                   # Logs de execução
└── docs/                   # Documentação
    ├── ACIDA.md            # Documentação do modelo ACIDA
    ├── prompt.md           # Documentação dos prompts
    └── CHANGELOG.md        # Registo de alterações
```

## Modelo ACIDA

O gerador utiliza o modelo ACIDA para estruturar o conteúdo:

1. **Atenção**: Captura a atenção do leitor com estatísticas impactantes e contexto relevante
2. **Confiança**: Estabelece credibilidade com dados, citações e estudos de mercado
3. **Interesse**: Desperta interesse com benefícios, casos de uso e exemplos práticos
4. **Decisão**: Ajuda na tomada de decisão com passos concretos e soluções práticas
5. **Ação**: Motiva à ação com conclusão persuasiva e call-to-action natural

Cada seção é otimizada para garantir um mínimo de 2000 palavras no total, com links internos e externos relevantes.

## Geração de Imagens

O sistema gera imagens destacadas personalizadas para cada artigo:

- Utiliza templates específicos por categoria
- Adiciona o título do artigo com posicionamento dinâmico
- Otimiza para web com formato WebP
- Implementa cache para evitar regeneração
- Suporta títulos longos com até 350 caracteres
- Ajusta automaticamente a posição vertical do texto

## Categorização

O sistema implementa um algoritmo avançado de correspondência de categorias:

- Busca exata por nome e slug
- Busca parcial por palavras-chave
- Verificação direta de IDs para categorias críticas
- Utiliza apenas categorias com prefixo "blog-"
- Cria categorias automaticamente quando necessário

## Melhorias Recentes

### Versão 1.0.4 (04-03-2025)
- Verificação direta para categoria "Marketing Digital" com ID 369
- Suporte para títulos mais longos nas imagens (até 350 caracteres)
- Algoritmo melhorado para centralização vertical do texto
- Redução do tamanho da fonte para melhor legibilidade
- Aumento do número máximo de linhas de texto de 5 para 6
- Correção de problemas com seleção incorreta de categoria

### Versão 1.0.3 (04-03-2025)
- Metadados avançados para o Rank Math SEO
- Algoritmo melhorado de busca de categorias
- Aumento do tamanho de texto permitido nas imagens
- Correção de problemas com texto truncado

## Contribuição

Para contribuir com o projeto:

1. Faça um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas alterações (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Licença

Este projeto é propriedade da Descomplicar - Agência de Aceleração Digital.
Todos os direitos reservados.

## Suporte

Para suporte, entre em contacto através de:
- Email: suporte@descomplicar.pt
- Website: https://descomplicar.pt/contacto/ 