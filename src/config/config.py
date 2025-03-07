"""
Configuração do projeto GeradorWP
"""
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Configurações da API OpenAI
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Configurações do WordPress
WP_URL = os.getenv("WP_URL")
WP_USERNAME = os.getenv("WP_USERNAME")
WP_PASSWORD = os.getenv("WP_PASSWORD")

# Configurações gerais
MAX_TOKENS = 2000
TEMPERATURE = 0.7
MODEL_NAME = "gpt-4-turbo-preview"

# Verifica se as variáveis de ambiente necessárias estão definidas
def validate_config():
    required_vars = [
        "OPENAI_API_KEY",
        "WP_URL",
        "WP_USERNAME",
        "WP_PASSWORD"
    ]
    
    missing_vars = [var for var in required_vars if not globals()[var]]
    
    if missing_vars:
        raise ValueError(f"Variáveis de ambiente em falta: {', '.join(missing_vars)}") 