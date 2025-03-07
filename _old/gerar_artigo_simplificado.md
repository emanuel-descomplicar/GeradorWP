# Script Simplificado para Geração de Artigos

**Autor:** Descomplicar - Agência de Aceleração Digital  
**URL:** https://descomplicar.pt

## Descrição

Este script (`src/gerar_artigo.py`) foi desenvolvido como uma versão simplificada do gerador de artigos, focado especificamente em testar a geração de conteúdo via Dify e salvar os resultados localmente. É uma alternativa mais leve e direta para depuração e testes, sem as complexidades da publicação no WordPress.

## Utilização

```bash
python src/gerar_artigo.py --titulo "Título do Artigo" --categoria "Categoria" [--output "diretório_saída"]
```

### Parâmetros

- `--titulo` (obrigatório): O título do artigo a ser gerado
- `--categoria` (obrigatório): A categoria do artigo (usado para contexto na geração)
- `--output` (opcional): Diretório onde o artigo será salvo (padrão: "output")

## Fluxo de Funcionamento

1. **Inicialização do Dify Client**: Estabelece conexão com a API Dify para geração de conteúdo
2. **Geração de Outline**: Cria a estrutura básica do artigo baseada no título
3. **Geração de Conteúdo**: Gera o conteúdo HTML completo do artigo
4. **Salvamento Local**: Salva o conteúdo HTML em um arquivo no diretório especificado

## Exemplos

### Gerar um artigo sobre IA
```bash
python src/gerar_artigo.py --titulo "O Impacto da Inteligência Artificial nas PMEs Portuguesas" --categoria "Tecnologia"
```

### Especificar um diretório de saída personalizado
```bash
python src/gerar_artigo.py --titulo "Estratégias de Marketing Digital" --categoria "Marketing" --output "artigos/marketing"
```

## Diferenças em Relação ao Script Completo

Este script simplificado:

- Não requer configurações de WordPress
- Não tenta publicar o artigo online
- Não gera imagens destacadas
- Não executa validações extensivas de conteúdo
- Não faz integração com o Rank Math para SEO

É recomendado para:
- Testes rápidos de geração de conteúdo
- Depuração de problemas específicos com a API Dify
- Geração de conteúdo offline para revisão manual

## Próximos Passos

Após gerar o artigo localmente, você pode:

1. Revisar manualmente o conteúdo HTML gerado
2. Utilizar o script completo (`test_article.py`) para publicar no WordPress
3. Extrair partes específicas do conteúdo para uso em outros contextos

## Tratamento de Erros

O script implementa tratamento básico de erros e logging para facilitar a depuração. Todas as mensagens são exibidas no console e as falhas são registradas claramente para identificação rápida do problema. 