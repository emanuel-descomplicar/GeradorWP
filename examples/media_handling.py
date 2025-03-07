"""
Exemplo de gerenciamento de mídia do GeradorWP.
"""

import os
from dotenv import load_dotenv
from gerador_wp.utils.image import ImageManager
from gerador_wp.utils.wordpress import WordPressClient
from gerador_wp.utils.logger import Logger
from gerador_wp.utils.exceptions import ImageError, WordPressError

def save_image(image_bytes: bytes, filename: str) -> str:
    """
    Salva uma imagem em disco.
    
    Args:
        image_bytes: Bytes da imagem
        filename: Nome do arquivo
        
    Returns:
        Caminho do arquivo salvo
    """
    # Cria diretório de mídia se não existir
    os.makedirs("media", exist_ok=True)
    
    # Salva a imagem
    filepath = os.path.join("media", filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes)
    
    return filepath

def main():
    """Função principal do exemplo."""
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Inicializa utilitários
    image = ImageManager()
    wp = WordPressClient()
    logger = Logger(__name__)
    
    try:
        print("Iniciando gerenciamento de mídia...")
        
        # 1. Geração de Imagem
        print("\n1. Gerando imagem com IA...")
        prompt = "Uma imagem moderna e minimalista sobre tecnologia e inovação"
        image_bytes = image.generate_image(prompt)
        
        if image_bytes:
            # Salva imagem original
            original_path = save_image(image_bytes, "original.jpg")
            print(f"✓ Imagem original salva: {original_path}")
            print(f"- Tamanho: {len(image_bytes) / 1024:.1f}KB")
            
            # 2. Otimização
            print("\n2. Otimizando imagem...")
            optimized_bytes = image.optimize_image(
                image_bytes,
                max_size=500 * 1024  # 500KB
            )
            
            # Salva imagem otimizada
            optimized_path = save_image(optimized_bytes, "optimized.jpg")
            print(f"✓ Imagem otimizada salva: {optimized_path}")
            print(f"- Tamanho: {len(optimized_bytes) / 1024:.1f}KB")
            
            # 3. Criação de Miniaturas
            print("\n3. Gerando miniaturas...")
            sizes = [(150, 150), (300, 300), (600, 600)]
            
            for width, height in sizes:
                # Gera miniatura
                thumbnail_bytes = image.create_thumbnail(
                    optimized_bytes,
                    width=width,
                    height=height
                )
                
                # Salva miniatura
                thumbnail_path = save_image(
                    thumbnail_bytes,
                    f"thumbnail_{width}x{height}.jpg"
                )
                print(f"✓ Miniatura salva: {thumbnail_path}")
                print(f"- Tamanho: {len(thumbnail_bytes) / 1024:.1f}KB")
            
            # 4. Upload para WordPress
            print("\n4. Fazendo upload para WordPress...")
            
            # Upload da imagem original
            original_id = wp._upload_image(original_path)
            print(f"✓ Imagem original enviada: ID {original_id}")
            
            # Upload da imagem otimizada
            optimized_id = wp._upload_image(optimized_path)
            print(f"✓ Imagem otimizada enviada: ID {optimized_id}")
            
            # Upload das miniaturas
            for width, height in sizes:
                thumbnail_path = f"media/thumbnail_{width}x{height}.jpg"
                thumbnail_id = wp._upload_image(thumbnail_path)
                print(f"✓ Miniatura {width}x{height} enviada: ID {thumbnail_id}")
            
            print("\nProcesso concluído com sucesso!")
            print(f"Total de arquivos processados: {2 + len(sizes)}")
            
        else:
            print("⚠ Não foi possível gerar a imagem")
        
    except ImageError as e:
        print(f"\nErro ao processar imagem: {e}")
        logger.error(f"Erro de imagem: {str(e)}")
    except WordPressError as e:
        print(f"\nErro ao fazer upload: {e}")
        logger.error(f"Erro do WordPress: {str(e)}")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        logger.error(f"Erro inesperado: {str(e)}")
    finally:
        # Limpa arquivos temporários
        if os.path.exists("media"):
            for file in os.listdir("media"):
                os.remove(os.path.join("media", file))
            os.rmdir("media")

if __name__ == "__main__":
    main() 