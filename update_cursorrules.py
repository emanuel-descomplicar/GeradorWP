#!/usr/bin/env python3
"""
Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os

def create_cursorrules():
    content = """# Project Configuration

## Project Details
- Name: GeradorWP
- Language: Python
- Framework: CrewAI
- Author: Descomplicar - Agência de Aceleração Digital
- Website: https://descomplicar.pt

## Code Style
- Indentation: 4 spaces
- Max line length: 120 characters
- Naming conventions:
  - Variables: camelCase
  - Classes: PascalCase
  - Constants: UPPER_SNAKE_CASE
  - Functions: snake_case

## File Patterns
- Python files: *.py
- Configuration files: *.yml, *.yaml, *.json
- Documentation: *.md
- Environment: .env
- Templates: *.png
- Fonts: *.ttf

## Ignore Patterns
- __pycache__/
- *.pyc
- .env
- venv/
- .git/
- .vscode/
- .idea/
- .cache/

## Auto-formatting
- Enabled for Python files
- Use black for formatting
- Use isort for import sorting

## Linting
- Enabled for Python files
- Use flake8 for linting
- Use mypy for type checking

## Testing
- Use pytest for testing
- Test files should be named test_*.py
- Test functions should be named test_*

## AI Assistant Features
- Code completion
- Code refactoring
- Documentation generation
- Bug detection
- Performance optimization

## Content Generation
- Temperature: 0.3
- Validação de fontes: obrigatória
- Citações: necessárias
- Foco: dados portugueses
- Estilo: formal e profissional
- SEO: otimizado para mercado português

## Image Generation
- Dimensões: 1920x1080
- Fonte principal: Montserrat Bold
- Fonte secundária: Montserrat Regular
- Tamanho título: 90px
- Tamanho categoria: 28px
- Logo: 200x50px
- Posição logo: (120, 60)
- Formato: WebP
- Qualidade: 90
- Método: 6
- Templates: PNG otimizados
- Categorias com cores Material Design
- Padrão de pontos: lado direito
- Overlay: 0.3 opacidade
- Gradiente: 0.4 opacidade

## WordPress Integration
- XML-RPC: ativado
- Categorias: mapeadas
- Featured Image: obrigatória
- SEO Yoast: integrado
- Validação: pré e pós publicação
- Status padrão: rascunho
- Retry mechanism: implementado

## Security
- RGPD compliant
- Validação de inputs/outputs
- Logs seguros
- Cache com TTL
- Backup automático
- Monitoramento ativo

# Implementation Status

## Fase 1: Configuração Base ✓
- [X] Ambiente de desenvolvimento
- [X] Estrutura de diretórios
- [X] Configuração de ferramentas
- [X] Documentação inicial

## Fase 2: Implementação dos Agentes ✓
- [X] ResearcherAgent
- [X] WriterAgent
- [X] PublisherAgent

## Fase 3: Sistema de Tarefas ✓
- [X] ResearchTask
- [X] WritingTask
- [X] PublishingTask

## Fase 4: Integração e Testes ✓
- [X] Testes unitários
- [X] Testes de integração
- [X] Testes de performance
- [X] Documentação final

## Current Focus
- Otimização de imagens
- Refinamento de templates
- Melhorias de performance
- Monitoramento de qualidade"""

    # Verifica se o arquivo existe e faz backup se necessário
    if os.path.exists('.cursorrules'):
        with open('.cursorrules', 'r', encoding='utf-8') as f:
            old_content = f.read()
        with open('.cursorrules.bak', 'w', encoding='utf-8') as f:
            f.write(old_content)
        print("✓ Backup do arquivo original criado como .cursorrules.bak")

    # Cria ou atualiza o arquivo .cursorrules
    with open('.cursorrules', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✓ Arquivo .cursorrules atualizado com sucesso")

if __name__ == '__main__':
    create_cursorrules() 