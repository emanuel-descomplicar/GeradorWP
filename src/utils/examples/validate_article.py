"""
Exemplo de uso do validador ACIDA.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

from ..validators import ACIDAValidator, validate_html_structure

def main():
    # Exemplo de conteúdo de artigo
    article_content = {
        'pre_cta': """
        <div class="cta-box-initial" style="background-color: #f2d9a2;">
            <h3>Se procura uma solução para Marketing Digital, a Descomplicar pode ajudar com:</h3>
            <ul>
                <li>Consultoria Estratégica Digital</li>
                <li>Gestão de Redes Sociais</li>
                <li>SEO e Marketing de Conteúdo</li>
            </ul>
            <p>
                <a href="https://descomplicar.pt/marcar-reuniao/">Marcar Reunião</a> |
                <a href="https://descomplicar.pt/pedido-de-orcamento/">Pedir Orçamento</a> |
                <a href="https://descomplicar.pt/contacto/">Contactar</a>
            </p>
        </div>
        """,
        'attention': "..." * 250,  # Simulando 250 palavras
        'confidence': "..." * 450,  # Simulando 450 palavras
        'interest': "..." * 550,  # Simulando 550 palavras
        'decision': "..." * 450,  # Simulando 450 palavras
        'action': """
        Para começar a transformar o seu negócio digital hoje mesmo, entre em contacto connosco:
        - Agende uma reunião gratuita em <a href="https://descomplicar.pt/marcar-reuniao/">https://descomplicar.pt/marcar-reuniao/</a>
        - Peça um orçamento em <a href="https://descomplicar.pt/pedido-de-orcamento/">https://descomplicar.pt/pedido-de-orcamento/</a>
        - Ou contacte-nos diretamente em <a href="https://descomplicar.pt/contacto/">https://descomplicar.pt/contacto/</a>
        """ * 10  # Simulando 175 palavras
    }

    # Criar validador
    validator = ACIDAValidator(dify_api_key="your_api_key_here")
    
    # Validar conteúdo
    is_valid, errors = validator.validate_content(article_content)
    
    print("=== Validação de Conteúdo ===")
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

if __name__ == '__main__':
    main() 