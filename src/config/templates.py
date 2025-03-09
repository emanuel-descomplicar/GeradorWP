"""
Templates de prompts para geração de conteúdo.

/**
 * Autor: Descomplicar - Agência de Aceleração Digital
 * https://descomplicar.pt
 */
"""

# Template ACIDA para estruturação de conteúdo
ACIDA_TEMPLATE = """
Estruture o seguinte conteúdo seguindo o formato ACIDA (Atenção, Contexto, Interesse, Desejo, Ação).

Conteúdo original:
{content}

Regras:

1. Estrutura ACIDA:
   - Atenção (200-300 palavras):
     * Estatísticas impactantes sobre o mercado português
     * Perguntas retóricas relevantes
     * Contexto atual do tema em Portugal
   
   - Contexto (400-500 palavras):
     * Dados e informações do mercado português
     * Citações de especialistas portugueses
     * Referências a instituições portuguesas
   
   - Interesse (500-600 palavras):
     * Benefícios tangíveis para o público português
     * Exemplos práticos do mercado local
     * Casos de estudo portugueses
   
   - Desejo (400-500 palavras):
     * Passos concretos para implementação
     * Recursos necessários em Portugal
     * Considerações específicas do mercado
   
   - Ação (150-200 palavras):
     * Conclusão persuasiva
     * CTA claro e direto
     * Próximos passos práticos

2. Formatação HTML:
   <article class="post-content">
     <section class="section-attention">
       <h2>Título Chamativo</h2>
       <p>Conteúdo de atenção...</p>
     </section>
     
     <section class="section-context">
       <h2>Contexto Atual</h2>
       <p>Conteúdo de contexto...</p>
     </section>
     
     <section class="section-interest">
       <h2>Benefícios e Vantagens</h2>
       <p>Conteúdo de interesse...</p>
     </section>
     
     <section class="section-desire">
       <h2>Como Implementar</h2>
       <p>Conteúdo de desejo...</p>
     </section>
     
     <section class="section-action">
       <h2>Próximos Passos</h2>
       <p>Conteúdo de ação...</p>
     </section>
   </article>

3. Elementos HTML:
   - Use <strong> para destacar pontos importantes
   - Use <em> para ênfase
   - Use <ul> e <li> para listas
   - Use <blockquote> para citações
   - Use <a> para links relevantes

4. SEO e Conteúdo:
   - Use português de Portugal (evite brasileirismos)
   - Mantenha parágrafos curtos (2-3 frases)
   - Distribua palavras-chave naturalmente
   - Use exemplos do mercado português
   - Mantenha tom profissional mas acessível

Retorne apenas o conteúdo estruturado em HTML, sem explicações adicionais.
"""

# Template para CTAs
CTA_TEMPLATE = """
Adicione um Call-to-Action profissional ao final do seguinte conteúdo.

Tipo de CTA: {cta_type}
{cta_text}

Conteúdo original:
{content}

Regras:

1. Estrutura HTML:
<div class="cta-box cta-{cta_type}">
  <h3 class="cta-title">Título Persuasivo</h3>
  <div class="cta-content">
    <p class="cta-description">Descrição convincente</p>
    <div class="cta-benefits">
      <ul>
        <li>Benefício 1</li>
        <li>Benefício 2</li>
        <li>Benefício 3</li>
      </ul>
    </div>
    <div class="cta-action">
      <a href="#" class="cta-button">Texto do Botão</a>
    </div>
  </div>
</div>

2. Conteúdo:
   - Use português de Portugal
   - Seja direto e persuasivo
   - Foque no benefício principal
   - Use verbos de ação
   - Crie senso de urgência
   - Mantenha tom profissional

3. Tipos de CTA:
   - consultoria: Foco em agendamento de consulta
   - servicos: Foco em contratação de serviços
   - newsletter: Foco em inscrição na newsletter
   - download: Foco em download de material
   - contacto: Foco em entrar em contacto

Retorne apenas o HTML do CTA, sem explicações adicionais.
"""

# Template para formatação HTML
HTML_TEMPLATE = """
Formate o seguinte conteúdo em HTML semântico e otimizado.

Conteúdo original:
{content}

Regras:

1. Estrutura Base:
<article class="post-content">
  <header class="post-header">
    <h1 class="post-title">{title}</h1>
    <div class="post-meta">
      <span class="post-category">{category}</span>
      <span class="post-date">{date}</span>
    </div>
  </header>
  
  <div class="post-body">
    {content}
  </div>
  
  <footer class="post-footer">
    <div class="post-tags">
      {tags}
    </div>
    {cta}
  </footer>
</article>

2. Elementos Semânticos:
   - Use <section> para seções principais
   - Use <aside> para conteúdo relacionado
   - Use <figure> para imagens com legenda
   - Use <nav> para navegação interna
   - Use <main> para conteúdo principal

3. Acessibilidade:
   - Adicione ARIA labels
   - Use alt text em imagens
   - Mantenha hierarquia de títulos
   - Garanta contraste adequado
   - Siga WCAG 2.1

4. SEO:
   - Use meta tags relevantes
   - Estruture URLs amigáveis
   - Otimize títulos e descrições
   - Adicione schema markup
   - Use canonical URLs

5. Performance:
   - Minimize HTML
   - Use lazy loading
   - Otimize imagens
   - Reduza requisições
   - Cache recursos estáticos

Retorne apenas o HTML formatado, sem explicações adicionais.
""" 