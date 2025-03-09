"""
Logger - Configuração de logging para o projeto

Este módulo fornece funções para configurar e utilizar o sistema de logging
de forma consistente em todo o projeto.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import logging
import sys
from typing import Dict, Any, Optional
from logging.handlers import RotatingFileHandler

def setup_logger(name: str = None, level: int = logging.INFO, 
                log_file: str = "geradorwp.log", 
                console: bool = True, max_bytes: int = 10485760, 
                backup_count: int = 3) -> logging.Logger:
    """
    Configura e retorna um logger com formatação padrão.
    
    Args:
        name: Nome do logger (None para o logger raiz)
        level: Nível de logging
        log_file: Caminho para o arquivo de log
        console: Se True, também envia logs para o console
        max_bytes: Tamanho máximo do arquivo de log antes de rotacionar
        backup_count: Número de arquivos de backup a manter
        
    Returns:
        O logger configurado
    """
    # Obter ou criar logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Verificar se já está configurado
    if logger.handlers:
        return logger
    
    # Definir formato
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Configurar handler de arquivo
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Adicionar handler de console se solicitado
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger pelo nome. Se não existir, cria um novo.
    
    Args:
        name: Nome do logger
        
    Returns:
        O logger solicitado
    """
    logger = logging.getLogger(name)
    
    # Se o logger não tiver handlers, configurá-lo
    if not logger.handlers:
        return setup_logger(name)
    
    return logger

def configure_global_logging(config: Optional[Dict[str, Any]] = None) -> None:
    """
    Configura o sistema de logging global para o projeto.
    
    Args:
        config: Configurações opcionais de logging
    """
    config = config or {}
    
    # Obter configurações
    level_name = config.get("level", "INFO")
    log_file = config.get("file", "geradorwp.log")
    console = config.get("console", True)
    
    # Mapear nível de logging
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    level = level_map.get(level_name, logging.INFO)
    
    # Configurar logger raiz
    setup_logger(None, level, log_file, console)
    
    # Configurar loggers de terceiros
    third_party_level = config.get("third_party_level", "WARNING")
    third_party_level = level_map.get(third_party_level, logging.WARNING)
    
    # Ajustar nível de alguns loggers de terceiros comuns
    for module in ["urllib3", "chardet", "requests", "wordpress_xmlrpc"]:
        logging.getLogger(module).setLevel(third_party_level)
    
    # Log inicial
    root_logger = logging.getLogger()
    root_logger.info(f"Sistema de logging configurado com nível {level_name}")

class LoggerMixin:
    """
    Mixin que adiciona funcionalidade de logging a uma classe.
    
    Exemplo de uso:
    ```python
    class MinhaClasse(LoggerMixin):
        def __init__(self):
            self.setup_logger()
            self.logger.info("MinhaClasse inicializada")
    ```
    """
    
    def setup_logger(self, name: str = None) -> None:
        """
        Configura o logger para a classe.
        
        Args:
            name: Nome do logger (None para usar o nome da classe)
        """
        if name is None:
            name = self.__class__.__module__ + "." + self.__class__.__name__
        
        self.logger = get_logger(name) 