"""
Template para geração de artigos seguindo o modelo ACIDA.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

ARTICLE_TEMPLATE = """
<!-- wp:heading {"level":1} -->
<h1>{title}</h1>
<!-- /wp:heading -->

<!-- wp:paragraph {"className":"article-intro"} -->
<p>{meta_description}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"className":"section-a"} -->
<h2>O Cenário Atual de {topic}</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{attention_intro}</p>
<!-- /wp:paragraph -->

<!-- wp:image {{"id":{infographic_1_id},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large">
    <img src="{infographic_1_url}" alt="Estatísticas sobre {topic} em Portugal" class="wp-image-{infographic_1_id}"/>
    <figcaption>Dados atualizados sobre {topic} em Portugal. Fontes: {infographic_1_sources}</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:paragraph -->
<p>{attention_context}</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph {"className":"sources-list"} -->
<p><strong>Fontes Oficiais:</strong></p>
<ul>
    <li>📊 INE - Instituto Nacional de Estatística: {ine_link}</li>
    <li>📈 PORDATA - Base de Dados Portugal Contemporâneo: {pordata_link}</li>
    <li>🇪🇺 Eurostat - Estatísticas Europeias: {eurostat_link}</li>
    <li>💼 IAPMEI - Agência para a Competitividade e Inovação: {iapmei_link}</li>
    <li>📱 GEE - Gabinete de Estratégia e Estudos: {gee_link}</li>
    <li>🏢 Portugal 2020/Portugal 2030: {pt2030_link}</li>
    <li>🌐 Comissão Europeia - Digital Economy and Society Index: {desi_link}</li>
    <li>📑 Banco de Portugal - Análises Setoriais: {bdp_link}</li>
</ul>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="cta-box initial" style="background-color: #f2d9a2; padding: 30px; margin: 20px 0; border-radius: 5px;">
    <h3>Precisa de ajuda com {topic}?</h3>
    <p>A Descomplicar oferece soluções especializadas para:</p>
    <ul style="list-style-type: none; padding-left: 0;">
        <li>✓ {service_a}: {problem_solution_a}</li>
        <li>✓ {service_b}: {problem_solution_b}</li>
        <li>✓ {service_c}: {problem_solution_c}</li>
    </ul>
    <div class="cta-buttons" style="margin-top: 20px;">
        <a href="https://descomplicar.pt/marcar-reuniao/" class="btn btn-primary">Marcar Reunião</a>
        <a href="https://descomplicar.pt/pedido-de-orcamento/" class="btn btn-secondary">Pedir Orçamento</a>
        <a href="https://descomplicar.pt/contacto/" class="btn btn-secondary">Contactar</a>
    </div>
</div>
<!-- /wp:html -->

<!-- wp:heading {"className":"section-c"} -->
<h2>Fundamentos e Evidências</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{confidence_intro}</p>
<!-- /wp:paragraph -->

<!-- wp:table -->
{comparison_table}
<!-- /wp:table -->

<!-- wp:paragraph -->
<p>{confidence_analysis}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"className":"section-i"} -->
<h2>Benefícios e Aplicações Práticas</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{interest_intro}</p>
<!-- /wp:paragraph -->

<!-- wp:columns -->
<div class="wp-block-columns">
    {benefit_columns}
</div>
<!-- /wp:columns -->

<!-- wp:image {{"id":{infographic_2_id},"sizeSlug":"large"}} -->
<figure class="wp-block-image size-large">
    <img src="{infographic_2_url}" alt="Processo de implementação de {topic}" class="wp-image-{infographic_2_id}"/>
    <figcaption>Processo de implementação de {topic}. Fonte: Descomplicar</figcaption>
</figure>
<!-- /wp:image -->

<!-- wp:heading {"className":"section-d"} -->
<h2>Implementação Passo a Passo</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{desire_intro}</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol>
    {implementation_steps}
</ol>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>{desire_conclusion}</p>
<!-- /wp:paragraph -->

<!-- wp:heading {"level":3} -->
<h3>Casos de Sucesso</h3>
<!-- /wp:heading -->

<!-- wp:columns -->
<div class="wp-block-columns">
    {case_studies}
</div>
<!-- /wp:columns -->

<!-- wp:heading {"className":"section-faq"} -->
<h2>Perguntas Frequentes sobre {topic}</h2>
<!-- /wp:heading -->

{faq_section}

<!-- wp:heading {"className":"section-conclusion"} -->
<h2>Conclusão e Próximos Passos</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{action_summary}</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
<div class="cta-box final" style="padding: 30px; margin: 20px 0; border-radius: 5px; background-color: #f5f5f5;">
    <h3>Pronto para implementar {topic} no seu negócio?</h3>
    <p>A Descomplicar está preparada para ajudar a sua empresa a alcançar resultados reais com {topic}. Podemos começar com uma conversa para entender as suas necessidades específicas e desenvolver um plano personalizado.</p>
    <p>Para dar o próximo passo:</p>
    <ul>
        <li><a href="https://descomplicar.pt/marcar-reuniao/">Agende uma consulta gratuita</a> com os nossos especialistas</li>
        <li><a href="https://descomplicar.pt/pedido-de-orcamento/">Solicite um orçamento personalizado</a> para o seu projeto</li>
        <li><a href="https://descomplicar.pt/contacto/">Entre em contacto</a> para esclarecer suas dúvidas</li>
    </ul>
</div>
<!-- /wp:html -->
"""

# Templates para seções específicas
BENEFIT_COLUMN_TEMPLATE = """
<!-- wp:column -->
<div class="wp-block-column">
    <!-- wp:heading {"level":4} -->
    <h4>{benefit_title}</h4>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p>{benefit_description}</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:list -->
    <ul>
        {benefit_items}
    </ul>
    <!-- /wp:list -->
</div>
<!-- /wp:column -->
"""

CASE_STUDY_TEMPLATE = """
<!-- wp:column -->
<div class="wp-block-column">
    <!-- wp:heading {"level":4} -->
    <h4>{company_name}</h4>
    <!-- /wp:heading -->
    
    <!-- wp:paragraph -->
    <p>{challenge}</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:paragraph -->
    <p>{solution}</p>
    <!-- /wp:paragraph -->
    
    <!-- wp:paragraph -->
    <p><strong>Resultados:</strong> {results}</p>
    <!-- /wp:paragraph -->
</div>
<!-- /wp:column -->
"""

FAQ_ITEM_TEMPLATE = """
<!-- wp:heading {"level":3} -->
<h3>{question}</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>{answer}</p>
<!-- /wp:paragraph -->
"""

COMPARISON_TABLE_TEMPLATE = """
<table class="wp-block-table">
    <thead>
        <tr>
            <th>Aspecto</th>
            <th>Antes</th>
            <th>Depois de {topic}</th>
        </tr>
    </thead>
    <tbody>
        {table_rows}
    </tbody>
</table>
""" 