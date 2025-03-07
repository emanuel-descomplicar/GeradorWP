# GeradorWP

## Descrição
Ferramenta desenvolvida em Python para gerar e gerenciar conteúdo WordPress de forma automatizada e eficiente, utilizando Crew AI para orquestrar agentes especializados.

## Funcionalidades
- Geração automática de conteúdo usando IA
- Pesquisa automatizada de informações
- Criação de conteúdo otimizado para SEO
- Publicação automática no WordPress
- Integração com WordPress via REST API
- Processamento de texto e NLP

## Requisitos
- Python 3.x ou superior
- Acesso a uma instalação WordPress
- Conta OpenAI com API Key
- Bibliotecas Python necessárias (ver requirements.txt)

## Instalação
1. Clone o repositório:
```bash
git clone https://github.com/seu-usuario/geradorwp.git
cd geradorwp
```

2. Crie um ambiente virtual e ative-o:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
```bash
cp .env.example .env
```
Edite o ficheiro `.env` com suas credenciais.

## Estrutura do Projeto
```
geradorwp/
├── src/
│   ├── agents/         # Agentes Crew AI
│   ├── tasks/          # Tarefas dos agentes
│   ├── config/         # Configurações
│   └── main.py         # Script principal
├── .env                # Variáveis de ambiente
├── .env.example        # Exemplo de variáveis
├── requirements.txt    # Dependências
└── README.md          # Este ficheiro
```

## Utilização
1. Certifique-se de que todas as variáveis de ambiente estão configuradas no ficheiro `.env`

2. Execute o script principal:
```bash
python src/main.py
```

3. O sistema irá:
   - Pesquisar informações sobre o tópico
   - Gerar conteúdo otimizado
   - Publicar no WordPress

## Agentes
O sistema utiliza três agentes especializados:

1. **Pesquisador**: Coleta informações relevantes sobre o tópico
2. **Escritor**: Cria conteúdo otimizado para SEO
3. **Publicador**: Gerencia a publicação no WordPress

## Contribuição
Contribuições são bem-vindas! Por favor, siga estas etapas:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Autor
Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt 