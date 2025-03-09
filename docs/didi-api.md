# Documentação da API da Didi - Descomplicar

## Visão Geral

A API Didi da Descomplicar permite que os desenvolvedores integrem capacidades avançadas de IA em suas aplicações. Esta documentação detalha os endpoints disponíveis, seus parâmetros e respostas.

## Autenticação

Todas as requisições à API devem incluir uma chave de API no cabeçalho `Authorization`. Por razões de segurança, recomendamos armazenar sua chave da API no lado do servidor e nunca compartilhá-la ou armazená-la no lado do cliente.

```
Authorization: Bearer {API_KEY}
```

## URL Base

```
https://didi.descomplicar.pt/v1
```

## Endpoints

### 1. Enviar Mensagem
`POST /chat-messages`

Envia uma solicitação para a aplicação de chat.

#### Parâmetros do Corpo

| Nome | Tipo | Descrição |
|------|------|-----------|
| query | string | Conteúdo da entrada/pergunta do usuário |
| inputs | object | Permite a entrada de vários valores de variáveis definidos pela aplicação |
| response_mode | string | Modo de retorno da resposta: `streaming` (recomendado) ou `blocking` |
| user | string | Identificador do usuário final |
| conversation_id | string | ID da conversa, necessário para continuar uma conversa anterior |
| files | array[object] | Lista de ficheiros para entrada |
| auto_generate_name | bool | Gerar título automaticamente (padrão: true) |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/chat-messages' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "inputs": {},
    "query": "Quais são as especificações do iPhone 13 Pro Max?",
    "response_mode": "streaming",
    "conversation_id": "",
    "user": "abc-123",
    "files": [
      {
        "type": "image",
        "transfer_method": "remote_url",
        "url": "https://example.com/image.png"
      }
    ]
}'
```

### 2. Upload de Ficheiro
`POST /files/upload`

Faz upload de um ficheiro para uso posterior em mensagens.

#### Parâmetros do Corpo

Este endpoint requer uma solicitação do tipo `multipart/form-data`.

| Nome | Tipo | Descrição |
|------|------|-----------|
| file | File | O ficheiro a ser carregado |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/files/upload' \
--header 'Authorization: Bearer {api_key}' \
--form 'file=@ficheiro_local;type=image/png' \
--form 'user=abc-123'
```

### 3. Parar Geração
`POST /chat-messages/:task_id/stop`

Interrompe a geração de resposta (apenas suportado no modo streaming).

#### Parâmetros

| Nome | Tipo | Descrição |
|------|------|-----------|
| task_id | string | ID da tarefa (obtido na resposta streaming) |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/chat-messages/:task_id/stop' \
-H 'Authorization: Bearer {api_key}' \
-H 'Content-Type: application/json' \
--data-raw '{"user": "abc-123"}'
```

### 4. Feedback de Mensagem
`POST /messages/:message_id/feedbacks`

Permite que os usuários forneçam feedback sobre as mensagens.

#### Parâmetros

| Nome | Tipo | Descrição |
|------|------|-----------|
| message_id | string | ID da mensagem |
| rating | string | "like" para positivo, "dislike" para negativo, nulo para revogar |
| user | string | Identificador do usuário |
| content | string | Conteúdo específico do feedback |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/messages/:message_id/feedbacks' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "rating": "like",
    "user": "abc-123",
    "content": "Informação de feedback da mensagem"
}'
```

### 5. Obter Perguntas Sugeridas
`GET /messages/{message_id}/suggested`

Obtém sugestões de próximas perguntas para a mensagem atual.

#### Parâmetros

| Nome | Tipo | Descrição |
|------|------|-----------|
| message_id | string | ID da mensagem |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl --location --request GET 'https://didi.descomplicar.pt/v1/messages/{message_id}/suggested?user=abc-123' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json'
```

### 6. Obter Histórico de Mensagens da Conversa
`GET /messages`

Retorna registros históricos de chat em formato de carregamento por deslocamento.

#### Parâmetros de Consulta

| Nome | Tipo | Descrição |
|------|------|-----------|
| conversation_id | string | ID da conversa |
| user | string | Identificador do usuário |
| first_id | string | ID do primeiro registro de chat na página atual (padrão: null) |
| limit | int | Quantidade de mensagens a retornar (padrão: 20) |

#### Exemplo de Solicitação

```bash
curl -X GET 'https://didi.descomplicar.pt/v1/messages?user=abc-123&conversation_id=' \
--header 'Authorization: Bearer {api_key}'
```

### 7. Obter Conversas
`GET /conversations`

Recupera a lista de conversas para o usuário atual.

#### Parâmetros de Consulta

| Nome | Tipo | Descrição |
|------|------|-----------|
| user | string | Identificador do usuário |
| last_id | string | ID do último registro na página atual (padrão: null) |
| limit | int | Quantidade de registros a retornar (padrão: 20, máximo: 100) |
| sort_by | string | Campo de ordenação (padrão: -updated_at) |

#### Exemplo de Solicitação

```bash
curl -X GET 'https://didi.descomplicar.pt/v1/conversations?user=abc-123&last_id=&limit=20' \
--header 'Authorization: Bearer {api_key}'
```

### 8. Eliminar Conversa
`DELETE /conversations/:conversation_id`

Elimina uma conversa.

#### Parâmetros

| Nome | Tipo | Descrição |
|------|------|-----------|
| conversation_id | string | ID da conversa |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -X DELETE 'https://didi.descomplicar.pt/v1/conversations/:conversation_id' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{ 
 "user": "abc-123"
}'
```

### 9. Renomear Conversa
`POST /conversations/:conversation_id/name`

Renomeia uma sessão de conversa.

#### Parâmetros

| Nome | Tipo | Descrição |
|------|------|-----------|
| conversation_id | string | ID da conversa |
| name | string | Nome da conversa (opcional se auto_generate for true) |
| auto_generate | bool | Gerar título automaticamente (padrão: false) |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/conversations/:conversation_id/name' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{ 
 "name": "", 
 "auto_generate": true, 
 "user": "abc-123"
}'
```

### 10. Fala para Texto
`POST /audio-to-text`

Converte áudio em texto.

#### Parâmetros do Corpo

| Nome | Tipo | Descrição |
|------|------|-----------|
| file | file | Ficheiro de áudio. Formatos suportados: mp3, mp4, mpeg, mpga, m4a, wav, webm |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -X POST 'https://didi.descomplicar.pt/v1/audio-to-text' \
--header 'Authorization: Bearer {api_key}' \
--form 'file=@ficheiro_local;type=audio/mp3'
```

### 11. Texto para Áudio
`POST /text-to-audio`

Converte texto em fala.

#### Parâmetros do Corpo

| Nome | Tipo | Descrição |
|------|------|-----------|
| message_id | string | Para mensagens geradas pela Didi, passe o message-id |
| text | string | Conteúdo a ser gerado em fala |
| user | string | Identificador do usuário |

#### Exemplo de Solicitação

```bash
curl -o texto-para-audio.mp3 -X POST 'https://didi.descomplicar.pt/v1/text-to-audio' \
--header 'Authorization: Bearer {api_key}' \
--header 'Content-Type: application/json' \
--data-raw '{
    "message_id": "5ad4cb98-f0c7-4085-b384-88c403be6290",
    "text": "Olá Didi",
    "user": "abc-123"
}'
```

### 12. Obter Informações Básicas da Aplicação
`GET /info`

Obter informações básicas sobre a aplicação.

#### Exemplo de Solicitação

```bash
curl -X GET 'https://didi.descomplicar.pt/v1/info' \
-H 'Authorization: Bearer {api_key}'
```

### 13. Obter Informações de Parâmetros da Aplicação
`GET /parameters`

Usado para obter informações sobre parâmetros da aplicação.

#### Exemplo de Solicitação

```bash
curl -X GET 'https://didi.descomplicar.pt/v1/parameters'
```

### 14. Obter Informações Meta da Aplicação
`GET /meta`

Usado para obter ícones de ferramentas nesta aplicação.

#### Exemplo de Solicitação

```bash
curl -X GET 'https://didi.descomplicar.pt/v1/meta' \
-H 'Authorization: Bearer {api_key}'
```

## Códigos de Erro

| Código | Descrição |
|--------|-----------|
| 404 | Conversa não existe |
| 400 | Parâmetro inválido, configuração indisponível, credencial não inicializada, quota excedida, modelo não suportado |
| 413 | Ficheiro muito grande |
| 415 | Tipo de ficheiro não suportado |
| 500 | Erro interno do servidor |
| 503 | Falha na conexão, permissão negada, ficheiro excede limite |

## Eventos de Streaming

Quando `response_mode` é definido como `streaming`, a API retorna uma série de eventos. Cada evento começa com `data:` e é separado por dois caracteres de nova linha `\n\n`.

### Tipos de Eventos

- `message`: Evento de texto retornado pelo modelo
- `message_file`: Evento de ficheiro de mensagem
- `message_end`: Evento de fim de mensagem
- `tts_message`: Evento de stream de áudio TTS
- `tts_message_end`: Evento de fim de stream de áudio TTS
- `message_replace`: Evento de substituição de conteúdo de mensagem
- `workflow_started`: Início de execução do fluxo de trabalho
- `node_started`: Início de execução do nó
- `node_finished`: Fim de execução do nó
- `workflow_finished`: Fim de execução do fluxo de trabalho
- `error`: Exceções que ocorrem durante o processo de streaming
- `ping`: Evento de ping a cada 10 segundos para manter a conexão ativa

## Notas Adicionais

- O tamanho máximo do ficheiro para upload é limitado de acordo com o tipo de ficheiro
- A API suporta uma variedade de formatos de áudio e imagem
- Imagens são suportadas apenas quando o modelo tem capacidade de Visão
- O upload de ficheiros requer prévia autenticação

Para mais informações, contacte a equipa da Descomplicar em [https://descomplicar.pt](https://descomplicar.pt).
