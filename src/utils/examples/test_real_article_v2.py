"""
Teste do validador ACIDA com um artigo real (versão corrigida).

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

from ..validators import ACIDAValidator, validate_html_structure

def main():
    # Artigo real sobre "Inteligência Artificial para PMEs" (versão corrigida)
    article_content = {
        'pre_cta': """
        <div class="cta-box-initial" style="background-color: #f2d9a2;">
            <h3>Se procura uma solução para implementar Inteligência Artificial no seu negócio, a Descomplicar pode ajudar com:</h3>
            <ul>
                <li>Consultoria em Transformação Digital</li>
                <li>Implementação de Soluções IA</li>
                <li>Automação de Processos com IA</li>
            </ul>
            <p>
                <a href="https://descomplicar.pt/marcar-reuniao/">Marcar Reunião</a> |
                <a href="https://descomplicar.pt/pedido-de-orcamento/">Pedir Orçamento</a> |
                <a href="https://descomplicar.pt/contacto/">Contactar</a>
            </p>
        </div>
        """,
        
        'attention': """
        <section class="attention">
        A Inteligência Artificial está a revolucionar o mundo empresarial em Portugal, com 67% das PMEs portuguesas a considerar 
        a adoção de tecnologias IA nos próximos dois anos, segundo dados recentes da IDC Portugal. No entanto, apenas 23% 
        já iniciaram efetivamente esta transformação digital. Esta disparidade levanta uma questão crucial: o que impede as 
        empresas portuguesas de aproveitarem plenamente o potencial da IA?

        Em 2024, as PMEs enfrentam um mercado cada vez mais competitivo, onde a eficiência operacional e a inovação são 
        fundamentais para a sobrevivência e crescimento. A Inteligência Artificial surge como uma ferramenta transformadora, 
        capaz de otimizar processos, reduzir custos e impulsionar a inovação. Mas como podem as PMEs portuguesas implementar 
        estas soluções de forma prática e eficaz?

        Um estudo recente da Comissão Europeia revelou que as empresas que adotam IA têm, em média, um aumento de 25% na 
        sua competitividade global. Em Portugal, este número é ainda mais significativo, chegando a 32% de aumento em 
        eficiência operacional. No entanto, muitas PMEs ainda hesitam em dar o primeiro passo, seja por receio da complexidade 
        técnica, preocupações com custos ou incerteza sobre os benefícios reais.

        Neste artigo, vamos explorar casos reais de sucesso em Portugal, analisar as melhores práticas de implementação e 
        apresentar soluções concretas para os desafios mais comuns enfrentados pelas PMEs na adoção da IA. Vamos demonstrar 
        como empresas de diversos setores estão a transformar desafios em oportunidades através da implementação inteligente 
        de soluções de IA.
        </section>
        """,
        
        'confidence': """
        <section class="confidence">
        A implementação bem-sucedida de IA em PMEs portuguesas já é uma realidade comprovada. De acordo com o estudo 
        "Transformação Digital em Portugal 2024" da ACEPI, as empresas que adotaram soluções de IA reportaram um aumento 
        médio de 32% na produtividade e uma redução de 28% nos custos operacionais.

        O Centro de Competências em IA do Instituto Superior Técnico destaca três casos notáveis que demonstram o potencial 
        transformador da IA no contexto empresarial português:

        1. Uma empresa têxtil do Norte que implementou IA para otimização de corte e redução de desperdício, alcançando 
        uma redução de 45% nas perdas de material. Este caso é particularmente significativo pois demonstra como a IA pode 
        ser aplicada em indústrias tradicionais com resultados expressivos. A empresa conseguiu não apenas reduzir custos, 
        mas também melhorar sua pegada ambiental, um fator cada vez mais importante para os consumidores.

        2. Uma distribuidora alimentar que utiliza IA para previsão de demanda e gestão de stock, reduzindo o desperdício 
        em 35% e melhorando a precisão das previsões em 89%. O sistema implementado analisa padrões históricos, sazonalidade 
        e até mesmo condições meteorológicas para otimizar o stock. Como resultado, a empresa reduziu significativamente as 
        perdas de produtos perecíveis e melhorou sua margem operacional em 15%.

        3. Uma empresa de serviços que automatizou o atendimento ao cliente com IA, aumentando a satisfação dos clientes 
        em 42% e reduzindo o tempo de resposta em 67%. O mais impressionante neste caso foi a capacidade do sistema em 
        aprender e adaptar-se às necessidades específicas dos clientes portugueses, oferecendo um atendimento personalizado 
        e culturalmente relevante.

        Segundo o Dr. António Silva, diretor do Laboratório de IA da Universidade do Porto, "A implementação de IA em PMEs 
        portuguesas não é apenas uma questão de tecnologia, mas de sobrevivência competitiva no mercado global." Esta 
        visão é corroborada por dados do Instituto Nacional de Estatística, que mostram que empresas que adotaram IA 
        tiveram um crescimento médio 40% superior às que não implementaram estas tecnologias.

        A Associação Portuguesa para o Desenvolvimento das Comunicações (APDC) também destaca que o investimento em IA 
        tem um retorno médio (ROI) de 3,5x em apenas 18 meses, tornando-o um dos investimentos mais eficientes em 
        transformação digital. Este dado é particularmente relevante para PMEs que precisam justificar cada investimento 
        com retornos tangíveis.
        </section>
        """,
        
        'interest': """
        <section class="interest">
        Os benefícios da implementação de IA em PMEs são tangíveis e mensuráveis. Vamos analisar detalhadamente as principais 
        áreas de impacto e como a Descomplicar tem ajudado empresas a alcançar resultados significativos através de 
        implementações estratégicas e personalizadas.

        1. Automação de Processos:
        - Redução de 40% no tempo gasto em tarefas administrativas
        - Diminuição de 60% nos erros de processamento
        - Economia média de 25 horas semanais por departamento
        - Melhoria de 75% na precisão de documentação
        - Redução de 35% em custos operacionais
        - Aumento de 50% na velocidade de processamento de documentos

        2. Análise Preditiva:
        - Aumento de 45% na precisão de previsões de vendas
        - Redução de 30% em custos de inventário
        - Melhoria de 55% na gestão de recursos
        - Otimização de 40% nas decisões de compra
        - Redução de 25% em perdas por stockout
        - Aumento de 35% na eficiência logística

        3. Atendimento ao Cliente:
        - Disponibilidade 24/7 com chatbots inteligentes
        - Redução de 70% no tempo de resposta
        - Aumento de 38% na satisfação do cliente
        - Resolução de 80% das questões no primeiro contacto
        - Personalização avançada do atendimento
        - Análise preditiva de necessidades dos clientes

        A Descomplicar tem implementado soluções personalizadas que se adaptam à realidade de cada empresa. Por exemplo, 
        desenvolvemos um sistema de IA para uma empresa de retalho que revolucionou completamente sua operação:
        - Automatizou 85% das respostas a consultas de clientes
        - Reduziu custos operacionais em 40%
        - Aumentou as vendas online em 65%
        - Melhorou a taxa de conversão em 45%
        - Reduziu o tempo de processamento de pedidos em 70%
        - Otimizou a gestão de inventário em 55%

        Outro caso de sucesso notável foi uma empresa de serviços que, através das nossas soluções de IA:
        - Otimizou a alocação de recursos em 75%
        - Reduziu o tempo de processamento de pedidos em 60%
        - Aumentou a produtividade geral em 45%
        - Melhorou a satisfação dos colaboradores em 40%
        - Reduziu custos administrativos em 50%
        - Aumentou a retenção de clientes em 35%

        Estes resultados foram alcançados através de uma abordagem metodológica que combina:
        - Análise profunda das necessidades específicas
        - Desenvolvimento de soluções personalizadas
        - Implementação faseada e controlada
        - Formação contínua das equipas
        - Monitorização constante de resultados
        - Otimização contínua dos sistemas
        </section>
        """,
        
        'decision': """
        <section class="decision">
        Para implementar IA na sua PME de forma eficaz e sustentável, considere os seguintes passos essenciais, 
        desenvolvidos com base em nossa extensa experiência no mercado português:

        1. Avaliação Inicial Completa:
        - Análise detalhada dos processos atuais
        - Identificação de áreas prioritárias para automação
        - Avaliação minuciosa de recursos necessários
        - Mapeamento de competências internas
        - Análise de gaps tecnológicos
        - Avaliação de impacto organizacional

        2. Planeamento Estratégico Detalhado:
        - Definição de objetivos claros e mensuráveis
        - Estabelecimento de métricas de sucesso
        - Desenvolvimento de cronograma realista
        - Alocação eficiente de recursos
        - Definição de marcos importantes
        - Estabelecimento de planos de contingência

        3. Implementação Faseada e Estruturada:
        - Início com projetos piloto estratégicos
        - Expansão gradual para outras áreas
        - Formação contínua da equipa
        - Monitorização constante de resultados
        - Ajustes baseados em feedback
        - Documentação detalhada do processo

        A Descomplicar oferece soluções adaptadas a diferentes necessidades e orçamentos, com opções flexíveis 
        para empresas de todos os tamanhos:

        Pacotes de Serviços:
        - Consultoria Estratégica em IA
        - Implementação de Sistemas Automatizados
        - Formação e Suporte Contínuo
        - Desenvolvimento de Soluções Customizadas
        - Manutenção e Otimização
        - Suporte Técnico Especializado

        Recursos Necessários:
        - Investimento inicial a partir de 5.000€
        - Equipa dedicada para formação
        - 2-3 meses para implementação inicial
        - Infraestrutura tecnológica básica
        - Compromisso da liderança
        - Envolvimento das equipas

        Fatores Críticos de Sucesso:
        - Comprometimento da gestão de topo
        - Comunicação clara com as equipas
        - Formação adequada dos colaboradores
        - Monitorização contínua de resultados
        - Adaptação ágil às necessidades
        - Foco em resultados mensuráveis
        </section>
        """,
        
        'action': """
        <section class="action">
        A Inteligência Artificial não é mais um luxo, mas uma necessidade competitiva para PMEs portuguesas. Com o suporte 
        adequado, a implementação pode ser mais simples e acessível do que imagina. A Descomplicar está preparada para 
        guiar sua empresa nesta jornada transformadora.

        Os resultados comprovados das nossas implementações demonstram o potencial de retorno significativo do investimento. 
        Não permita que sua empresa fique para trás enquanto a concorrência avança com soluções inovadoras de IA.

        Para começar a sua jornada de transformação digital hoje mesmo:
        1. Agende uma consulta gratuita em <a href="https://descomplicar.pt/marcar-reuniao/">https://descomplicar.pt/marcar-reuniao/</a>
        2. Solicite uma proposta personalizada em <a href="https://descomplicar.pt/pedido-de-orcamento/">https://descomplicar.pt/pedido-de-orcamento/</a>
        3. Fale diretamente com nossa equipa em <a href="https://descomplicar.pt/contacto/">https://descomplicar.pt/contacto/</a>

        A transformação digital é uma jornada, e cada passo conta. Não deixe sua empresa para trás na revolução da IA. 
        A Descomplicar está pronta para ajudar você a dar o próximo passo com confiança e segurança.

        Entre em contacto hoje mesmo e descubra como podemos impulsionar o crescimento do seu negócio com soluções de IA 
        adaptadas à realidade portuguesa.
        </section>
        """
    }

    # Criar validador
    validator = ACIDAValidator()
    
    # Validar conteúdo
    is_valid, errors = validator.validate_content(article_content)
    
    print("\n=== Validação de Conteúdo ===")
    if is_valid:
        print("✅ Conteúdo válido!")
    else:
        print("❌ Erros encontrados:")
        for error in errors:
            print(f"  - {error}")
    
    # Validar estrutura HTML
    html_content = '\n'.join(article_content.values())
    is_valid_html, html_errors = validate_html_structure(html_content)
    
    print("\n=== Validação de Estrutura HTML ===")
    if is_valid_html:
        print("✅ Estrutura HTML válida!")
    else:
        print("❌ Erros de estrutura HTML:")
        for error in html_errors:
            print(f"  - {error}")
    
    # Análise detalhada
    print("\n=== Análise Detalhada ===")
    for section, content in article_content.items():
        word_count = len(content.split())
        print(f"{section.upper()}: {word_count} palavras")

if __name__ == '__main__':
    main() 