"""
Script para criar o arquivo .env com as configurações corretas.
"""

env_content = """# Configurações da API Dify - NÃO ALTERAR
DIFY_API_KEY=app-XLvZjzjRWd43aBugtr5s2yFI
DIFY_API_URL=https://didi.descomplicar.pt/v1

# Configurações do WordPress
WP_URL=https://descomplicar.pt
WP_USERNAME=it@descomplicar.pt
WP_PASSWORD=2025+CriarResultados!
WP_APP_PASSWORD=YqcZ 6tiy gqDD Tuqv OEHV zARs

# Configurações de Cache
CACHE_TTL=3600
CACHE_DIR=.cache

# Configurações de Logging
LOG_LEVEL=INFO
LOG_FILE=gerador-wp.log

# Configurações de Conteúdo
MIN_CONTENT_LENGTH=1000
MAX_CONTENT_LENGTH=5000
DEFAULT_CATEGORY=Marketing Digital
DEFAULT_TAGS=marketing digital,psicologia,saúde mental,clínica

# Configurações de SEO
DEFAULT_META_DESCRIPTION_LENGTH=160
DEFAULT_TITLE_LENGTH=60

# Configurações de Imagens
IMAGE_WIDTH=1920
IMAGE_HEIGHT=1080
IMAGE_QUALITY=90

# Configurações de Tempo
REQUEST_TIMEOUT=30
MAX_RETRIES=3
RETRY_DELAY=5"""

with open(".env", "w", encoding="utf-8") as f:
    f.write(env_content)

print("Arquivo .env criado com sucesso!") 