# Documentação do Gerador de Imagens Destacadas

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */

## Descrição

O módulo `image_generator.py` é responsável pela geração de imagens destacadas para artigos do WordPress. Ele utiliza templates específicos para cada categoria e aplica o título do artigo sobre a imagem com configurações otimizadas.

## Configurações Principais

### Parâmetros de Texto

| Parâmetro                | Valor           | Descrição                                      |
| ------------------------ | --------------- | ---------------------------------------------- |
| Fonte                    | Montserrat Bold | Fonte utilizada para o texto                   |
| Tamanho                  | 65px            | Tamanho da fonte                               |
| Cor                      | Preto (#000000) | Cor do texto                                   |
| Largura máxima           | 850px           | Largura máxima do texto antes de quebrar linha |
| **Margem superior**      | **500px**       | **Posição vertical fixa do texto (CRÍTICO)**   |
| Posição horizontal       | 100px           | Distância da borda esquerda                    |
| Espaçamento entre linhas | 15px            | Espaçamento vertical entre linhas              |
| Máximo de linhas         | 5               | Número máximo de linhas antes de truncar       |

### Templates por Categoria

O sistema utiliza templates específicos para cada categoria:

- Marketing Digital: `templates/Marketing Digital.png`
- E-commerce: `templates/e-commerce.png`
- Gestão de PMEs: `templates/PMEs_Gestão.png`
- Inteligência Artificial: `templates/Inteligência Artificial.png`
- Transformação Digital: `templates/Transformação Digital.png`
- Vendas: `templates/Vendas.png`
- Empreendedorismo: `templates/Empreendedorismo.png`
- Tecnologia: `templates/Tecnologia.png`
- Default: `templates/default.png` (usado quando a categoria não tem template específico)

## Requisitos Críticos

### Margem Superior de 500px

**IMPORTANTE**: A margem superior de 500px é essencial para evitar sobreposição com outros elementos do template. Esta configuração deve ser mantida em todas as atualizações futuras do código.

O sistema implementa múltiplas verificações para garantir que esta margem seja respeitada:

1. Na inicialização da classe:
   ```python
   self.text_position = (100, 500)  # Posição inicial do texto com margem superior FIXA de 500px
   ```

2. No método `_calculate_text_position`:
   ```python
   # FORÇAR a posição y para exatamente 500px
   y = 500
   ```

3. No método `create_featured_image`:
   ```python
   # FORÇAR a posição vertical para exatamente 500px
   y = 500
   ```

### Tratamento de Títulos Longos

Para títulos longos, o sistema:

1. Limita o título a 800 caracteres
2. Quebra o texto em linhas de no máximo 850px de largura
3. Limita a 5 linhas no máximo
4. Adiciona "..." à última linha quando truncado
5. Limita o nome do arquivo a 50 caracteres para evitar erros no WordPress

## Uso do Módulo

### Uso Básico

```python
from src.image_generator import ImageGenerator

generator = ImageGenerator()
image_path = generator.create_featured_image(
    title="Estratégias de Marketing Digital para PMEs em 2025",
    category="Marketing Digital"
)
print(f"Imagem gerada: {image_path}")
```

### Uso Avançado

```python
import asyncio
from src.image_generator import ImageGenerator

async def generate_images():
    generator = ImageGenerator(api_key="sua_api_key")
    
    # Gerar imagem destacada
    featured_image = generator.create_featured_image(
        title="Estratégias de Marketing Digital para PMEs em 2025",
        category="Marketing Digital"
    )
    
    # Gerar imagem para seção específica (usando API externa)
    section_image = await generator.generate_image(
        prompt="Gráfico mostrando crescimento de marketing digital",
        title="Estratégias de Marketing Digital",
        section="Confiança"
    )
    
    return featured_image, section_image

# Executar função assíncrona
featured_image, section_image = asyncio.run(generate_images())
```

## Considerações Importantes

1. **Margem Superior**: A margem superior de 500px é crítica e não deve ser alterada, pois garante que o texto não se sobreponha a outros elementos do template.

2. **Templates**: Todos os templates devem ser projetados considerando a posição do texto a 500px do topo.

3. **Fonte**: A fonte Montserrat Bold deve estar disponível no diretório `fonts/`.

4. **Cache**: As imagens geradas são armazenadas em cache para evitar regeneração desnecessária.

5. **Fallback**: Se uma categoria não tiver template específico, o sistema tentará encontrar uma correspondência parcial ou usará o template padrão.

## Testes e Validação

Para testar o gerador de imagens:

```bash
python src/image_generator.py "Título do Artigo" "Categoria"
```

Ou usando o script de publicação de teste:

```bash
python src/publish_test_article.py --title "Título do Artigo" --category "Categoria"
```

## Resolução de Problemas

### Texto Não Visível ou Mal Posicionado

Se o texto não estiver visível ou estiver mal posicionado:

1. Verifique se a margem superior de 500px está sendo respeitada
2. Confirme que o método `_calculate_text_position` está retornando y=500
3. Verifique se o método `create_featured_image` não está sobrescrevendo o valor de y
4. Teste com títulos de diferentes comprimentos para garantir consistência

### Erros ao Fazer Upload para WordPress

Se ocorrerem erros ao fazer upload da imagem para o WordPress:

1. Verifique se o nome do arquivo não é muito longo (deve ser limitado a 50 caracteres)
2. Confirme que o formato da imagem é suportado (WebP é recomendado)
3. Verifique se o tamanho do arquivo não excede os limites do WordPress

## Histórico de Atualizações

- **05/03/2025**: Implementada correção para garantir que a margem superior de 500px seja sempre respeitada
- **04/03/2025**: Adicionado suporte para templates por categoria
- **03/03/2025**: Implementada geração de imagens destacadas com texto
- **02/03/2025**: Versão inicial do gerador de imagens 