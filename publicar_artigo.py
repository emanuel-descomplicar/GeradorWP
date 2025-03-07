"""
Script para publicar um artigo sobre marketing digital para clínicas de psicologia.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configura o logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    """Função principal para publicar o artigo."""
    try:
        print("Iniciando publicação de artigo: A Importância do Marketing Digital para Clínicas de Psicologia")
        
        # Define o tópico e palavras-chave
        topic = "A Importância do Marketing Digital para Clínicas de Psicologia"
        keywords = [
            "marketing digital psicologia",
            "marketing para psicólogos",
            "divulgação clínica psicologia",
            "psicologia online",
            "marketing consultório psicologia",
            "presença digital psicólogos",
            "atendimento online psicologia",
            "estratégias marketing psicologia"
        ]
        
        print(f"Palavras-chave: {', '.join(keywords)}")
        
        # Gera o conteúdo diretamente
        print("\n1. Gerando conteúdo...")
        
        content = """
# A Importância do Marketing Digital para Clínicas de Psicologia

## Introdução

No cenário atual, onde a presença online se tornou essencial para qualquer negócio, as clínicas de psicologia não podem ficar para trás. O marketing digital oferece oportunidades únicas para psicólogos e clínicas ampliarem seu alcance, estabelecerem autoridade em suas áreas de especialização e conectarem-se com potenciais pacientes de forma mais eficaz e personalizada.

Este artigo explora a importância do marketing digital para clínicas de psicologia, apresentando estratégias práticas e eficientes para implementar uma presença online sólida e ética, respeitando sempre os princípios deontológicos da profissão.

## Por que o Marketing Digital é Essencial para Clínicas de Psicologia?

### Alcance Ampliado

O marketing digital permite que clínicas de psicologia alcancem um público muito maior do que seria possível apenas com métodos tradicionais. Através de estratégias bem implementadas, é possível atingir pessoas que estão ativamente procurando por serviços de saúde mental, mesmo que estejam geograficamente distantes da sua clínica.

### Credibilidade e Autoridade

Manter um site profissional, blog com conteúdo relevante e perfis ativos nas redes sociais ajuda a estabelecer a clínica como uma autoridade no campo da psicologia. Compartilhar conhecimentos, pesquisas e informações úteis sobre saúde mental contribui para construir confiança com potenciais pacientes.

### Educação e Desmistificação

O marketing de conteúdo permite educar o público sobre a importância da saúde mental, desmistificar o processo terapêutico e reduzir o estigma associado à busca por ajuda psicológica. Isso não apenas beneficia a sociedade como um todo, mas também incentiva mais pessoas a procurarem apoio profissional.

### Personalização e Segmentação

As ferramentas digitais permitem segmentar o público-alvo com base em diversos critérios, como idade, localização, interesses e comportamentos online. Isso possibilita a criação de mensagens mais relevantes e personalizadas, aumentando a eficácia das campanhas de marketing.

## Estratégias de Marketing Digital para Clínicas de Psicologia

### 1. Website Profissional e Otimizado

Um website bem estruturado é a base de qualquer estratégia de marketing digital. Para clínicas de psicologia, o site deve:

- Ter design limpo e acolhedor, transmitindo confiança e profissionalismo
- Ser responsivo (adaptado para dispositivos móveis)
- Incluir informações claras sobre serviços, especialidades e profissionais
- Conter depoimentos de pacientes (respeitando o anonimato)
- Facilitar o agendamento de consultas
- Ser otimizado para SEO (Search Engine Optimization)

### 2. Marketing de Conteúdo

Criar e compartilhar conteúdo relevante é uma das estratégias mais eficazes para clínicas de psicologia:

- Blog com artigos sobre saúde mental, bem-estar e temas relacionados
- E-books e guias gratuitos sobre tópicos específicos
- Vídeos explicativos sobre condições psicológicas comuns
- Podcasts abordando questões de saúde mental
- Infográficos com dicas práticas e informações úteis

### 3. Presença nas Redes Sociais

As redes sociais são canais poderosos para conectar-se com o público:

- Instagram: compartilhar infográficos, dicas rápidas e conteúdo visual
- Facebook: criar uma comunidade, compartilhar artigos e promover eventos
- LinkedIn: networking profissional e compartilhamento de conteúdo mais técnico
- YouTube: vídeos educativos sobre saúde mental
- Twitter: compartilhar notícias, pesquisas e participar de discussões relevantes

### 4. Email Marketing

O email marketing continua sendo uma ferramenta eficaz para nutrir relacionamentos:

- Newsletter mensal com artigos, dicas e novidades da clínica
- Sequências de emails educativos para novos inscritos
- Lembretes de consultas e acompanhamento pós-atendimento
- Conteúdo exclusivo para a lista de emails

### 5. SEO (Search Engine Optimization)

Otimizar o site para mecanismos de busca é fundamental para ser encontrado por quem procura serviços de psicologia:

- Pesquisa de palavras-chave relevantes para o setor
- Otimização on-page (títulos, meta descrições, estrutura de URL)
- Criação de conteúdo otimizado para termos de busca específicos
- Construção de backlinks de qualidade
- Otimização para busca local (Google Meu Negócio)

### 6. Publicidade Online

Anúncios pagos podem complementar as estratégias orgânicas:

- Google Ads para aparecer nas buscas por termos relevantes
- Anúncios no Facebook e Instagram direcionados ao público-alvo
- Remarketing para reconectar-se com visitantes do site
- Anúncios de display em sites relacionados à saúde e bem-estar

## Considerações Éticas no Marketing Digital para Psicólogos

Ao implementar estratégias de marketing digital, os psicólogos devem sempre considerar as questões éticas envolvidas:

### Confidencialidade

Nunca compartilhar informações que possam identificar pacientes, mesmo com consentimento. Depoimentos devem ser anônimos ou fictícios (com clara indicação).

### Expectativas Realistas

Evitar promessas de "cura" ou resultados garantidos. O marketing deve ser honesto sobre o que a terapia pode oferecer.

### Linguagem Apropriada

Utilizar linguagem acessível, mas evitar simplificações excessivas que possam banalizar condições psicológicas sérias.

### Respeito às Diretrizes Profissionais

Seguir as diretrizes do conselho profissional de psicologia quanto à publicidade e marketing de serviços.

## Medindo o Sucesso das Estratégias de Marketing Digital

Para avaliar a eficácia das estratégias implementadas, é importante monitorar métricas como:

- Tráfego do website
- Taxa de conversão (visitantes que agendam consultas)
- Engajamento nas redes sociais
- Abertura e cliques em emails
- Posicionamento nas buscas para palavras-chave relevantes
- ROI (retorno sobre investimento) em publicidade paga

## Conclusão

O marketing digital oferece inúmeras oportunidades para clínicas de psicologia ampliarem seu alcance, educarem o público sobre saúde mental e conectarem-se com pessoas que precisam de apoio psicológico. Ao implementar estratégias digitais de forma ética e profissional, os psicólogos não apenas beneficiam seus consultórios, mas também contribuem para uma sociedade mais consciente sobre a importância da saúde mental.

Investir em marketing digital não significa abandonar os valores fundamentais da profissão, mas sim utilizar as ferramentas disponíveis para cumprir melhor a missão de promover o bem-estar psicológico e ajudar mais pessoas a terem acesso a serviços de saúde mental de qualidade.

## Como Começar?

Se você é proprietário de uma clínica de psicologia e deseja implementar ou aprimorar suas estratégias de marketing digital, considere começar com passos simples:

1. Crie ou atualize seu website
2. Estabeleça presença nas redes sociais mais relevantes para seu público
3. Comece a produzir conteúdo útil e informativo
4. Otimize seu perfil no Google Meu Negócio
5. Considere buscar ajuda profissional para estratégias mais avançadas

Lembre-se: o marketing digital é uma maratona, não uma corrida de velocidade. Resultados consistentes vêm com tempo, dedicação e estratégias bem planejadas.

Precisa de ajuda para implementar estratégias de marketing digital para sua clínica de psicologia? Entre em contato conosco para uma consultoria especializada!
        """
        
        # Publica o conteúdo no WordPress
        print("\n2. Publicando no WordPress...")
        
        from gerador_wp.utils.wordpress import WordPressClient
        
        # Inicializa o cliente WordPress
        wp_client = WordPressClient()
        
        # Define os dados do post
        title = "A Importância do Marketing Digital para Clínicas de Psicologia"
        excerpt = "Descubra como o marketing digital pode transformar a presença online da sua clínica de psicologia, atrair mais pacientes e estabelecer autoridade no mercado, sempre respeitando os princípios éticos da profissão."
        status = "draft"  # Pode ser "draft", "publish", "pending", "private"
        category = "Marketing Digital"
        tags = keywords
        
        # Publica o post
        post_data = wp_client.create_post(
            title=title,
            content=content,
            excerpt=excerpt,
            status=status,
            category=category,
            tags=tags
        )
        
        # Exibe informações sobre o post publicado
        print("\n3. Artigo publicado com sucesso!")
        print(f"Título: {post_data['title']}")
        print(f"Status: {post_data['status']}")
        print(f"Link: {post_data['link']}")
        print(f"ID: {post_data['id']}")
        
        return 0
    
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        print(f"\nErro: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 