# GeradorWP - Gerador de Conteúdo WordPress

Sistema automatizado para geração e publicação de conteúdo de alta qualidade no WordPress, utilizando CrewAI e o modelo ACIDA.

## Sobre o Projeto

O GeradorWP utiliza uma arquitetura baseada em agentes para pesquisar, escrever e publicar conteúdo de forma eficiente e com alta qualidade. O sistema é especialmente focado no mercado português, utilizando português europeu autêntico e referências locais relevantes.

### Modelo ACIDA

Todo o conteúdo gerado segue o modelo ACIDA:
- **Attention**: Capte a atenção (200-300 palavras)
- **Confidence**: Estabeleça credibilidade (400-500 palavras)
- **Interest**: Desperte interesse (500-600 palavras)
- **Decision**: Ajude na tomada de decisão (400-500 palavras)
- **Action**: Motive à ação (150-200 palavras)

## Requisitos

- Python 3.10+
- WordPress com acesso XML-RPC
- API Keys para serviços (OpenAI, DifyAI, etc.)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/descomplicar/geradorwp.git
   cd geradorwp
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o arquivo .env:
   ```bash
   cp .env.example .env
   # Edite o arquivo .env com suas credenciais
   ```

## Arquitetura

O sistema segue uma arquitetura modular baseada em agentes:

```
src/
├── agents/                # Agentes de IA
│   ├── researcher_agent.py   # Pesquisa e coleta de informações
│   ├── writer_agent.py       # Geração de conteúdo usando modelo ACIDA
│   └── publisher_agent.py    # Publicação no WordPress
├── tasks/                 # Tarefas definidas para os agentes
│   ├── research_task.py      # Definição de tarefas de pesquisa
│   ├── writing_task.py       # Definição de tarefas de escrita
│   └── publishing_task.py    # Definição de tarefas de publicação
├── utils/                 # Utilitários e helpers
│   ├── wordpress.py          # Cliente WordPress
│   ├── logger.py             # Sistema de logging
│   └── cache.py              # Sistema de cache
├── config/                # Configurações do sistema
│   ├── settings.py           # Gerenciamento de configurações
│   └── prompts.py            # Templates de prompts para os agentes
├── prompts/               # Arquivos de prompts extensos
└── main.py                # Ponto de entrada do sistema
```

## Uso

### Processando um único tópico

```bash
python -m src.main single --topic "Marketing Digital para Clínicas" --keywords "marketing,clínicas,estratégia" --category "Marketing" --status draft
```

### Processando múltiplos tópicos de um arquivo

```bash
python -m src.main file --file topicos.json --status draft
```

### Formato do arquivo de tópicos (JSON)

```json
[
  {
    "topic": "Marketing Digital para Clínicas",
    "keywords": ["marketing", "clínicas", "estratégia"],
    "category": "Marketing"
  },
  {
    "topic": "SEO para E-commerce",
    "keywords": ["seo", "e-commerce", "vendas online"],
    "category": "SEO"
  }
]
```

### Formato do arquivo de tópicos (CSV)

```csv
topic,keywords,category
"Marketing Digital para Clínicas","marketing,clínicas,estratégia",Marketing
"SEO para E-commerce","seo,e-commerce,vendas online",SEO
```

## Configuração

O sistema pode ser configurado através de:

1. Variáveis de ambiente (arquivo .env)
2. Arquivo de configuração (JSON ou YAML)
3. Argumentos de linha de comando

Exemplo de arquivo de configuração:

```json
{
  "content": {
    "min_word_count": 2500,
    "max_word_count": 3500,
    "use_acida_model": true
  },
  "publishing": {
    "default_status": "draft",
    "verify_after_publish": true
  }
}
```

## Desenvolvimento

Para contribuir com o projeto:

1. Bifurque o repositório
2. Crie sua branch de funcionalidade (`git checkout -b feature/nova-funcionalidade`)
3. Cometa suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Envie para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## Autor

Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt

## Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo LICENSE para detalhes. 