# Gerador de Artigos WordPress

## Descrição
Sistema automatizado para geração e publicação de artigos otimizados para SEO no WordPress, desenvolvido pela Descomplicar.

## Funcionalidades
- Geração de artigos completos com mais de 2000 palavras
- Otimização SEO automática com Rank Math
- Geração de imagens destacadas otimizadas
- Gestão automática de categorias e tags
- Sistema de cache para imagens
- Integração completa com WordPress REST API
- Suporte a metadados SEO personalizados
- Verificação e validação de conteúdo

## Requisitos
- Python 3.10 ou superior
- WordPress com REST API ativada
- Plugin Rank Math SEO instalado e configurado
- Acesso de aplicação WordPress configurado

## Instalação
1. Clone o repositório
```bash
git clone https://github.com/descomplicar/gerador-wp.git
cd gerador-wp
```

2. Crie e ative o ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

## Configuração
### Variáveis de Ambiente
- `WP_URL`: URL da API WordPress (ex: https://descomplicar.pt/wp-json)
- `WP_USERNAME`: Nome de utilizador WordPress
- `WP_APP_PASSWORD`: Senha de aplicação WordPress

### Categorias WordPress
Configure os IDs corretos das categorias no ficheiro `src/publicar_artigo.py`:
```python
categories = [
    15,  # Marketing Digital
    17,  # Estratégia Digital
    19   # Consultoria
]
```

### Metadados SEO
Os metadados do Rank Math são configurados automaticamente, incluindo:
- SEO Title
- Meta Description
- Focus Keywords
- Open Graph
- Twitter Cards

## Utilização
Para publicar um novo artigo:
```bash
python src/publicar_artigo.py
```

## Estrutura do Projeto
```
gerador-wp/
├── src/
│   ├── __init__.py
│   ├── publicar_artigo.py
│   ├── image_generator.py
│   └── tests/
│       └── test_image_generator.py
├── cache/
│   └── images/
├── .env
├── requirements.txt
└── README.md
```

## Autor
Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt

## Licença
Proprietária - Todos os direitos reservados 