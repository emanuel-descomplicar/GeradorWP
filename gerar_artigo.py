"""
Script para gerar e publicar um artigo sobre marketing digital para clínicas de psicologia.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import logging
from dotenv import load_dotenv
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carrega variáveis de ambiente
load_dotenv()

def gerar_artigo():
    """Gera um artigo sobre marketing digital para clínicas de psicologia."""
    logger.info("Gerando artigo sobre marketing digital para clínicas de psicologia...")
    
    # Título do artigo
    titulo = "A Importância do Marketing Digital para Clínicas de Psicologia"
    
    # Conteúdo do artigo
    conteudo = """
<h1>A Importância do Marketing Digital para Clínicas de Psicologia</h1>

<p>No cenário atual, onde a presença online se tornou essencial para qualquer negócio, as clínicas de psicologia não podem ficar para trás. O marketing digital oferece ferramentas poderosas que permitem às clínicas de psicologia alcançarem mais pacientes, construírem uma reputação sólida e se destacarem num mercado cada vez mais competitivo.</p>

<h2>Por que o Marketing Digital é Fundamental para Clínicas de Psicologia?</h2>

<p>A transformação digital tem mudado a forma como as pessoas procuram serviços de saúde mental. Hoje, antes de marcar uma consulta, potenciais pacientes pesquisam online, leem avaliações e comparam opções. Uma estratégia de marketing digital bem executada permite que sua clínica:</p>

<ul>
    <li><strong>Aumente sua visibilidade online</strong>, sendo encontrada por quem precisa dos seus serviços</li>
    <li><strong>Construa credibilidade e confiança</strong> através de conteúdo relevante e educativo</li>
    <li><strong>Estabeleça conexões significativas</strong> com pacientes atuais e potenciais</li>
    <li><strong>Diferencie-se da concorrência</strong>, destacando sua abordagem única</li>
    <li><strong>Expanda seu alcance geográfico</strong>, especialmente com a popularização do atendimento online</li>
</ul>

<h2>Estratégias Eficazes de Marketing Digital para Psicólogos</h2>

<h3>1. Website Profissional e Otimizado</h3>

<p>Seu website é frequentemente o primeiro contato que potenciais pacientes têm com sua clínica. Ele deve ser:</p>

<ul>
    <li>Profissional e acolhedor, transmitindo confiança</li>
    <li>Responsivo, funcionando perfeitamente em dispositivos móveis</li>
    <li>Otimizado para SEO, para ser encontrado nas pesquisas</li>
    <li>Fácil de navegar, com informações claras sobre serviços e formas de contato</li>
    <li>Seguro, especialmente para proteger dados sensíveis dos pacientes</li>
</ul>

<h3>2. Conteúdo Relevante e Educativo</h3>

<p>Criar e compartilhar conteúdo de qualidade posiciona você como autoridade em sua área e ajuda a educar o público sobre saúde mental:</p>

<ul>
    <li>Blog com artigos sobre temas relevantes de psicologia</li>
    <li>E-books e guias sobre bem-estar mental</li>
    <li>Vídeos explicativos sobre condições psicológicas comuns</li>
    <li>Podcasts abordando temas de saúde mental</li>
    <li>Infográficos compartilháveis em redes sociais</li>
</ul>

<h3>3. Presença Ativa nas Redes Sociais</h3>

<p>As redes sociais são canais poderosos para conectar-se com seu público e desmistificar temas relacionados à saúde mental:</p>

<ul>
    <li>Instagram para compartilhar dicas rápidas e infográficos</li>
    <li>Facebook para criar uma comunidade e compartilhar artigos mais longos</li>
    <li>LinkedIn para networking profissional e conteúdo mais técnico</li>
    <li>YouTube para vídeos educativos e explicativos</li>
    <li>TikTok para alcançar públicos mais jovens com conteúdo acessível</li>
</ul>

<h3>4. Email Marketing Personalizado</h3>

<p>O email marketing permite manter contato regular com pacientes atuais e potenciais:</p>

<ul>
    <li>Newsletter mensal com dicas de saúde mental</li>
    <li>Lembretes de consultas e acompanhamentos</li>
    <li>Conteúdo exclusivo para assinantes</li>
    <li>Informações sobre novos serviços ou horários disponíveis</li>
    <li>Pesquisas de satisfação para melhorar continuamente</li>
</ul>

<h3>5. SEO Local para Atrair Pacientes da Região</h3>

<p>Para clínicas físicas, o SEO local é fundamental para ser encontrado por pacientes próximos:</p>

<ul>
    <li>Google Meu Negócio otimizado e atualizado</li>
    <li>Diretórios locais de profissionais de saúde</li>
    <li>Palavras-chave locais no seu website</li>
    <li>Avaliações e depoimentos de pacientes</li>
    <li>Conteúdo relevante para a comunidade local</li>
</ul>

<h2>Desafios Específicos e Como Superá-los</h2>

<h3>Confidencialidade e Ética Profissional</h3>

<p>O marketing para serviços de psicologia deve sempre respeitar a confidencialidade e seguir os códigos de ética profissional:</p>

<ul>
    <li>Nunca use casos reais sem consentimento explícito e anonimização</li>
    <li>Evite promessas de "cura" ou resultados garantidos</li>
    <li>Mantenha a comunicação profissional e baseada em evidências</li>
    <li>Seja transparente sobre qualificações e abordagens terapêuticas</li>
    <li>Respeite os limites da relação profissional nas redes sociais</li>
</ul>

<h3>Equilibrando o Profissionalismo e a Acessibilidade</h3>

<p>Um desafio comum é encontrar o equilíbrio entre manter o profissionalismo e tornar o conteúdo acessível:</p>

<ul>
    <li>Use linguagem clara e evite jargão técnico excessivo</li>
    <li>Mantenha o tom acolhedor, mas profissional</li>
    <li>Aborde temas sensíveis com cuidado e respeito</li>
    <li>Humanize sua comunicação sem comprometer a credibilidade</li>
    <li>Adapte a linguagem ao canal e ao público-alvo</li>
</ul>

<h2>Medindo Resultados e Ajustando Estratégias</h2>

<p>Como em qualquer estratégia de marketing, é essencial medir resultados e fazer ajustes:</p>

<ul>
    <li>Acompanhe métricas de tráfego do website e conversões</li>
    <li>Monitore o engajamento nas redes sociais</li>
    <li>Analise taxas de abertura e cliques em campanhas de email</li>
    <li>Pergunte aos novos pacientes como encontraram sua clínica</li>
    <li>Teste diferentes abordagens e otimize com base nos resultados</li>
</ul>

<h2>Conclusão</h2>

<p>O marketing digital não é apenas uma tendência passageira, mas uma necessidade para clínicas de psicologia que desejam prosperar no ambiente atual. Ao implementar estratégias eficazes de marketing digital, psicólogos podem não apenas atrair mais pacientes, mas também educar o público sobre a importância da saúde mental e derrubar estigmas associados à busca por ajuda psicológica.</p>

<p>Lembre-se que o objetivo final do marketing para serviços de psicologia não é apenas promover seu negócio, mas também conectar pessoas que precisam de ajuda com os profissionais qualificados que podem fornecê-la.</p>

<h3>Precisa de ajuda para implementar estratégias de marketing digital para sua clínica de psicologia?</h3>

<p>A Descomplicar - Agência de Aceleração Digital especializa-se em soluções de marketing digital para profissionais de saúde. Entre em contato connosco para descobrir como podemos ajudar sua clínica a alcançar mais pacientes e fazer a diferença na vida de mais pessoas.</p>
    """
    
    # Resumo do artigo
    resumo = """
    Descubra como o marketing digital pode transformar sua clínica de psicologia, aumentando sua visibilidade online, construindo credibilidade e atraindo mais pacientes. Este artigo apresenta estratégias eficazes de marketing digital específicas para psicólogos, abordando desafios únicos da área e fornecendo dicas práticas para implementação.
    """
    
    # Categorias e tags
    categorias = ["Marketing Digital", "Psicologia"]
    tags = [
        "marketing digital psicologia", 
        "marketing para psicólogos", 
        "divulgação clínica psicologia", 
        "psicologia online", 
        "marketing consultório psicologia", 
        "presença digital psicólogos", 
        "atendimento online psicologia", 
        "estratégias marketing psicologia"
    ]
    
    return {
        "titulo": titulo,
        "conteudo": conteudo,
        "resumo": resumo,
        "categorias": categorias,
        "tags": tags
    }

def publicar_no_wordpress(artigo):
    """Publica o artigo no WordPress."""
    try:
        # Configurações do WordPress
        wp_url = os.getenv('WP_URL')
        wp_username = os.getenv('WP_USERNAME')
        wp_password = os.getenv('WP_APP_PASSWORD')
        
        if not wp_url or not wp_username or not wp_password:
            logger.error("Configurações do WordPress não encontradas no arquivo .env")
            return False
        
        # Conecta ao WordPress
        wp_client = Client(f"{wp_url}/xmlrpc.php", wp_username, wp_password)
        
        # Cria o post
        post = WordPressPost()
        post.title = artigo["titulo"]
        post.content = artigo["conteudo"]
        post.excerpt = artigo["resumo"]
        post.terms_names = {
            'category': artigo["categorias"],
            'post_tag': artigo["tags"]
        }
        post.post_status = 'publish'
        
        # Publica o post
        post_id = wp_client.call(NewPost(post))
        
        logger.info(f"Artigo publicado com sucesso! ID: {post_id}")
        logger.info(f"Título: {artigo['titulo']}")
        logger.info(f"URL: {wp_url}/?p={post_id}")
        
        return True
    except Exception as e:
        logger.error(f"Erro ao publicar no WordPress: {str(e)}")
        return False

def main():
    """Função principal."""
    try:
        print("Iniciando geração e publicação de artigo sobre marketing digital para clínicas de psicologia...")
        
        # Gera o artigo
        artigo = gerar_artigo()
        
        # Publica no WordPress
        resultado = publicar_no_wordpress(artigo)
        
        if resultado:
            print("Artigo gerado e publicado com sucesso!")
        else:
            print("Erro ao publicar o artigo. Verifique os logs para mais detalhes.")
        
    except Exception as e:
        logger.error(f"Erro: {str(e)}")
        print(f"Erro: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 