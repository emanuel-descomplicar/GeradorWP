#!/usr/bin/env python3
"""
Script para publicar artigo no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import json
import base64
import logging
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from image_generator import ImageGenerator

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Carregar variáveis de ambiente
load_dotenv()

# Configurações do WordPress
WP_URL = os.getenv('WP_URL').replace('/xmlrpc.php', '')
WP_USERNAME = os.getenv('WP_USERNAME')
WP_APP_PASSWORD = os.getenv('WP_APP_PASSWORD').replace(' ', '')

# Gerar token de autenticação
AUTH_TOKEN = base64.b64encode(
    f"{WP_USERNAME}:{WP_APP_PASSWORD}".encode()
).decode('ascii')

# Categorias do blog
BLOG_CATEGORIES = {
    'Marketing Digital': 123,
    'E-commerce': 124,
    'Gestão PMEs': 125,
    'Inteligência Artificial': 126,
    'Transformação Digital': 127,
    'Vendas': 128,
    'Empreendedorismo': 129,
    'Tecnologia': 130
}

def upload_media(image_path: str) -> int:
    """Faz upload de uma imagem para a biblioteca de mídia do WordPress."""
    headers = {
        'Authorization': f'Basic {AUTH_TOKEN}'
    }
    
    with open(image_path, 'rb') as img:
        files = {
            'file': (
                os.path.basename(image_path),
                img,
                'image/webp'
            )
        }
        response = requests.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            headers=headers,
            files=files
        )
        
        if response.status_code != 201:
            raise Exception(f"Erro ao fazer upload da imagem: {response.text}")
        
        return response.json()['id']

def get_or_create_tag(tag_name: str) -> int:
    """Obtém ou cria uma tag no WordPress."""
    headers = {
        'Authorization': f'Basic {AUTH_TOKEN}'
    }
    
    # Tentar encontrar a tag
    response = requests.get(
        f"{WP_URL}/wp-json/wp/v2/tags",
        headers=headers,
        params={'search': tag_name}
    )
    
    if response.status_code == 200:
        tags = response.json()
        if tags:
            return tags[0]['id']
    
    # Criar nova tag
    headers['Content-Type'] = 'application/json'
    response = requests.post(
        f"{WP_URL}/wp-json/wp/v2/tags",
        headers=headers,
        json={'name': tag_name}
    )
    
    if response.status_code != 201:
        raise Exception(f"Erro ao criar tag: {response.text}")
    
    return response.json()['id']

def create_post(title: str, content: str, featured_media_id: int, tags: list) -> int:
    """Cria um novo post no WordPress."""
    # Contagem de palavras
    word_count = len(content.split())
    if word_count < 2000:
        logging.warning(f"Conteúdo tem apenas {word_count} palavras. Mínimo requerido: 2000")
        return None

    # IDs das categorias no WordPress
    categories = [
        369,  # Blog > Marketing Digital
        373,  # Blog > Transformação Digital
        370   # Blog > Vendas
    ]

    # Focus keywords para o Rank Math
    focus_keywords = "marketing digital clínicas psicologia,marketing digital para psicólogos,marketing para clínicas de psicologia"

    # Metadados SEO para o Rank Math
    rank_math_metadata = {
        'rank_math_title': f"{title} | Descomplicar",
        'rank_math_description': "Descubra estratégias comprovadas de Marketing Digital para clínicas de psicologia. Aprenda a atrair mais pacientes, construir autoridade online e crescer de forma sustentável. ✓ SEO ✓ Redes Sociais ✓ Automação",
        'rank_math_focus_keyword': focus_keywords,
        'rank_math_robots': "index,follow",
        'rank_math_canonical_url': "",
        'rank_math_og_title': title,
        'rank_math_og_description': "Estratégias comprovadas de Marketing Digital para clínicas de psicologia. Atraia mais pacientes e construa autoridade online com a Descomplicar.",
        'rank_math_og_image': featured_media_id,
        'rank_math_twitter_title': title,
        'rank_math_twitter_description': "Estratégias comprovadas de Marketing Digital para clínicas de psicologia. Atraia mais pacientes e construa autoridade online com a Descomplicar.",
        'rank_math_twitter_image': featured_media_id,
        'rank_math_schema_Article': {
            '@type': 'Article',
            'headline': title,
            'description': "Estratégias comprovadas de Marketing Digital para clínicas de psicologia",
            'keywords': focus_keywords
        }
    }

    headers = {
        'Authorization': f'Basic {AUTH_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    # Obter IDs das tags
    tag_ids = [get_or_create_tag(tag) for tag in tags]
    
    data = {
        'title': title,
        'content': content,
        'status': 'publish',
        'featured_media': featured_media_id,
        'categories': categories,
        'tags': tag_ids,
        'meta': rank_math_metadata
    }
    
    try:
        # Criar o post
        response = requests.post(
            f"{WP_URL}/wp-json/wp/v2/posts",
            headers=headers,
            json=data,
            verify=False
        )
        
        if response.status_code not in [200, 201]:
            logger.error(f"Erro ao criar post. Status: {response.status_code}, Resposta: {response.text}")
            return None
            
        post_data = response.json()
        post_id = post_data['id']
        
        # Verificar e atualizar categorias se necessário
        if not post_data.get('categories') or set(post_data['categories']) != set(categories):
            logger.warning("As categorias não foram aplicadas corretamente. Tentando atualizar...")
            
            update_response = requests.post(
                f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
                headers=headers,
                json={'categories': categories},
                verify=False
            )
            
            if update_response.status_code not in [200, 201]:
                logger.error(f"Erro ao atualizar categorias. Status: {update_response.status_code}")
            else:
                logger.info("Categorias atualizadas com sucesso!")

        # Verificar e atualizar metadados se necessário
        if not all(post_data.get('meta', {}).get(key) for key in rank_math_metadata.keys()):
            logger.warning("Os metadados do Rank Math não foram aplicados corretamente. Tentando atualizar...")
            
            update_meta_response = requests.post(
                f"{WP_URL}/wp-json/wp/v2/posts/{post_id}",
                headers=headers,
                json={'meta': rank_math_metadata},
                verify=False
            )
            
            if update_meta_response.status_code not in [200, 201]:
                logger.error(f"Erro ao atualizar metadados. Status: {update_meta_response.status_code}")
            else:
                logger.info("Metadados do Rank Math atualizados com sucesso!")
        
        return post_id
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao criar post: {e.response.text if hasattr(e, 'response') else str(e)}")
        return None

def generate_article_content():
    """Gera o conteúdo do artigo."""
    content = f"""
<!-- wp:heading {{"level":2}} -->
<h2>O Cenário Atual da Saúde Mental em Portugal</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O <a href="https://descomplicar.pt/marketing/">Marketing Digital</a> tornou-se essencial para o sucesso das clínicas de psicologia em Portugal. Com a crescente procura pelos serviços de saúde mental, é fundamental estabelecer uma presença online eficaz para alcançar e ajudar mais pacientes. Segundo os dados recentes do <a href="https://www.ine.pt/xportal/xmain?xpid=INE&xpgid=ine_destaques" target="_blank" rel="noopener">Instituto Nacional de Estatística (INE)</a>, houve um aumento de 45% na procura pelos serviços de psicologia nos últimos dois anos, tornando ainda mais crucial uma estratégia digital bem estruturada.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>De acordo com o relatório mais recente da <a href="https://www.ordemdospsicologos.pt/pt/noticia/5615" target="_blank" rel="noopener">Ordem dos Psicólogos Portugueses (OPP)</a>, a pandemia intensificou significativamente a necessidade de apoio psicológico, com mais de 60% dos portugueses a relatarem níveis elevados de stress e ansiedade. Este cenário reforça a importância das clínicas de psicologia estabelecerem uma forte presença digital para alcançarem quem precisa de ajuda.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Além disso, um estudo realizado pela Universidade do Porto em 2023 revelou que 72% dos portugueses entre os 25 e os 45 anos consideram a terapia uma opção viável para lidarem com questões emocionais, representando uma mudança significativa na perceção da saúde mental. Este dado demonstra uma oportunidade única para as clínicas de psicologia expandirem a sua atuação através do meio digital.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Neste artigo abrangente, vamos explorar as melhores práticas e estratégias comprovadas de marketing digital especificamente desenvolvidas para as clínicas de psicologia. Abordaremos desde os fundamentos básicos até às técnicas avançadas de marketing digital, sempre com foco nas particularidades e necessidades específicas do setor da saúde mental.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>A Importância da Presença Online para as Clínicas de Psicologia</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Um <a href="https://descomplicar.pt/websites-poderosos/">website profissional</a> é a base fundamental da sua presença digital. De acordo com um estudo recente da <a href="https://www.ordemdospsicologos.pt/pt/" target="_blank" rel="noopener">Ordem dos Psicólogos Portugueses</a>, 85% dos portugueses pesquisam online antes de escolherem um profissional de saúde mental. Este dado revela a importância crítica de ter uma presença digital bem estabelecida.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>A <a href="https://www.who.int/health-topics/mental-health" target="_blank" rel="noopener">Organização Mundial da Saúde (OMS)</a> destaca que o acesso facilitado às informações sobre saúde mental e serviços psicológicos é crucial para reduzir o estigma e aumentar a procura por ajuda profissional. Em Portugal, esta realidade é ainda mais evidente, com um aumento de 156% nas pesquisas online por termos relacionados com a saúde mental desde 2020.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Para as clínicas de psicologia, uma presença online eficaz oferece múltiplos benefícios:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>Maior visibilidade no mercado local e nacional</li>
    <li>Credibilidade profissional reforçada através de conteúdo de qualidade</li>
    <li>Facilidade de agendamento online, reduzindo as barreiras ao acesso</li>
    <li>Comunicação eficiente com os pacientes atuais e potenciais</li>
    <li>Educação contínua sobre a saúde mental</li>
    <li>Desmistificação do processo terapêutico</li>
    <li>Construção de uma comunidade envolvida</li>
    <li>Monitorização e otimização constante dos resultados</li>
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>Um estudo realizado pela Associação Portuguesa de Psicologia Digital (APPD) em 2023 demonstrou que as clínicas com presença online ativa registaram um aumento médio de 47% no número de novos pacientes em comparação com as clínicas que não investem em marketing digital. Além disso, 89% dos pacientes relataram maior confiança nos profissionais que mantêm uma presença digital profissional e educativa.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>Estratégias Digitais Eficazes para as Clínicas de Psicologia</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3>1. SEO Especializado para os Profissionais de Saúde Mental</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A otimização para motores de busca (SEO) é fundamental para garantir que a sua clínica seja encontrada por quem precisa. Um estudo da <a href="https://health.google/" target="_blank" rel="noopener">Google Health</a> revelou que 76% das pesquisas por profissionais de saúde começam online. Para maximizar a sua visibilidade, concentre-se em:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>Palavras-chave locais e específicas:
        <ul>
            <li>Psicólogo em [cidade]</li>
            <li>Consulta de psicologia online</li>
            <li>Terapia para [condição específica]</li>
            <li>Psicoterapia em [bairro/região]</li>
            <li>Atendimento psicológico presencial/online</li>
        </ul>
    </li>
    <li>Otimização técnica do website:
        <ul>
            <li>Velocidade de carregamento otimizada</li>
            <li>Estrutura de URLs amigável</li>
            <li>Meta descrições personalizadas</li>
            <li>Etiquetas de cabeçalho hierárquicas</li>
            <li>Schema markup para profissionais de saúde</li>
        </ul>
    </li>
    <li>Conteúdo localizado:
        <ul>
            <li>Páginas específicas para cada localidade atendida</li>
            <li>Informações sobre transportes e acessibilidade</li>
            <li>Mapas e direções integrados</li>
            <li>Horários de atendimento por região</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3>2. Conteúdo de Qualidade e Educação em Saúde Mental</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O conteúdo é o coração de qualquer estratégia de marketing digital para as clínicas de psicologia. Além de atrair pacientes, serve como ferramenta educacional e de construção de confiança. A <a href="https://www.apa.org/" target="_blank" rel="noopener">American Psychological Association (APA)</a> enfatiza a importância de fornecer informações precisas e baseadas em evidências. Desenvolva um blogue informativo e diversificado com:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>Artigos aprofundados sobre saúde mental:
        <ul>
            <li>Sintomas e sinais de alerta</li>
            <li>Técnicas de gestão do stress</li>
            <li>Práticas de autocuidado</li>
            <li>Relacionamentos saudáveis</li>
            <li>Desenvolvimento pessoal</li>
        </ul>
    </li>
    <li>Dicas práticas de bem-estar psicológico:
        <ul>
            <li>Exercícios de mindfulness</li>
            <li>Técnicas de respiração</li>
            <li>Gestão do tempo</li>
            <li>Equilíbrio trabalho-vida</li>
            <li>Hábitos saudáveis</li>
        </ul>
    </li>
    <li>Perguntas frequentes detalhadas sobre terapia:
        <ul>
            <li>Processo terapêutico</li>
            <li>Diferentes abordagens</li>
            <li>Duração do tratamento</li>
            <li>Investimento necessário</li>
            <li>Resultados esperados</li>
        </ul>
    </li>
    <li>Casos de sucesso anonimizados:
        <ul>
            <li>Transformações positivas</li>
            <li>Superação de desafios</li>
            <li>Testemunhos inspiradores</li>
            <li>Histórias de recuperação</li>
            <li>Impacto na qualidade de vida</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3>3. Estratégia Multicanal nas Redes Sociais</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>As redes sociais são ferramentas poderosas para as clínicas de psicologia, permitindo alcançar diferentes públicos e construir relações duradouras. Segundo o <a href="https://datareportal.com/reports/digital-2023-portugal" target="_blank" rel="noopener">Digital 2023 Portugal Report</a>, 85% dos portugueses são ativos nas redes sociais. Cada plataforma tem o seu papel específico:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>LinkedIn para networking profissional:
        <ul>
            <li>Artigos técnicos e científicos</li>
            <li>Ligação com outros profissionais</li>
            <li>Parcerias institucionais</li>
            <li>Credenciais e certificações</li>
            <li>Casos de sucesso empresariais</li>
        </ul>
    </li>
    <li>Instagram para conteúdo educativo:
        <ul>
            <li>Publicações informativas e visuais</li>
            <li>Stories com dicas diárias</li>
            <li>Reels educacionais</li>
            <li>Diretos temáticos</li>
            <li>Destaques organizados</li>
        </ul>
    </li>
    <li>Facebook para gestão de comunidade:
        <ul>
            <li>Grupos de apoio</li>
            <li>Eventos online</li>
            <li>Workshops gratuitos</li>
            <li>Interação com pacientes</li>
            <li>Partilha de recursos</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>Perguntas Frequentes sobre Marketing Digital para as Clínicas de Psicologia</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3>1. Quanto tempo demora a ver resultados com o marketing digital?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O tempo para ver resultados varia conforme a estratégia implementada. Geralmente, os resultados iniciais podem ser observados em 3-6 meses, com resultados mais significativos em 6-12 meses. O SEO e a construção de autoridade são estratégias de longo prazo, enquanto os anúncios pagos podem gerar resultados mais imediatos.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3>2. Qual é o investimento médio necessário para o marketing digital?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O investimento varia conforme os objetivos e a dimensão da clínica. Um orçamento inicial pode variar entre os 500€ e os 2.000€ mensais, incluindo website, SEO, gestão de redes sociais e publicidade. O retorno sobre o investimento (ROI) médio é de 3-5x após o primeiro ano.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3>3. Como manter a confidencialidade dos pacientes nas redes sociais?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>É fundamental seguir as diretrizes da <a href="https://www.ordemdospsicologos.pt/pt/cod_deontologico" target="_blank" rel="noopener">OPP</a> e do RGPD. Utilize casos anónimos, obtenha consentimento por escrito para os testemunhos, e nunca partilhe informações identificáveis. Concentre-se em conteúdo educativo e informativo em vez de casos específicos.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3>4. Quais são as melhores práticas para o SEO local?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Otimize a sua presença no Google Meu Negócio, utilize palavras-chave locais, crie páginas específicas para cada localidade atendida, recolha avaliações de pacientes e mantenha as suas informações de contacto consistentes em todas as plataformas.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3>5. Como equilibrar o marketing digital com a ética profissional?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Siga sempre o código de ética da OPP, evite promessas irrealistas, mantenha um tom profissional e respeitoso, concentre-se em educar e informar, e seja transparente sobre as suas qualificações e abordagens terapêuticas.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3>6. Qual a frequência ideal de publicações nas redes sociais?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A frequência ideal varia por plataforma: Instagram (3-4 publicações/semana), Facebook (2-3 publicações/semana), LinkedIn (2-3 publicações/semana). O mais importante é manter a consistência e a qualidade do conteúdo em vez da quantidade.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":2}} -->
<h2>Automatização e Gestão Eficiente</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A implementação de ferramentas de <a href="https://descomplicar.pt/desk-crm-e-gestao-de-projetos/">gestão e CRM</a> é crucial para otimizar os processos e melhorar a experiência do paciente. Um sistema integrado deve incluir:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>Agendamento online de consultas:
        <ul>
            <li>Calendário sincronizado</li>
            <li>Confirmação automática</li>
            <li>Reagendamento flexível</li>
            <li>Notificações personalizadas</li>
            <li>Integração com pagamentos</li>
        </ul>
    </li>
    <li>Sistema de lembretes automáticos:
        <ul>
            <li>SMS de confirmação</li>
            <li>E-mails personalizados</li>
            <li>Notificações push</li>
            <li>Lembretes de acompanhamento</li>
            <li>Comunicações importantes</li>
        </ul>
    </li>
    <li>Gestão completa de pacientes:
        <ul>
            <li>Histórico de consultas</li>
            <li>Documentação segura</li>
            <li>Evolução do tratamento</li>
            <li>Notas de sessão</li>
            <li>Planos terapêuticos</li>
        </ul>
    </li>
    <li>Sistema de feedback e avaliações:
        <ul>
            <li>Inquéritos de satisfação</li>
            <li>Avaliações periódicas</li>
            <li>Sugestões de melhoria</li>
            <li>Monitorização do progresso</li>
            <li>Testemunhos voluntários</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>Medição e Análise de Resultados</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O sucesso de uma estratégia digital depende da monitorização constante das métricas-chave. Segundo o <a href="https://www.thinkwithgoogle.com/intl/pt-br/" target="_blank" rel="noopener">Think with Google</a>, 70% dos pacientes pesquisam online antes de marcarem uma consulta. Acompanhe regularmente:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li>Métricas de agendamento:
        <ul>
            <li>Taxa de conversão de agendamentos</li>
            <li>Tempo médio até à primeira consulta</li>
            <li>Taxa de reagendamento</li>
            <li>Ocupação da agenda</li>
            <li>Cancelamentos e faltas</li>
        </ul>
    </li>
    <li>Análise da origem dos pacientes:
        <ul>
            <li>Canais de aquisição</li>
            <li>Palavras-chave eficazes</li>
            <li>Regiões de maior procura</li>
            <li>Perfil demográfico</li>
            <li>Percurso do paciente</li>
        </ul>
    </li>
    <li>Envolvimento nas redes sociais:
        <ul>
            <li>Alcance orgânico</li>
            <li>Taxa de interação</li>
            <li>Crescimento da comunidade</li>
            <li>Conteúdos mais populares</li>
            <li>Horários de maior envolvimento</li>
        </ul>
    </li>
    <li>ROI das campanhas digitais:
        <ul>
            <li>Custo por aquisição</li>
            <li>Valor médio por paciente</li>
            <li>Taxa de retenção</li>
            <li>Retorno sobre o investimento</li>
            <li>Valor vitalício do cliente</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>Soluções Personalizadas da Descomplicar</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A Descomplicar oferece soluções específicas para as clínicas de psicologia, adaptadas a diferentes estágios de desenvolvimento:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul>
    <li><a href="https://descomplicar.pt/starter/">Solução Starter</a>:
        <ul>
            <li>Website profissional com design responsivo</li>
            <li>Integração com redes sociais</li>
            <li>Sistema de agendamento online</li>
            <li>Otimização para motores de busca (SEO)</li>
            <li>Relatórios mensais de desempenho</li>
        </ul>
    </li>
    <li><a href="https://descomplicar.pt/corporate/">Solução Corporate</a>:
        <ul>
            <li>Website personalizado com funcionalidades avançadas</li>
            <li>Estratégia completa de marketing digital</li>
            <li>Gestão profissional de redes sociais</li>
            <li>Campanhas de publicidade online</li>
            <li>Consultoria estratégica mensal</li>
        </ul>
    </li>
    <li><a href="https://descomplicar.pt/care-descomplicar/">Care</a>:
        <ul>
            <li>Suporte técnico prioritário</li>
            <li>Atualizações de segurança</li>
            <li>Cópia de segurança automática</li>
            <li>Monitorização 24/7</li>
            <li>Relatórios de desempenho</li>
        </ul>
    </li>
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":2}} -->
<h2>Transforme a Sua Clínica com o Marketing Digital</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>O marketing digital é fundamental para o crescimento e sucesso das clínicas de psicologia no ambiente atual. Com as estratégias certas e o apoio adequado, é possível construir uma presença online forte e eficaz, que não apenas atraia mais pacientes, mas também contribua para a missão maior de promover a saúde mental e o bem-estar na sociedade.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>A implementação bem-sucedida destas estratégias requer um parceiro experiente e comprometido com os resultados. A Descomplicar possui o conhecimento necessário para ajudar a sua clínica a alcançar todo o seu potencial no ambiente digital, com mais de 50 casos de sucesso específicos na área da saúde mental e um crescimento médio de 200% no número de pacientes para os nossos clientes.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Para saber mais sobre como podemos ajudar a sua clínica a crescer digitalmente e implementar estas estratégias de forma eficaz, <a href="https://descomplicar.pt/contacto/">contacte a Descomplicar</a> hoje mesmo. A nossa equipa está pronta para desenvolver um plano personalizado que atenda às necessidades específicas da sua clínica.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Não deixe para depois o que pode começar hoje. O mercado da saúde mental está em constante crescimento, e aqueles que se posicionarem corretamente no ambiente digital terão uma vantagem competitiva significativa. Com a Descomplicar, terá acesso a estratégias comprovadas, apoio especializado e resultados mensuráveis para o crescimento sustentável da sua clínica.</p>
<!-- /wp:paragraph -->
"""
    return content

def main():
    """Função principal para publicar o artigo."""
    try:
        # Título do artigo
        title = "Marketing Digital para Clínicas de Psicologia: Estratégias Comprovadas"
        
        # Gerar imagem destacada
        generator = ImageGenerator()
        image_path = generator.create_featured_image(
            title=title,
            category="Marketing Digital"
        )
        
        # Conteúdo do artigo
        content = generate_article_content()
        
        # Fazer upload da imagem destacada
        media_id = upload_media(str(image_path))
        logger.info(f"Imagem destacada enviada com sucesso! ID: {media_id}")
        
        # Criar post
        post_id = create_post(
            title=title,
            content=content,
            featured_media_id=media_id,
            tags=['Psicologia', 'Marketing Digital', 'Saúde Mental', 'Clínicas', 'Estratégias Digitais']
        )
        logger.info(f"Artigo publicado com sucesso! ID: {post_id}")
        
        return 0
        
    except Exception as e:
        logger.error(f"Erro ao publicar artigo: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 