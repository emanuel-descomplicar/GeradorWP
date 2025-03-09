#!/usr/bin/env python3
"""
GeradorWP - Sistema de Geração e Publicação de Conteúdo para WordPress

Este é o ponto de entrada principal do sistema GeradorWP, que coordena os agentes
para pesquisar, escrever e publicar conteúdo no WordPress.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import sys
import json
import asyncio
import argparse
import logging
from typing import Dict, List, Any, Optional
from pathlib import Path

# Adicionar diretório pai ao sys.path para permitir importações
sys.path.insert(0, str(Path(__file__).parent.parent))

# Importar componentes principais
from src.config import get_settings
from src.utils.logger import configure_global_logging
from src.agents.researcher_agent import ResearcherAgent
from src.agents.writer_agent import WriterAgent
from src.agents.publisher_agent import PublisherAgent
from src.tasks.research_task import ResearchTask
from src.tasks.writing_task import WritingTask
from src.tasks.publishing_task import PublishingTask

# Configurar logging
logger = logging.getLogger(__name__)

async def process_topic(topic: str, keywords: List[str], category: str, status: str = "draft", config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Processa um tópico completo, desde a pesquisa até a publicação.
    
    Args:
        topic: Tópico principal do artigo
        keywords: Lista de palavras-chave relacionadas
        category: Categoria do WordPress
        status: Status de publicação (draft, publish, etc.)
        config: Configurações opcionais
        
    Returns:
        Resultados do processamento
    """
    logger.info(f"Iniciando processamento do tópico: {topic}")
    results = {"topic": topic, "success": False}
    config = config or {}
    
    try:
        # Inicializar agentes
        researcher = ResearcherAgent(config.get("research", {}))
        writer = WriterAgent(config.get("writing", {}))
        publisher = PublisherAgent(config.get("publishing", {}))
        
        # Fase 1: Pesquisa
        logger.info("Fase 1: Pesquisa")
        research_task = ResearchTask(topic, keywords, config.get("research", {}))
        research_data = await researcher.research_topic(topic, keywords)
        validated_research = research_task.validate_results(research_data)
        
        if not validated_research.get("validation", {}).get("meets_criteria", False):
            logger.warning(f"Resultados da pesquisa não atendem aos critérios mínimos: {validated_research['validation'].get('improvement_suggestions', [])}")
        
        # Fase 2: Escrita
        logger.info("Fase 2: Escrita")
        writing_task = WritingTask(topic, keywords, validated_research, config.get("writing", {}))
        content = await writer.create_content(validated_research, topic, keywords)
        optimized_content = await writer.optimize_seo(content, keywords)
        validated_content = writing_task.validate_content(optimized_content)
        
        if not validated_content.get("validation", {}).get("meets_criteria", False):
            logger.warning(f"Conteúdo não atende aos critérios mínimos: {validated_content['validation'].get('improvement_suggestions', [])}")
        
        # Fase 3: Publicação
        logger.info("Fase 3: Publicação")
        publishing_task = PublishingTask(validated_content, category, status, config.get("publishing", {}))
        pre_validation = publishing_task.validate_pre_publish()
        
        if not pre_validation.get("can_proceed", False):
            logger.error(f"Validação pré-publicação falhou: {pre_validation.get('failed_validations', [])}")
            results["error"] = f"Validação pré-publicação falhou: {pre_validation.get('failed_validations', [])}"
            return results
        
        # Publicar
        publish_result = await publisher.publish_content(validated_content, category, status)
        
        # Validar publicação
        if publish_result.get("success", False) and publishing_task.verify_after_publish:
            verification = await publisher.verify_publication(publish_result.get("post_id", 0))
            post_validation = publishing_task.validate_post_publish(publish_result)
            
            if not post_validation.get("all_passed", False):
                logger.warning(f"Validação pós-publicação com alertas: {post_validation.get('failed_validations', [])}")
        
        # Atualizar resultados
        results.update({
            "success": publish_result.get("success", False),
            "post_id": publish_result.get("post_id", None),
            "permalink": publish_result.get("permalink", None),
            "research_quality": validated_research.get("validation", {}).get("quality_score", 0),
            "content_quality": validated_content.get("validation", {}).get("overall_quality", 0),
            "word_count": validated_content.get("word_count", 0),
            "status": status
        })
        
        logger.info(f"Processamento do tópico concluído: {topic}")
        return results
        
    except Exception as e:
        logger.error(f"Erro ao processar tópico {topic}: {str(e)}", exc_info=True)
        results["error"] = str(e)
        return results

async def process_topics_from_file(file_path: str, status: str = "draft", config_file: str = None) -> List[Dict[str, Any]]:
    """
    Processa múltiplos tópicos de um arquivo CSV ou JSON.
    
    Args:
        file_path: Caminho para o arquivo CSV ou JSON
        status: Status de publicação (draft, publish, etc.)
        config_file: Caminho para arquivo de configuração opcional
        
    Returns:
        Lista com os resultados do processamento de cada tópico
    """
    logger.info(f"Processando tópicos do arquivo: {file_path}")
    
    # Carregar configurações
    settings = get_settings(config_file)
    
    # Determinar tipo de arquivo
    file_path = Path(file_path)
    if not file_path.exists():
        logger.error(f"Arquivo não encontrado: {file_path}")
        return []
    
    topics = []
    
    try:
        # Carregar tópicos do arquivo
        if file_path.suffix.lower() == '.json':
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Verificar formato do JSON
                if isinstance(data, list):
                    topics = data
                elif isinstance(data, dict) and "topics" in data:
                    topics = data["topics"]
                else:
                    logger.error(f"Formato JSON inválido em {file_path}")
                    return []
                
        elif file_path.suffix.lower() == '.csv':
            import csv
            
            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    topics.append(row)
        else:
            logger.error(f"Formato de arquivo não suportado: {file_path.suffix}")
            return []
        
        # Validar tópicos
        if not topics:
            logger.error(f"Nenhum tópico encontrado no arquivo: {file_path}")
            return []
        
        # Processar cada tópico
        results = []
        for topic_data in topics:
            if not isinstance(topic_data, dict):
                logger.warning(f"Formato de tópico inválido, ignorando: {topic_data}")
                continue
                
            topic = topic_data.get("topic", "") or topic_data.get("tema", "")
            keywords = topic_data.get("keywords", []) or topic_data.get("palavras_chave", [])
            category = topic_data.get("category", "") or topic_data.get("categoria", "")
            
            # Converter keywords de string para lista se necessário
            if isinstance(keywords, str):
                keywords = [k.strip() for k in keywords.split(",")]
            
            if not topic or not category:
                logger.warning(f"Tópico ou categoria em falta, ignorando: {topic_data}")
                continue
            
            # Processar tópico
            result = await process_topic(topic, keywords, category, status, settings.get_all())
            results.append(result)
        
        logger.info(f"Processamento de tópicos concluído: {len(results)} processados")
        return results
        
    except Exception as e:
        logger.error(f"Erro ao processar tópicos do arquivo {file_path}: {str(e)}", exc_info=True)
        return []

def main():
    """Função principal do programa."""
    # Configurar parser de argumentos
    parser = argparse.ArgumentParser(description="GeradorWP - Gerador de conteúdo para WordPress")
    
    # Argumentos básicos
    parser.add_argument("--config", "-c", help="Caminho para arquivo de configuração")
    parser.add_argument("--log-level", "-l", choices=["DEBUG", "INFO", "WARNING", "ERROR"], default="INFO", help="Nível de logging")
    
    # Subcomandos
    subparsers = parser.add_subparsers(dest="command", help="Comando a executar")
    
    # Comando 'single': Processar um único tópico
    single_parser = subparsers.add_parser("single", help="Processar um único tópico")
    single_parser.add_argument("--topic", "-t", required=True, help="Tópico para o artigo")
    single_parser.add_argument("--keywords", "-k", required=True, help="Palavras-chave separadas por vírgula")
    single_parser.add_argument("--category", "-cat", required=True, help="Categoria do WordPress")
    single_parser.add_argument("--status", "-s", default="draft", choices=["draft", "publish", "pending"], help="Status de publicação")
    
    # Comando 'file': Processar tópicos de um arquivo
    file_parser = subparsers.add_parser("file", help="Processar tópicos de um arquivo CSV ou JSON")
    file_parser.add_argument("--file", "-f", required=True, help="Caminho para o arquivo CSV ou JSON")
    file_parser.add_argument("--status", "-s", default="draft", choices=["draft", "publish", "pending"], help="Status de publicação")
    
    # Processar argumentos
    args = parser.parse_args()
    
    # Configurar logging global
    configure_global_logging({
        "level": args.log_level,
        "file": "geradorwp.log",
        "console": True
    })
    
    # Carregar configurações
    settings = get_settings(args.config)
    
    # Executar comando
    if args.command == "single":
        # Processar tópico único
        keywords = [k.strip() for k in args.keywords.split(",")]
        
        result = asyncio.run(process_topic(
            args.topic,
            keywords,
            args.category,
            args.status,
            settings.get_all()
        ))
        
        if result["success"]:
            print(f"Tópico processado com sucesso: {args.topic}")
            print(f"ID: {result.get('post_id', 'N/A')}")
            print(f"URL: {result.get('permalink', 'N/A')}")
        else:
            print(f"Erro ao processar tópico: {result.get('error', 'Erro desconhecido')}")
        
    elif args.command == "file":
        # Processar tópicos de arquivo
        results = asyncio.run(process_topics_from_file(
            args.file,
            args.status,
            args.config
        ))
        
        # Imprimir resultados
        success_count = sum(1 for r in results if r.get("success", False))
        print(f"Processamento concluído: {success_count}/{len(results)} tópicos processados com sucesso")
        
        # Salvar resultados
        output_file = f"results_{Path(args.file).stem}_{args.status}.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados salvos em: {output_file}")
    else:
        # Sem comando, mostrar ajuda
        parser.print_help()

if __name__ == "__main__":
    main() 