"""
Exemplo de tratamento de erros do GeradorWP.
"""

import os
import sys
import traceback
from dotenv import load_dotenv
from gerador_wp.agents import ResearcherAgent, WriterAgent, PublisherAgent
from gerador_wp.utils.logger import Logger
from gerador_wp.utils.exceptions import (
    ResearchError,
    WritingError,
    PublishingError,
    ValidationError,
    APIError
)

def handle_research_error(e: ResearchError, logger: Logger) -> None:
    """
    Trata erros de pesquisa.
    
    Args:
        e: Exceção ocorrida
        logger: Logger para registro
    """
    print("\nErro durante a pesquisa:")
    print(f"- Mensagem: {str(e)}")
    print("- Tipo: ResearchError")
    print("- Causa provável: Falha na coleta de dados ou API indisponível")
    print("\nSugestões:")
    print("1. Verifique sua conexão com a internet")
    print("2. Confirme se a API do Dify está disponível")
    print("3. Tente reduzir o escopo da pesquisa")
    print("4. Aguarde alguns minutos e tente novamente")
    
    logger.error(f"Erro de pesquisa: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def handle_writing_error(e: WritingError, logger: Logger) -> None:
    """
    Trata erros de escrita.
    
    Args:
        e: Exceção ocorrida
        logger: Logger para registro
    """
    print("\nErro durante a geração de conteúdo:")
    print(f"- Mensagem: {str(e)}")
    print("- Tipo: WritingError")
    print("- Causa provável: Falha na geração ou formatação do conteúdo")
    print("\nSugestões:")
    print("1. Verifique se os dados da pesquisa estão completos")
    print("2. Tente reduzir o tamanho do conteúdo")
    print("3. Verifique se as palavras-chave são válidas")
    print("4. Tente simplificar a estrutura do conteúdo")
    
    logger.error(f"Erro de escrita: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def handle_publishing_error(e: PublishingError, logger: Logger) -> None:
    """
    Trata erros de publicação.
    
    Args:
        e: Exceção ocorrida
        logger: Logger para registro
    """
    print("\nErro durante a publicação:")
    print(f"- Mensagem: {str(e)}")
    print("- Tipo: PublishingError")
    print("- Causa provável: Falha na comunicação com o WordPress")
    print("\nSugestões:")
    print("1. Verifique suas credenciais do WordPress")
    print("2. Confirme se o site está acessível")
    print("3. Verifique se tem permissão para publicar")
    print("4. Tente publicar como rascunho primeiro")
    
    logger.error(f"Erro de publicação: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def handle_validation_error(e: ValidationError, logger: Logger) -> None:
    """
    Trata erros de validação.
    
    Args:
        e: Exceção ocorrida
        logger: Logger para registro
    """
    print("\nErro de validação:")
    print(f"- Mensagem: {str(e)}")
    print("- Tipo: ValidationError")
    print("- Causa provável: Dados inválidos ou incompletos")
    print("\nSugestões:")
    print("1. Verifique se todos os campos obrigatórios estão preenchidos")
    print("2. Confirme se os formatos dos dados estão corretos")
    print("3. Verifique os limites de tamanho")
    print("4. Valide as URLs e arquivos de mídia")
    
    logger.error(f"Erro de validação: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def handle_api_error(e: APIError, logger: Logger) -> None:
    """
    Trata erros de API.
    
    Args:
        e: Exceção ocorrida
        logger: Logger para registro
    """
    print("\nErro de API:")
    print(f"- Mensagem: {str(e)}")
    print("- Tipo: APIError")
    print("- Causa provável: Falha na comunicação com APIs externas")
    print("\nSugestões:")
    print("1. Verifique suas chaves de API")
    print("2. Confirme se os serviços estão disponíveis")
    print("3. Verifique os limites de requisições")
    print("4. Tente novamente mais tarde")
    
    logger.error(f"Erro de API: {str(e)}")
    logger.error(f"Traceback: {traceback.format_exc()}")

def main():
    """Função principal do exemplo."""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Inicializa o logger
    logger = Logger(__name__)
    
    try:
        # Inicializa os agentes
        researcher = ResearcherAgent()
        writer = WriterAgent()
        publisher = PublisherAgent()
        
        # Testa erro de pesquisa
        print("\nTestando erro de pesquisa...")
        try:
            researcher.research("", [])
        except ResearchError as e:
            handle_research_error(e, logger)
        
        # Testa erro de escrita
        print("\nTestando erro de escrita...")
        try:
            writer.write({}, [])
        except WritingError as e:
            handle_writing_error(e, logger)
        
        # Testa erro de publicação
        print("\nTestando erro de publicação...")
        try:
            publisher.publish({}, [])
        except PublishingError as e:
            handle_publishing_error(e, logger)
        
        # Testa erro de validação
        print("\nTestando erro de validação...")
        try:
            raise ValidationError("Dados inválidos")
        except ValidationError as e:
            handle_validation_error(e, logger)
        
        # Testa erro de API
        print("\nTestando erro de API...")
        try:
            raise APIError("API indisponível")
        except APIError as e:
            handle_api_error(e, logger)
        
        print("\nTestes de erro concluídos!")
        print("Verifique o arquivo de log para mais detalhes.")
        
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        logger.error(f"Erro inesperado: {str(e)}")
        logger.error(f"Traceback: {traceback.format_exc()}")
        sys.exit(1)

if __name__ == "__main__":
    main() 