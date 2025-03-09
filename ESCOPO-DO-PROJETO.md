# Escopo do Projeto

## Nome do Projeto
GeradorWP - Gerador de Conteúdo WordPress

## Objetivo do Projeto
Criar um sistema automatizado que utiliza CrewAI para gerar e publicar conteúdo de qualidade no WordPress, mantendo uma estrutura simples e eficiente, com foco em naturalidade e relevância para o mercado português.

## Stack Tecnológica
- Python 3.10+
- CrewAI para automação
- WordPress XML-RPC API
- OpenAI API para geração de conteúdo
- Playwright para web scraping
- DuckDuckGo Search para pesquisa
- BeautifulSoup4 para parsing HTML

## Responsáveis
Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt

## Cronograma
1. Fase 1: Configuração Base (1 dia)
   - Ambiente de desenvolvimento
   - Estrutura de diretórios
   - Configuração de dependências
   - Configuração de ferramentas de qualidade

2. Fase 2: Implementação Core (2 dias)
   - ResearcherAgent com pesquisa avançada
   - WriterAgent com modelo ACIDA
   - PublisherAgent com validações
   - Sistema de logging e monitoramento

3. Fase 3: Integração (1 dia)
   - Conexão com WordPress
   - Testes e validação
   - Documentação
   - Otimização de performance

## Requisitos Técnicos

### 1. Funcionalidades Essenciais
- Geração de conteúdo relevante e natural
- Otimização SEO avançada
- Publicação no WordPress com validações
- Sistema de logging e monitoramento
- Tratamento de erros robusto
- Cache de resultados de pesquisa
- Validação de qualidade do conteúdo

### 2. Estrutura do Projeto
```
src/
├── agents/
│   ├── researcher.py      # Pesquisa e coleta de informações
│   ├── writer.py         # Geração de conteúdo
│   └── publisher.py      # Publicação no WordPress
├── config/
│   ├── settings.py       # Configurações do projeto
│   └── prompts.py        # Prompts para os agentes
├── utils/
│   ├── wordpress.py      # Cliente WordPress
│   ├── validators.py     # Validações de conteúdo
│   ├── logger.py         # Sistema de logging
│   └── cache.py          # Sistema de cache
└── main.py               # Ponto de entrada
```

### 3. Fluxo de Trabalho
```
Tópico → Research → Write → Validate → Publish → WordPress
```

### 4. Modelo de Conteúdo ACIDA
- **Pre-Content CTA Box**
  - Fundo: #f2d9a2
  - Formato: "Se procura uma solução para [tema] a Descomplicar pode ajudar com:"
  - Lista de serviços relevantes personalizados
  - Links de ação:
    - https://descomplicar.pt/marcar-reuniao/
    - https://descomplicar.pt/pedido-de-orcamento/
    - https://descomplicar.pt/contacto/

- **Attention**: Capte a atenção (200-300 palavras)
  - Estatísticas impactantes
  - Contexto português
  - Perguntas retóricas
  - Estudos de caso reais validados

- **Confidence**: Estabeleça credibilidade (400-500 palavras)
  - Dados e fontes respeitáveis
  - Citações de especialistas
  - Referências a instituições portuguesas
  - Base de Conhecimento Dify

- **Interest**: Desperte interesse (500-600 palavras)
  - Benefícios tangíveis
  - Exemplos práticos
  - Casos de estudo reais
  - Serviços Descomplicar relevantes

- **Decision**: Ajude na tomada de decisão (400-500 palavras)
  - Passos concretos
  - Recursos necessários
  - Considerações específicas
  - Soluções Descomplicar aplicáveis

- **Action**: Motive à ação (150-200 palavras)
  - Conclusão persuasiva
  - CTA natural com links relevantes
  - Próximos passos
  - CTA Box final com links contextualizados

### 5. Requisitos de Qualidade
- Mínimo de 2000 palavras por artigo
- Validação automática de:
  - Contagem total de palavras
  - Contagem por seção ACIDA
  - Presença de CTAs e links
  - Relevância dos serviços sugeridos
- Integração com API Dify para:
  - Base de Conhecimento especializada
  - Validação de informações
  - Personalização de conteúdo
- Otimização SEO completa
- Links internos e externos relevantes
- Imagem destacada personalizada
- Metadados SEO otimizados
- Validação de naturalidade do texto
- Verificação de plágio

### 6. Validações e Verificações
- Verificação de categorias existentes
- Validação de tags
- Verificação de links quebrados
- Validação de imagens
- Verificação de metadados SEO
- Validação de estrutura ACIDA
- Verificação de CTAs e links
- Validação de estudos de caso
- Verificação de integração Dify
- Validação de serviços sugeridos
- Verificação de naturalidade do texto

## Lições Aprendidas e Melhorias

### 1. Naturalidade do Texto
- Implementar linguagem conversacional
- Garantir fluidez entre parágrafos
- Usar português europeu autêntico
- Incluir exemplos do mercado português
- Manter tom consistente

### 2. Estrutura e Organização
- Simplificar a arquitetura
- Centralizar configurações
- Melhorar tratamento de erros
- Implementar logging detalhado
- Adicionar sistema de cache

### 3. SEO e Otimização
- Implementar validação de keywords
- Garantir densidade adequada
- Otimizar metadados
- Validar links internos/externos
- Verificar estrutura HTML

### 4. Publicação WordPress
- Validar categorias antes da publicação
- Verificar tags existentes
- Garantir upload de imagens
- Configurar metadados SEO
- Implementar rollback em caso de erro

## Notas Adicionais
- Manter o foco em qualidade e relevância
- Evitar complexidade desnecessária
- Priorizar manutenibilidade
- Documentar decisões importantes
- Implementar testes automatizados
- Manter backup de conteúdo
- Monitorar performance 