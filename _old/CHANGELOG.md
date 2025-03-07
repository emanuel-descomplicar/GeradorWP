# Registo de Alterações - Gerador de Conteúdos WordPress

Todas as alterações notáveis neste projeto serão documentadas neste ficheiro.

## [1.0.4] - 04-03-2025  
### Adicionado:  
- Verificação direta para usar a categoria "Marketing Digital" com ID 369
- Suporte para títulos mais longos nas imagens destacadas (até 350 caracteres)
- Algoritmo melhorado para centralização vertical do texto nas imagens

### Alterado:  
- Reduzido o tamanho da fonte nas imagens para melhor legibilidade
- Aumentado o número máximo de linhas de texto nas imagens de 5 para 6
- Ajustada a posição vertical do texto para melhor visualização
- Melhorado o algoritmo de quebra de texto para evitar truncamento

### Corrigido:  
- Problema de seleção incorreta de categoria (agora usa diretamente a categoria correta)
- Texto truncado nas imagens destacadas com títulos longos
- Posicionamento inadequado do texto em imagens com poucas linhas

## [1.0.3] - 04-03-2025  
### Adicionado:  
- Metadados avançados para o Rank Math SEO
- Algoritmo melhorado de busca de categorias com múltiplos métodos de correspondência
- Depuração detalhada das categorias disponíveis no WordPress

### Alterado:  
- Aumentado o tamanho de texto permitido nas imagens destacadas (dobro do original)
- Ajustado tamanho da fonte para acomodar mais texto nas imagens
- Método de wrapping de texto otimizado para títulos mais longos

### Corrigido:  
- Problema na seleção de categorias com falha na correspondência exata
- Texto truncado nas imagens destacadas
- Metadados do Rank Math não sendo adicionados corretamente

## [1.0.2] - 04-03-2025  
### Adicionado:  
- Integração com o módulo image_generator.py para usar templates específicos por categoria
- Mapeamento completo das categorias do WordPress por slug com prefixo blog-
- Sistema de fallback cascata para geração de imagens (tentativa em múltiplos níveis)

### Alterado:  
- Reestruturação da lógica de categorias para usar os IDs corretos das categorias do blog
- Melhoramento no sistema de importação de módulos com caminhos relativos e absolutos

### Corrigido:  
- Problema com geração de imagens que não estava a usar o image_generator.py
- Categorias incorretas (agora usando apenas categorias com prefixo blog-)
- Caminhos relativos de importação de módulos

## [1.0.1] - 04-03-2025  
### Adicionado:  
- Implementação de contagem de palavras para garantir mínimo de 2000 palavras em cada artigo
- Adição de seção de estudos de caso para aumentar o conteúdo
- Expansão da seção de FAQ com perguntas e respostas adicionais para tópicos relevantes
- Sistema de fallback para imagens com mecanismo de recuperação de falhas
- Adição de texto explicativo à imagem destacada

### Alterado:  
- Reorganização da estrutura de conteúdo ACIDA para incluir mais texto
- Otimização de prompts para acomodar o mínimo de palavras exigido
- Melhoria no controle de fluxo para geração de conteúdo

### Corrigido:  
- Problemas com imagens destacadas que não apareciam nos artigos publicados
- Contagem de palavras insuficiente nos artigos gerados
- Falhas na manipulação de erros durante a geração de imagens
- Integração inadequada do gerador de imagens com o fluxo de publicação

## [1.0.0] - 04-03-2025  
### Adicionado:  
- Sistema completo de geração de conteúdo com modelo ACIDA
- Implementação de cliente Dify otimizado para prompts estruturados
- Validador de conteúdo para garantir qualidade dos artigos
- Scripts para geração individual e em lote de artigos
- Estrutura modular com diretório core para componentes principais
- Validação automática de conteúdo para SEO, gramática e estrutura
- Suporte a geração e otimização de imagens destacadas
- Integração completa com WordPress e Rank Math para SEO
- Detecção e correção automática de brasileirismos 
- Validação e correção de tratamento na 3ª pessoa
- Documentação detalhada com README e guia rápido atualizados

### Alterado:  
- Reorganização da estrutura de código para módulos específicos
- Otimização dos prompts para melhor qualidade de conteúdo
- Melhorias no tratamento de erros e sessões HTTP
- Atualização da integração com API WordPress
- Correção de problemas com chamadas de métodos inconsistentes

### Corrigido:  
- Incompatibilidade entre assinaturas de métodos na integração com Dify
- Vazamentos de recursos em sessões HTTP não fechadas corretamente
- Problemas com links internos e externos nos artigos gerados
- Tratamento incorreto de erros em integrações com APIs externas
- Problemas com geração de conteúdo sem estrutura ACIDA consistente 