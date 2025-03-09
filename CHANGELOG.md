# Registo de Alterações

Todas as alterações notáveis neste projeto serão documentadas neste ficheiro.

## [1.2.0] - 09-03-2025

### Adicionado
- Nova estrutura de diretórios mais limpa e organizada
- Sistema de validação unificado em `exceptions.py`
- Templates de prompts em `config/templates.py`
- Documentação atualizada com a nova estrutura
- Configuração de desenvolvimento com ferramentas de qualidade

### Alterado
- Renomeado diretório `gerador_wp` para `src`
- Simplificado sistema removendo dependência do CrewAI
- Atualizado `setup.py` com configurações corretas
- Otimizado sistema de geração de imagens
- Melhorado sistema de cache e logging

### Removido
- Módulos obsoletos e duplicados
- Dependências não utilizadas
- Arquivos de backup e temporários
- Referências ao CrewAI e agentes

## [1.1.0] - 07-03-2025

### Adicionado
- Implementação inicial do sistema
- Cliente WordPress funcional
- Gerador de imagens destacadas
- Sistema de estruturação de conteúdo ACIDA
- Otimização SEO automática
- Sistema de cache e logging

### Alterado
- Primeira versão estável do projeto
- Estrutura base do código
- Configurações iniciais

### Removido
- Nada relevante

## [1.0.0] - 07-03-2023  
### Adicionado:  
- Versão inicial do sistema GeradorWP
- Scripts para geração e publicação de artigos (gerar_artigo.py, publicar_artigo.py)
- Integração básica com WordPress
- Estrutura inicial do projeto

## [0.3.0] - 08-03-2025  
### Adicionado:  
- Script para publicação direta de artigos no WordPress
- Artigo sobre "A Importância do Marketing Digital para Clínicas de Psicologia"
- Suporte a tags para melhor SEO
- Tratamento de erros na publicação

### Alterado:  
- Simplificação do processo de publicação
- Melhoria na formatação do conteúdo HTML
- Otimização do fluxo de trabalho

### Corrigido:  
- Problema com categorias hierárquicas no WordPress
- Tratamento de erros na API WordPress
- Formatação de conteúdo HTML

## [0.2.1] - 08-03-2024
### Alterado
- Ajustes no gerador de imagens:
  - Tamanho da letra reduzido de 65px para 55px
  - Margem superior reduzida de 500px para 350px
  - Largura máxima do texto aumentada de 800px para 1000px
- Otimização da estrutura de templates de imagens
- Melhorias na documentação do sistema

## [0.2.0] - 08-03-2024
### Adicionado
- Integração com Rank Math SEO
- Metadados SEO automáticos para cada artigo
- Verificação e atualização de categorias
- Sistema de logging melhorado
- Tratamento de erros aprimorado

### Alterado
- Estrutura da função create_post para melhor gestão de metadados
- Processo de categorização de artigos
- Formato de logging para mais detalhes

### Corrigido
- Problemas na atribuição de categorias
- Gestão de erros na publicação
- Verificação de status code nas respostas da API

## [0.1.0] - 07-03-2024
### Adicionado
- Implementação inicial do gerador de artigos
- Sistema de geração de imagens destacadas
- Integração com WordPress REST API
- Gestão de tags automática
- Sistema de cache de imagens

## [1.2.1] - 09-03-2025

### Alterado
- Ajustes no gerador de imagens:
  - Simplificação do processo usando template base pré-definido
  - Margem superior ajustada para 400px
  - Implementado formato de subtítulo "[Categoria]: [Título do Artigo]"
  - Refinamento do posicionamento dos elementos de texto
  - Otimização do processo de inserção de texto no template 

## [1.2.2] - 09-03-2025

### Adicionado
- Integração com API Dify para Base de Conhecimento especializada
- CTAs personalizadas no início e fim dos artigos
- Sistema de validação automática de conteúdo:
  - Contagem de palavras por seção ACIDA
  - Verificação de CTAs e links
  - Validação de estudos de caso
  - Relevância dos serviços sugeridos

### Alterado
- Melhorado template de artigos com:
  - CTA Box inicial com fundo #f2d9a2
  - Links para ação contextualizados
  - Integração natural de serviços Descomplicar
  - CTA Box final com links naturais
- Aprimorado sistema de validação de conteúdo 