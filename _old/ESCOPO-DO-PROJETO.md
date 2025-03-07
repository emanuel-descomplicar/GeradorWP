# Escopo do Projeto

## Nome do Projeto
Gerador de Conteúdos WordPress com Modelo ACIDA

## Objetivo do Projeto
Criar um sistema de geração automática de conteúdos otimizados para WordPress, utilizando o modelo ACIDA (Atenção, Confiança, Interesse, Decisão, Ação) para garantir artigos persuasivos e de alta qualidade. O sistema deve integrar-se com a API Dify para geração de texto e com o WordPress para publicação automática, incluindo geração de imagens destacadas e otimização SEO.

## Stack Tecnológica
- **Linguagem:** Python 3.8+
- **Integração de IA:** API Dify
- **CMS:** WordPress (via API REST)
- **SEO:** Rank Math
- **Processamento de Imagens:** Pillow, API de imagens
- **Processamento Assíncrono:** asyncio, aiohttp
- **Configuração:** python-dotenv
- **Validação:** Regex, HTML/XML parsing
- **Logging:** Biblioteca logging do Python

## Responsáveis
- Desenvolvimento: Equipe de Desenvolvimento da Descomplicar
- Gestão de Projeto: Coordenação de Projetos Digitais
- Produção de Conteúdo: Departamento de Marketing de Conteúdo

## Cronograma
- **Fase 1 (Completa):** Implementação da integração com APIs (Dify e WordPress)
- **Fase 2 (Completa):** Desenvolvimento do modelo ACIDA e validação de conteúdo
- **Fase 3 (Completa):** Geração e otimização de imagens destacadas
- **Fase 4 (Completa):** Processamento em lote e reporting
- **Fase 5 (Completa):** Testes e otimizações finais

## Requisitos Técnicos
- **Formato:** Artigos em HTML com estrutura ACIDA completa
- **Volume:** Capacidade para gerar e publicar múltiplos artigos por lote
- **Extensão:** Mínimo de 2000 palavras por artigo
- **SEO:** Integração com Rank Math, otimização de keywords e metadados
- **Imagens:** Geração de imagens destacadas otimizadas
- **Links:** Validação automática de links internos e externos
- **Linguagem:** Português de Portugal (sem brasileirismos)
- **Tratamento:** Uso consistente da 3ª pessoa

## Recursos Implementados
1. **Geração de Conteúdo**
   - Implementação de modelo ACIDA completo (Atenção, Confiança, Interesse, Decisão, Ação, FAQ)
   - Prompts otimizados para geração de cada seção
   - Validação automática de qualidade e estrutura

2. **Otimização SEO**
   - Integração com Rank Math
   - Geração de meta descrições e focus keywords
   - Densidade de palavras-chave otimizada

3. **Imagens**
   - Geração de imagens destacadas baseadas no título e categoria
   - Upload e associação automática ao WordPress

4. **Validação e Correção**
   - Detecção e correção de brasileirismos
   - Verificação de tratamento na 3ª pessoa
   - Validação de links internos e externos
   - Análise de estrutura ACIDA

5. **Processamento**
   - Geração individual via CLI
   - Processamento em lote via CSV
   - Logging detalhado de execução

## Notas Adicionais
- O sistema foi projetado com modularidade para fácil manutenção e expansão
- A estrutura de código segue boas práticas com diretório core/ para componentes principais
- Implementação robusta de tratamento de erros e exceções
- Documentação completa com README, GUIA-RAPIDO e comentários no código 