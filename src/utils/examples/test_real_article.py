"""
Teste do validador ACIDA com um artigo real.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

from ..validators import ACIDAValidator, validate_html_structure

def main():
    # Artigo real sobre "Inteligência Artificial para PMEs"
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

        Neste artigo, vamos explorar casos reais de sucesso em Portugal, analisar as melhores práticas de implementação e 
        apresentar soluções concretas para os desafios mais comuns enfrentados pelas PMEs na adoção da IA.
        </section>
        """,
        
        'confidence': """
        <section class="confidence">
        A implementação bem-sucedida de IA em PMEs portuguesas já é uma realidade comprovada. De acordo com o estudo 
        "Transformação Digital em Portugal 2024" da ACEPI, as empresas que adotaram soluções de IA reportaram um aumento 
        médio de 32% na produtividade e uma redução de 28% nos custos operacionais.

        O Centro de Competências em IA do Instituto Superior Técnico destaca três casos notáveis:

        1. Uma empresa têxtil do Norte que implementou IA para otimização de corte e redução de desperdício, alcançando 
        uma redução de 45% nas perdas de material.

        2. Uma distribuidora alimentar que utiliza IA para previsão de demanda e gestão de stock, reduzindo o desperdício 
        em 35% e melhorando a precisão das previsões em 89%.

        3. Uma empresa de serviços que automatizou o atendimento ao cliente com IA, aumentando a satisfação dos clientes 
        em 42% e reduzindo o tempo de resposta em 67%.

        Segundo o Dr. António Silva, diretor do Laboratório de IA da Universidade do Porto, "A implementação de IA em PMEs 
        portuguesas não é apenas uma questão de tecnologia, mas de sobrevivência competitiva no mercado global."
        </section>
        """,
        
        'interest': """
        <section class="interest">
        Os benefícios da implementação de IA em PMEs são tangíveis e mensuráveis. Vamos analisar as principais áreas de 
        impacto e como a Descomplicar tem ajudado empresas a alcançar resultados significativos:

        1. Automação de Processos:
        - Redução de 40% no tempo gasto em tarefas administrativas
        - Diminuição de 60% nos erros de processamento
        - Economia média de 25 horas semanais por departamento

        2. Análise Preditiva:
        - Aumento de 45% na precisão de previsões de vendas
        - Redução de 30% em custos de inventário
        - Melhoria de 55% na gestão de recursos

        3. Atendimento ao Cliente:
        - Disponibilidade 24/7 com chatbots inteligentes
        - Redução de 70% no tempo de resposta
        - Aumento de 38% na satisfação do cliente

        A Descomplicar tem implementado soluções personalizadas que se adaptam à realidade de cada empresa. Por exemplo, 
        desenvolvemos um sistema de IA para uma empresa de retalho que:
        - Automatizou 85% das respostas a consultas de clientes
        - Reduziu custos operacionais em 40%
        - Aumentou as vendas online em 65%

        Outro caso de sucesso foi uma empresa de serviços que, através das nossas soluções de IA:
        - Otimizou a alocação de recursos em 75%
        - Reduziu o tempo de processamento de pedidos em 60%
        - Aumentou a produtividade geral em 45%
        </section>
        """,
        
        'decision': """
        <section class="decision">
        Para implementar IA na sua PME, considere os seguintes passos essenciais:

        1. Avaliação Inicial:
        - Análise completa dos processos atuais
        - Identificação de áreas prioritárias para automação
        - Avaliação de recursos necessários

        2. Planeamento Estratégico:
        - Definição de objetivos claros
        - Estabelecimento de métricas de sucesso
        - Desenvolvimento de cronograma realista

        3. Implementação Faseada:
        - Início com projetos piloto
        - Expansão gradual para outras áreas
        - Formação contínua da equipa

        A Descomplicar oferece soluções adaptadas a diferentes necessidades e orçamentos:
        - Consultoria Estratégica em IA
        - Implementação de Sistemas Automatizados
        - Formação e Suporte Contínuo

        Recursos Necessários:
        - Investimento inicial a partir de 5.000€
        - Equipa dedicada para formação
        - 2-3 meses para implementação inicial
        </section>
        """,
        
        'action': """
        <section class="action">
        A Inteligência Artificial não é mais um luxo, mas uma necessidade competitiva para PMEs portuguesas. Com o suporte 
        adequado, a implementação pode ser mais simples e acessível do que imagina.

        Para começar a sua jornada de transformação digital:
        1. Agende uma consulta gratuita em <a href="https://descomplicar.pt/marcar-reuniao/">https://descomplicar.pt/marcar-reuniao/</a>
        2. Solicite uma proposta personalizada em <a href="https://descomplicar.pt/pedido-de-orcamento/">https://descomplicar.pt/pedido-de-orcamento/</a>
        3. Fale diretamente com nossa equipa em <a href="https://descomplicar.pt/contacto/">https://descomplicar.pt/contacto/</a>

        Não deixe sua empresa para trás na revolução da IA. A Descomplicar está pronta para ajudar você a dar o próximo passo.
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