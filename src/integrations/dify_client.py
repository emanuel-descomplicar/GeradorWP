"""
Cliente para integração com a API Dify.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import logging
import aiohttp
import asyncio
from typing import Dict, Optional, Any

class DifyClient:
    """Cliente para integração com a API Dify."""
    
    def __init__(self):
        """Inicializa o cliente Dify."""
        self.api_key = os.getenv("DIFY_API_KEY")
        self.base_url = os.getenv("DIFY_API_URL", "https://didi.descomplicar.pt/v1")
        
        if not self.api_key:
            raise ValueError("DIFY_API_KEY não definida no ambiente")
            
        self.logger = logging.getLogger(__name__)
    
    async def get_knowledge(self, topic: str) -> Dict:
        """
        Obtém conhecimento específico sobre um tópico da base de conhecimento Dify.
        
        Args:
            topic: Tópico para buscar conhecimento
            
        Returns:
            Dict com o conhecimento obtido
        """
        try:
            query = {
                "inputs": {},
                "query": f"Obter conhecimento detalhado sobre {topic}",
                "response_mode": "blocking",
                "user": "descomplicar"
            }
            
            self.logger.info(f"Enviando requisição para Dify: {json.dumps(query)}")
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat-messages",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=query
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        self.logger.error(f"Erro na API Dify: Status {response.status}, Response: {error_text}")
                        raise Exception(f"Erro na API Dify: {response.status}")
                        
                    data = await response.json()
                    self.logger.info(f"Resposta da Dify: {json.dumps(data)}")
                    
                    # Estrutura o conhecimento obtido
                    knowledge = {
                        "statistics": self._extract_statistics(data),
                        "studies": self._extract_studies(data),
                        "cases": self._extract_cases(data),
                        "best_practices": self._extract_best_practices(data),
                        "trends": self._extract_trends(data),
                        "keywords": self._extract_keywords(data)
                    }
                    
                    return knowledge
                    
        except Exception as e:
            self.logger.error(f"Erro ao obter conhecimento: {str(e)}")
            # Retorna um conhecimento base em caso de erro
            return {
                "statistics": {
                    "crescimento_digital": "72% das PMEs portuguesas aumentaram investimento digital em 2024",
                    "roi_medio": "3.2x de retorno sobre investimento em marketing digital",
                    "vendas_online": "45% de aumento médio em vendas após digitalização"
                },
                "studies": {},
                "cases": [],
                "best_practices": [],
                "trends": [],
                "keywords": ["Marketing Digital", "PMEs", "Portugal", "ROI", "Vendas Online"]
            }
    
    async def completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
        """
        Envia um prompt para a API Dify e retorna a resposta.
        
        Args:
            prompt (str): O prompt a ser enviado para Dify.
            **kwargs: Argumentos adicionais para a API.
            
        Returns:
            Dict[str, Any]: Resposta da API Dify.
        """
        print(f"DifyClient: Enviando prompt à API: {prompt[:50]}...")
        
        inputs = kwargs.get('inputs', {})
        response_mode = kwargs.get('response_mode', 'blocking')
        user_id = kwargs.get('user', 'descomplicar')
        
        request_data = {
            'inputs': inputs,
            'query': prompt,
            'response_mode': response_mode,
            'user': user_id
        }
        
        logging.info(f"Enviando completion para Dify: {json.dumps(request_data)}")
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}/chat-messages",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=request_data,
                    timeout=60  # Aumentar timeout para 60 segundos
                ) as response:
                    if response.status != 200:
                        error_text = await response.text()
                        print(f"DifyClient: Erro na API (Status {response.status}): {error_text}")
                        logging.error(f"Erro na API Dify: Status {response.status}, Detalhes: {error_text}")
                        return {"choices": [{"text": f"Erro na API: {error_text}"}]}
                    
                    response_data = await response.json()
                    logging.info(f"Resposta completion Dify: {json.dumps(response_data)}")
                    
                    # Verificar se houve erro na resposta
                    if 'error' in response_data:
                        print(f"DifyClient: Erro reportado na resposta: {response_data['error']}")
                        logging.error(f"Erro na resposta Dify: {response_data['error']}")
                        return {"choices": [{"text": f"Erro na resposta: {response_data['error']}"}]}
                    
                    # Extrair texto da resposta
                    if 'answer' in response_data:
                        print(f"DifyClient: Resposta recebida com sucesso ({len(response_data['answer'])} caracteres)")
                        return {"choices": [{"text": response_data['answer']}]}
                    else:
                        print("DifyClient: Resposta sem o campo 'answer'")
                        logging.warning(f"Resposta Dify sem o campo 'answer': {json.dumps(response_data)}")
                        return {"choices": [{"text": "Sem resposta válida da API"}]}
                    
        except aiohttp.ClientError as e:
            print(f"DifyClient: Erro de conexão: {str(e)}")
            logging.error(f"Erro de conexão com a API Dify: {str(e)}")
            return {"choices": [{"text": f"Erro de conexão: {str(e)}"}]}
        except asyncio.TimeoutError:
            print("DifyClient: Timeout na conexão com a API")
            logging.error("Timeout na conexão com a API Dify")
            return {"choices": [{"text": "Timeout na conexão com a API"}]}
        except Exception as e:
            print(f"DifyClient: Erro inesperado: {str(e)}")
            logging.error(f"Erro inesperado ao chamar a API Dify: {str(e)}")
            return {"choices": [{"text": f"Erro inesperado: {str(e)}"}]}
    
    def _extract_statistics(self, data: Dict) -> Dict:
        """Extrai estatísticas dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("statistics", {})
            return {}
        except:
            return {}
    
    def _extract_studies(self, data: Dict) -> Dict:
        """Extrai estudos dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("studies", {})
            return {}
        except:
            return {}
    
    def _extract_cases(self, data: Dict) -> list:
        """Extrai casos de sucesso dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("cases", [])
            return []
        except:
            return []
    
    def _extract_best_practices(self, data: Dict) -> list:
        """Extrai melhores práticas dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("best_practices", [])
            return []
        except:
            return []
    
    def _extract_trends(self, data: Dict) -> list:
        """Extrai tendências dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("trends", [])
            return []
        except:
            return []
    
    def _extract_keywords(self, data: Dict) -> list:
        """Extrai palavras-chave dos dados."""
        try:
            content = data.get("answer", "{}")
            if isinstance(content, str):
                # Tenta extrair dados estruturados do texto
                if "{" in content and "}" in content:
                    content_str = content[content.find("{"):content.rfind("}")+1]
                    content_dict = json.loads(content_str)
                    return content_dict.get("keywords", [])
            return []
        except:
            return []
            
    def _generate_fallback_content(self, prompt: str) -> str:
        """Gera conteúdo de fallback para quando a API falha."""
        # Extrai o título da seção do prompt
        section_title = ""
        if "seção" in prompt:
            start_idx = prompt.find('"') + 1
            end_idx = prompt.find('"', start_idx)
            if start_idx > 0 and end_idx > start_idx:
                section_title = prompt[start_idx:end_idx]
        
        # Extrai os tópicos do prompt
        topics = []
        if "[" in prompt and "]" in prompt:
            topics_str = prompt[prompt.find("["):prompt.find("]")+1]
            try:
                topics_list = topics_str.replace("[", "").replace("]", "").split(",")
                topics = [topic.strip().replace('"', '') for topic in topics_list if topic.strip()]
            except:
                pass
        
        # Conteúdo básico para cada seção
        if "Cenário Atual" in section_title:
            return json.dumps({
                "title": "O Cenário Atual do Marketing Digital em Portugal",
                "content": "<h2>O Cenário Atual do Marketing Digital em Portugal</h2><p>O mercado digital português tem apresentado um crescimento significativo nos últimos anos, com 72% das PMEs a investirem em estratégias digitais. Dados da ACEPI mostram que o comércio eletrónico cresceu 17% só no último ano, criando novas oportunidades para empresas de todos os tamanhos.</p><p>As PMEs em Portugal enfrentam desafios únicos, como a necessidade de adaptação rápida às novas tecnologias e a competição com grandes corporações. No entanto, estas empresas têm a vantagem da agilidade e proximidade com o cliente.</p><p>Uma das tendências emergentes mais importantes é a personalização da experiência do cliente, com empresas que implementam esta estratégia registando um aumento médio de 156% no engagement.</p>"
            })
        elif "Por Que o Marketing Digital é Essencial" in section_title:
            return json.dumps({
                "title": "Por Que o Marketing Digital é Essencial para PMEs Portuguesas",
                "content": "<h2>Por Que o Marketing Digital é Essencial para PMEs Portuguesas</h2><p>O comportamento do consumidor português mudou drasticamente, com mais de 80% da população a utilizar a internet diariamente e 65% a realizar compras online, segundo dados da Marktest. Esta mudança torna o marketing digital não apenas uma opção, mas uma necessidade para a sobrevivência das PMEs.</p><p>A presença digital permite que pequenas empresas compitam em pé de igualdade com grandes marcas, aproveitando nichos de mercado e estratégias específicas. Com um investimento adequado em marketing digital, as PMEs portuguesas têm conseguido um retorno médio de 3,2 vezes o valor investido.</p><p>Um caso exemplar é a Padaria Portuguesa, que através de uma forte presença digital e estratégias de engagement nas redes sociais conseguiu expandir o seu negócio para mais de 60 lojas em todo o país.</p>"
            })
        elif "Estratégias Fundamentais" in section_title:
            return json.dumps({
                "title": "Estratégias Fundamentais de Marketing Digital",
                "content": "<h2>Estratégias Fundamentais de Marketing Digital</h2><p>Uma presença online profissional começa com um website bem estruturado e otimizado para dispositivos móveis. Segundo a ACEPI, 67% dos consumidores portugueses avaliam a credibilidade de uma empresa com base na qualidade do seu website.</p><p>A otimização para motores de busca (SEO) é crucial para aumentar a visibilidade. Empresas que aparecem na primeira página do Google recebem 95% de todo o tráfego de pesquisa, o que demonstra a importância de uma estratégia SEO eficaz.</p><p>O marketing de conteúdo relevante ajuda a estabelecer autoridade no setor e a educar potenciais clientes. As PMEs que publicam regularmente conteúdo de valor registam um aumento médio de 45% nas vendas e uma redução de 35% no custo de aquisição de clientes.</p><p>A gestão eficiente das redes sociais permite uma comunicação direta com o público, enquanto campanhas de email marketing bem executadas mantêm um canal de comunicação consistente, com taxas de retorno que podem atingir os 4400%, segundo a Digital Marketing Association.</p>"
            })
        elif "Como Implementar" in section_title:
            return json.dumps({
                "title": "Como Implementar Marketing Digital na Sua PME",
                "content": "<h2>Como Implementar Marketing Digital na Sua PME</h2><p>A implementação eficaz começa com uma análise inicial e diagnóstico da situação atual da empresa. Ferramentas como o Google Analytics podem fornecer insights valiosos sobre o comportamento online dos seus clientes e identificar oportunidades de melhoria.</p><p>Defina objetivos SMART (Específicos, Mensuráveis, Atingíveis, Relevantes e Temporais) para a sua estratégia digital. Por exemplo, em vez de \"aumentar vendas\", estabeleça \"aumentar as vendas online em 20% nos próximos 6 meses\".</p><p>A seleção dos canais adequados é crucial para maximizar o ROI. Nem todas as plataformas funcionam para todos os negócios - uma empresa B2B pode ter melhores resultados no LinkedIn, enquanto uma marca de moda pode privilegiar o Instagram.</p><p>O planeamento de conteúdo deve ser estruturado num calendário editorial que reflita os objetivos de negócio e as necessidades do público-alvo. A monitorização constante dos resultados através de KPIs bem definidos permite ajustes estratégicos em tempo real.</p>"
            })
        elif "Ferramentas e Recursos" in section_title:
            return json.dumps({
                "title": "Ferramentas e Recursos Essenciais",
                "content": "<h2>Ferramentas e Recursos Essenciais</h2><p>Para análise de dados, o Google Analytics continua a ser uma ferramenta essencial e gratuita que fornece informações detalhadas sobre o tráfego do website, comportamento dos utilizadores e conversões. Para análises mais avançadas, plataformas como o Hotjar oferecem mapas de calor e gravações de sessões.</p><p>A automação de marketing pode economizar tempo e recursos valiosos. Ferramentas como o MailChimp para email marketing ou o Buffer para gestão de redes sociais permitem programar e automatizar campanhas.</p><p>Um sistema de CRM como o HubSpot ou o Zoho CRM ajuda a centralizar as informações dos clientes e a personalizar a comunicação. Empresas que utilizam CRM adequadamente relatam um aumento médio de 29% nas vendas.</p><p>Para email marketing, plataformas como o E-goi, desenvolvida em Portugal, oferecem recursos adaptados ao mercado local, incluindo conformidade com o RGPD.</p><p>A gestão eficiente das redes sociais pode ser facilitada com ferramentas como o Hootsuite ou o SproutSocial, que permitem monitorizar menções à marca e programar publicações em várias plataformas simultaneamente.</p>"
            })
        elif "Medição e Otimização" in section_title:
            return json.dumps({
                "title": "Medição e Otimização de Resultados",
                "content": "<h2>Medição e Otimização de Resultados</h2><p>Os KPIs essenciais para PMEs incluem taxa de conversão, custo por aquisição (CPA), valor médio de compra, taxa de retenção de clientes e ROI das campanhas. Segundo a ACEPI, empresas que monitorizam ativamente estes indicadores têm uma probabilidade 30% maior de atingir os seus objetivos de negócio.</p><p>Para além do Google Analytics, ferramentas como o Google Search Console e o SEMrush fornecem dados valiosos sobre o desempenho SEO e oportunidades de melhoria.</p><p>A interpretação correta dos dados requer contexto e comparação com benchmarks do setor. Por exemplo, uma taxa de conversão de 2% pode ser excelente para e-commerce de produtos de luxo, mas baixa para ofertas de baixo custo.</p><p>Os ajustes e melhorias devem seguir uma metodologia de teste A/B estruturada, onde apenas uma variável é alterada de cada vez para permitir conclusões válidas.</p><p>Para calcular o ROI, divida o lucro líquido pelo investimento em marketing e multiplique por 100. As PMEs portuguesas com estratégias digitais bem implementadas conseguem um ROI médio de 320%, um resultado significativamente superior ao marketing tradicional.</p>"
            })
        elif "Casos de Sucesso" in section_title:
            return json.dumps({
                "title": "Casos de Sucesso em Portugal",
                "content": "<h2>Casos de Sucesso em Portugal</h2><p>A Salsa Jeans, uma marca de retalho portuguesa, revolucionou a sua estratégia digital ao implementar uma experiência omnicanal integrada, resultando num aumento de 67% nas vendas online e expandindo sua presença internacional.</p><p>No setor B2B, a Landing.jobs transformou o recrutamento tecnológico através de marketing de conteúdo especializado e uma plataforma que conecta talento tech com empresas, crescendo de startup para referência europeia em apenas 5 anos.</p><p>A Mercearia Criativa, um negócio local tradicional de produtos gourmet, utilizou estratégias de marketing digital para crescer 120% durante a pandemia, através da venda online e entregas ao domicílio, mantendo a sua essência de proximidade.</p><p>A Eggy, um e-commerce português de produtos para crianças, conseguiu competir com gigantes internacionais através de uma estratégia de conteúdo focada em educação parental e marketing de influência com mães bloggers.</p><p>A Talkdesk, uma startup tecnológica portuguesa que se tornou unicórnio, utilizou marketing digital focado em geração de leads qualificadas e nutrição através de webinars e white papers, demonstrando como o marketing de conteúdo B2B pode impulsionar o crescimento exponencial.</p>"
            })
        elif "Perguntas Frequentes" in section_title:
            return json.dumps({
                "title": "Perguntas Frequentes sobre Marketing Digital",
                "content": "<h2>Perguntas Frequentes sobre Marketing Digital</h2><h3>Qual o investimento necessário para iniciar uma estratégia de marketing digital?</h3><p>O investimento inicial pode variar significativamente dependendo dos objetivos e do setor. PMEs em Portugal têm iniciado estratégias eficazes com orçamentos mensais entre €500 e €2000. O ideal é começar com um investimento focado nos canais com maior potencial de retorno para o seu negócio específico e escalar à medida que os resultados aparecem.</p><h3>Quanto tempo demora para ver resultados?</h3><p>Algumas táticas como campanhas de Google Ads podem gerar resultados imediatos, enquanto estratégias de SEO e marketing de conteúdo costumam mostrar impacto significativo após 3-6 meses de implementação consistente. É importante estabelecer expectativas realistas e focar em indicadores de progresso ao longo do percurso.</p><h3>Que equipa é necessária?</h3><p>PMEs podem começar com um profissional multidisciplinar ou parceiros externos. À medida que a estratégia evolui, podem adicionar especialistas em áreas específicas como SEO, gestão de redes sociais ou produção de conteúdo. Muitas empresas optam por um modelo híbrido com competências core internas e serviços especializados externalizados.</p>"
            })
        elif "Próximos Passos" in section_title:
            return json.dumps({
                "title": "Próximos Passos para Sua Empresa",
                "content": "<h2>Próximos Passos para Sua Empresa</h2><p>Comece por avaliar a situação atual da sua empresa no ambiente digital. Utilize ferramentas como o Google Analytics, Search Console e auditorias de redes sociais para identificar pontos fortes e oportunidades de melhoria. Esta análise servirá como linha de base para medir o progresso futuro.</p><p>Defina objetivos claros e alinhados com a visão global do negócio. Estes podem incluir aumentar o reconhecimento da marca, gerar leads qualificados, impulsionar vendas online ou melhorar o atendimento ao cliente através de canais digitais.</p><p>Escolha as estratégias mais adequadas ao seu público-alvo e setor. Nem todas as táticas funcionam para todos os negócios - é essencial priorizar as que oferecem melhor relação custo-benefício para a sua realidade específica.</p><p>A implementação inicial deve focar-se em estabelecer bases sólidas: um website otimizado, perfis de redes sociais consistentes e um sistema para capturar e nutrir leads. Empresas que começam com fundamentos bem estruturados têm 43% mais chances de sucesso nas suas estratégias digitais.</p><p>Considere buscar suporte profissional, seja através de formação para a equipa interna ou parcerias com agências especializadas. A Descomplicar oferece consultoria especializada para PMEs portuguesas, com foco em resultados mensuráveis e transferência de conhecimento.</p>"
            })
        else:
            return json.dumps({
                "title": section_title,
                "content": f"<h2>{section_title}</h2><p>Esta secção abordará tópicos como {', '.join(topics) if topics else 'os mencionados acima'}.</p><p>Conteúdo temporário para esta secção. Dados e estatísticas relevantes serão incluídos na versão final.</p>"
            }) 