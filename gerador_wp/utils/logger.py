"""
Sistema de logging para o GeradorWP.
"""

import os
import logging
from typing import Optional
from datetime import datetime

from ..config.config import LOG_LEVEL, LOG_FILE

class Logger:
    """Classe para gerenciar o logging do sistema."""
    
    def __init__(self, name: str):
        """
        Inicializa o sistema de logging.
        
        Args:
            name: Nome do logger
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, LOG_LEVEL))
        
        # Cria o diretório de logs se não existir
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # Configura o formato do log
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        
        # Handler para arquivo
        file_handler = logging.FileHandler(LOG_FILE, encoding="utf-8")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Handler para console
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)
    
    def debug(self, message: str) -> None:
        """
        Registra uma mensagem de debug.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.debug(message)
    
    def info(self, message: str) -> None:
        """
        Registra uma mensagem de informação.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.info(message)
    
    def warning(self, message: str) -> None:
        """
        Registra uma mensagem de aviso.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.warning(message)
    
    def error(self, message: str) -> None:
        """
        Registra uma mensagem de erro.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.error(message)
    
    def critical(self, message: str) -> None:
        """
        Registra uma mensagem crítica.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.critical(message)
    
    def exception(self, message: str) -> None:
        """
        Registra uma mensagem de exceção.
        
        Args:
            message: Mensagem a ser registrada
        """
        self.logger.exception(message)
    
    def log_request(
        self,
        method: str,
        url: str,
        status_code: Optional[int] = None,
        response_time: Optional[float] = None
    ) -> None:
        """
        Registra uma requisição HTTP.
        
        Args:
            method: Método HTTP
            url: URL da requisição
            status_code: Código de status da resposta
            response_time: Tempo de resposta em segundos
        """
        message = f"HTTP {method} {url}"
        
        if status_code:
            message += f" - Status: {status_code}"
            
        if response_time is not None:
            message += f" - Tempo: {response_time:.2f}s"
            
        self.info(message)
    
    def log_error(
        self,
        error: Exception,
        context: Optional[str] = None
    ) -> None:
        """
        Registra um erro com contexto.
        
        Args:
            error: Exceção ocorrida
            context: Contexto do erro
        """
        message = f"Erro: {str(error)}"
        
        if context:
            message = f"{context} - {message}"
            
        self.error(message)
        self.exception(message) 