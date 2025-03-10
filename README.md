# GeradorWP

## Descrição
Gerador automático de artigos para WordPress com inteligência artificial. Desenvolvido pela Descomplicar, este projeto permite criar conteúdo estruturado e otimizado para SEO de forma automatizada.

## Funcionalidades
- Geração automática de artigos com IA
- Formatação estruturada do conteúdo
- Otimização SEO automática
- Integração direta com WordPress
- Geração automática de imagens destacadas
- Categorização inteligente de conteúdo
- Sistema de tags automático

## Requisitos
- Python 3.10 ou superior
- Acesso a uma instalação WordPress
- Credenciais de API necessárias
- Bibliotecas Python (ver requirements.txt)

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/emanuel-descomplicar/GeradorWP.git
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Configure as variáveis de ambiente:
```bash
cp .env.example .env
# Edite o ficheiro .env com suas credenciais
```

## Utilização
```bash
python src/examples/generate_article.py --topic "Seu Tópico" --category "sua-categoria" --publish
```

## Estrutura do Projeto
```
GeradorWP/
├── src/
│   ├── generators/
│   │   └── content_generator.py
│   ├── integrations/
│   │   ├── dify_client.py
│   │   └── wordpress_client.py
│   └── examples/
│       └── generate_article.py
├── debug/
│   └── verify_solution.py
├── tests/
├── docs/
└── requirements.txt
```

## Autor
Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt

## Licença
Todos os direitos reservados © 2024 Descomplicar