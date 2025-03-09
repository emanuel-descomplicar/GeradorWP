"""
Configurações para geração de conteúdo.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

from typing import Dict, List

# Configurações do modelo ACIDA
ACIDA_CONFIG = {
    'attention': {
        'min_words': 200,
        'max_words': 300,
        'elements': [
            'estatísticas_impactantes',
            'contexto_português',
            'perguntas_retóricas',
            'problema_central'
        ]
    },
    'confidence': {
        'min_words': 400,
        'max_words': 500,
        'elements': [
            'dados_mercado',
            'casos_sucesso',
            'citações_especialistas',
            'estudos_pesquisas'
        ]
    },
    'interest': {
        'min_words': 500,
        'max_words': 600,
        'elements': [
            'benefícios_tangíveis',
            'exemplos_práticos',
            'casos_estudo',
            'resultados_mensuráveis'
        ]
    },
    'decision': {
        'min_words': 400,
        'max_words': 500,
        'elements': [
            'passos_implementação',
            'recursos_necessários',
            'considerações_importantes',
            'soluções_descomplicar'
        ]
    },
    'action': {
        'min_words': 150,
        'max_words': 200,
        'elements': [
            'conclusão_persuasiva',
            'chamada_ação',
            'próximos_passos',
            'links_contato'
        ]
    }
}

# Links obrigatórios
REQUIRED_LINKS = [
    'https://descomplicar.pt/marcar-reuniao/',
    'https://descomplicar.pt/pedido-de-orcamento/',
    'https://descomplicar.pt/contacto/'
]

# Configurações de CTA
CTA_CONFIG = {
    'initial': {
        'background_color': '#f2d9a2',
        'template': 'Se procura uma solução para {tema}, a Descomplicar pode ajudar com:',
        'links': REQUIRED_LINKS
    },
    'final': {
        'template': 'Para começar a sua jornada de {tema} hoje mesmo:',
        'links': REQUIRED_LINKS
    }
}

# Métricas e KPIs comuns
METRICS = {
    'produtividade': [
        'aumento de eficiência',
        'redução de custos',
        'otimização de processos',
        'economia de tempo'
    ],
    'vendas': [
        'aumento de receita',
        'taxa de conversão',
        'valor médio de venda',
        'retenção de clientes'
    ],
    'digital': [
        'tráfego web',
        'engagement',
        'leads gerados',
        'ROI digital'
    ]
}

# Fontes de dados confiáveis
TRUSTED_SOURCES = [
    'INE - Instituto Nacional de Estatística',
    'ACEPI - Associação da Economia Digital',
    'IDC Portugal',
    'Comissão Europeia',
    'Instituto Superior Técnico',
    'Universidade do Porto',
    'APDC - Associação Portuguesa para o Desenvolvimento das Comunicações'
]

# Templates HTML
HTML_TEMPLATES = {
    'pre_cta': """
        <div class="cta-box-initial" style="background-color: {background_color};">
            <h3>{title}</h3>
            <ul>
                {services}
            </ul>
            <p>
                <a href="{link_reuniao}">Marcar Reunião</a> |
                <a href="{link_orcamento}">Pedir Orçamento</a> |
                <a href="{link_contacto}">Contactar</a>
            </p>
        </div>
    """,
    'section': """
        <section class="{section_class}">
            {content}
        </section>
    """
}

# Categorias do WordPress e seus serviços associados
WP_CATEGORIES = {
    'blog-e-commerce': {
        'name': 'E-commerce',
        'services': [
            'Desenvolvimento de E-commerce',
            'Marketing Digital para E-commerce',
            'Otimização de Conversão'
        ]
    },
    'blog-empreendedorismo': {
        'name': 'Empreendedorismo',
        'services': [
            'Consultoria para Empreendedores',
            'Estratégia de Negócios',
            'Marketing Digital'
        ]
    },
    'blog-gestao-pmes': {
        'name': 'Gestão de PMEs',
        'services': [
            'Consultoria para PMEs',
            'Transformação Digital',
            'Marketing Digital'
        ]
    },
    'blog-inteligencia-artificial': {
        'name': 'Inteligência Artificial',
        'services': [
            'Soluções de IA para Empresas',
            'Automação Inteligente',
            'Consultoria em IA'
        ]
    },
    'blog-marketing-digital': {
        'name': 'Marketing Digital',
        'services': [
            'SEO e Content Marketing',
            'Gestão de Redes Sociais',
            'Marketing de Performance'
        ]
    },
    'blog-tecnologia': {
        'name': 'Tecnologia',
        'services': [
            'Desenvolvimento Web',
            'Transformação Digital',
            'Consultoria Tecnológica'
        ]
    },
    'blog-transformacao-digital': {
        'name': 'Transformação Digital',
        'services': [
            'Consultoria em Transformação Digital',
            'Automação de Processos',
            'Digitalização de Negócios'
        ]
    },
    'blog-vendas': {
        'name': 'Vendas',
        'services': [
            'Estratégia de Vendas',
            'Marketing Digital',
            'Automação de Vendas'
        ]
    }
}

# Métricas para usar em diferentes categorias
METRICS = {
    'produtividade': [
        'aumento de eficiência',
        'redução de custos',
        'otimização de processos',
        'economia de tempo'
    ],
    'digital': [
        'tráfego web',
        'engagement',
        'leads gerados',
        'ROI digital'
    ]
}

# Métricas de qualidade de conteúdo
QUALITY_METRICS = {
    'readability': {
        'target': 60,  # Índice Flesch-Kincaid (mais alto = mais legível)
        'min': 50,
        'max': 70
    },
    'keywords_density': {
        'target': 2.0,  # Percentagem
        'min': 1.0,
        'max': 3.0
    }
}

# Requisitos para cada seção do modelo ACIDA
SECTION_REQUIREMENTS = {
    'ATTENTION': {
        'min_words': 200,
        'max_words': 300,
        'elements': [
            'estatísticas_impactantes',
            'contexto_português',
            'perguntas_retóricas',
            'problema_central'
        ]
    },
    'CONFIDENCE': {
        'min_words': 400,
        'max_words': 500,
        'elements': [
            'dados_mercado',
            'casos_sucesso',
            'citações_especialistas',
            'estudos_pesquisas'
        ]
    },
    'INTEREST': {
        'min_words': 500,
        'max_words': 600,
        'elements': [
            'benefícios_tangíveis',
            'exemplos_práticos',
            'casos_estudo',
            'resultados_mensuráveis'
        ]
    },
    'DECISION': {
        'min_words': 400,
        'max_words': 500,
        'elements': [
            'passos_implementação',
            'recursos_necessários',
            'considerações_importantes',
            'soluções_descomplicar'
        ]
    },
    'ACTION': {
        'min_words': 150,
        'max_words': 200,
        'elements': [
            'conclusão_persuasiva',
            'chamada_ação',
            'próximos_passos',
            'links_contato'
        ]
    }
} 