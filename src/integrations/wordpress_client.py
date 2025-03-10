#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Cliente para integração com a API REST do WordPress.

Este módulo fornece funcionalidades para publicar artigos no WordPress
através da API REST.

Autor: Descomplicar - Agência de Aceleração Digital
https://descomplicar.pt
"""

import os
import json
import mimetypes
import requests
from typing import Dict, List, Optional, Any, Tuple, Union
from bs4 import BeautifulSoup, Comment
import logging
import requests.exceptions
import urllib.parse
import random
import time

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WordPressClient:
    """Cliente para interagir com a API REST do WordPress."""

    def __init__(self, base_url: str = None, username: str = None, password: str = None):
        """
        Inicializa o cliente WordPress com as credenciais.
        
        Args:
            base_url: URL base do site WordPress (ex: https://exemplo.com)
            username: Nome de utilizador para autenticação
            password: Senha do utilizador
        """
        self.base_url = base_url or os.getenv('WP_URL')
        self.username = username or os.getenv('WP_USERNAME')
        self.password = password or os.getenv('WP_PASSWORD')
        self.post_status = os.getenv('WP_POST_STATUS', 'draft')
        
        if not self.base_url or not self.username or not self.password:
            raise ValueError("WordPress URL, username e password são necessários. "
                          "Defina as variáveis de ambiente WP_URL, WP_USERNAME e WP_PASSWORD.")
        
        # Remover a barra final se existir
        if self.base_url.endswith('/'):
            self.base_url = self.base_url[:-1]
            
        self.api_url = f"{self.base_url}/wp-json/wp/v2"
        
        # Utilizar autenticação básica para API
        self.auth = (self.username, self.password)
        
        # Alternativamente, obter token JWT para autenticação mais robusta (quando disponível)
        self.token = None
        try:
            self._get_jwt_token()
        except:
            logger.warning("Não foi possível obter token JWT, usando autenticação básica.")
        
        self.default_timeout = 30  # Timeout padrão para requisições
        
        logger.info(f"Cliente WordPress inicializado para {self.base_url}")

    def _get_jwt_token(self):
        """
        Obtém um token JWT para autenticação com a API WordPress.
        Requer o plugin JWT Authentication for WP REST API instalado.
        """
        try:
            token_url = f"{self.base_url}/wp-json/jwt-auth/v1/token"
            response = requests.post(
                token_url,
                data={
                    'username': self.username,
                    'password': self.password
                },
                timeout=self.default_timeout
            )
            
            if response.status_code == 200:
                self.token = response.json().get('token')
                if self.token:
                    logger.info("Token JWT obtido com sucesso.")
                    return True
            
            return False
        except Exception as e:
            logger.warning(f"Erro ao obter token JWT: {str(e)}")
            return False

    def get_categories(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de categorias disponíveis no WordPress.
        
        Returns:
            Lista de categorias com seus IDs e nomes
        """
        try:
            response = requests.get(
                f"{self.api_url}/categories?per_page=100", 
                auth=self.auth,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            categories = response.json()
            logger.info(f"Obtidas {len(categories)} categorias")
            return categories
        except requests.RequestException as e:
            logger.error(f"Erro ao obter categorias: {str(e)}")
            return []

    def get_category_id(self, slug: str) -> Optional[int]:
        """
        Obtém o ID de uma categoria pelo seu slug.
        
        Args:
            slug: Slug da categoria (ex: 'blog-tecnologia')
            
        Returns:
            ID da categoria ou None se não encontrada
        """
        try:
            encoded_slug = urllib.parse.quote(slug)
            response = requests.get(
                f"{self.api_url}/categories?slug={encoded_slug}", 
                auth=self.auth,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            categories = response.json()
            
            if categories:
                category_id = categories[0]['id']
                logger.info(f"Categoria '{slug}' encontrada com ID {category_id}")
                return category_id
            else:
                logger.warning(f"Categoria com slug '{slug}' não encontrada")
                return None
        except requests.RequestException as e:
            logger.error(f"Erro ao obter categoria por slug: {str(e)}")
            return None

    def get_tags(self) -> List[Dict[str, Any]]:
        """
        Obtém a lista de tags disponíveis no WordPress.
        
        Returns:
            Lista de tags com seus IDs e nomes
        """
        try:
            response = requests.get(
                f"{self.api_url}/tags?per_page=100", 
                auth=self.auth,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            tags = response.json()
            logger.info(f"Obtidas {len(tags)} tags")
            return tags
        except requests.RequestException as e:
            logger.error(f"Erro ao obter tags: {str(e)}")
            return []

    def get_or_create_tag(self, name: str) -> Optional[int]:
        """
        Obtém o ID de uma tag pelo nome ou cria uma nova se não existir.
        
        Args:
            name: Nome da tag
            
        Returns:
            ID da tag ou None se falhar
        """
        # Normalizar o nome da tag
        name = name.strip().lower()
        if not name:
            return None
            
        try:
            # Tentar encontrar a tag existente
            encoded_name = urllib.parse.quote(name)
            response = requests.get(
                f"{self.api_url}/tags?search={encoded_name}", 
                auth=self.auth,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            tags = response.json()
            
            # Verificar tags existentes pelo nome exato
            for tag in tags:
                if tag['name'].lower() == name:
                    logger.info(f"Tag '{name}' encontrada com ID {tag['id']}")
                    return tag['id']
            
            # Criar nova tag se não existir
            logger.info(f"Criando nova tag: '{name}'")
            response = requests.post(
                f"{self.api_url}/tags",
                auth=self.auth,
                json={'name': name},
                timeout=self.default_timeout
            )
            response.raise_for_status()
            tag_id = response.json()['id']
            logger.info(f"Tag '{name}' criada com ID {tag_id}")
            return tag_id
        
        except requests.RequestException as e:
            logger.error(f"Erro ao obter/criar tag '{name}': {str(e)}")
            return None

    def process_tags(self, tags: List[str]) -> List[int]:
        """
        Processa uma lista de tags, obtendo ou criando cada uma.
        
        Args:
            tags: Lista de nomes de tags
            
        Returns:
            Lista de IDs de tags
        """
        tag_ids = []
        for tag_name in tags:
            tag_id = self.get_or_create_tag(tag_name)
            if tag_id:
                tag_ids.append(tag_id)
        
        logger.info(f"Processadas {len(tag_ids)} tags")
        return tag_ids

    def download_image(self, url: str, output_dir: str = "temp_images") -> Optional[str]:
        """
        Faz download de uma imagem a partir de uma URL.
        
        Args:
            url: URL da imagem
            output_dir: Diretório para salvar a imagem
            
        Returns:
            Caminho do arquivo local ou None se falhar
        """
        if not url:
            return None
            
        try:
            # Criar diretório se não existir
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
                
            # Gerar nome de arquivo único
            filename = f"image_{int(time.time())}_{random.randint(1000, 9999)}"
            
            # Determinar extensão do arquivo
            content_type = None
            response = requests.head(url, timeout=self.default_timeout)
            if response.status_code == 200:
                content_type = response.headers.get('Content-Type', '')
                
            if 'image/jpeg' in content_type or url.lower().endswith('.jpg') or url.lower().endswith('.jpeg'):
                filename += '.jpg'
            elif 'image/png' in content_type or url.lower().endswith('.png'):
                filename += '.png'
            elif 'image/webp' in content_type or url.lower().endswith('.webp'):
                filename += '.webp'
            else:
                filename += '.jpg'  # Default para jpg
                
            # Caminho completo para o arquivo
            file_path = os.path.join(output_dir, filename)
            
            # Fazer download da imagem
            response = requests.get(url, stream=True, timeout=self.default_timeout)
            response.raise_for_status()
            
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            logger.info(f"Imagem baixada com sucesso: {file_path}")
            return file_path
        
        except Exception as e:
            logger.error(f"Erro ao baixar imagem: {str(e)}")
            return None

    def upload_media(self, file_path: str) -> Optional[int]:
        """
        Faz upload de um arquivo de mídia para o WordPress.
        
        Args:
            file_path: Caminho para o arquivo a ser enviado ou URL para download
            
        Returns:
            ID da mídia ou None se o upload falhar
        """
        # Verificar se é uma URL
        if file_path and (file_path.startswith('http://') or file_path.startswith('https://')):
            local_file = self.download_image(file_path)
            if not local_file:
                logger.error(f"Não foi possível baixar a imagem: {file_path}")
                return None
            file_path = local_file
            
        # Verificar se o arquivo existe
        if not os.path.exists(file_path):
            logger.error(f"Arquivo não encontrado: {file_path}")
            return None
            
        try:
            filename = os.path.basename(file_path)
            mimetype = mimetypes.guess_type(file_path)[0] or 'image/jpeg'
            
            with open(file_path, 'rb') as file:
                media_data = file.read()
                
            headers = {
                'Content-Disposition': f'attachment; filename="{filename}"',
                'Content-Type': mimetype,
            }
            
            # Usar token JWT se disponível, senão usar autenticação básica
            if self.token:
                headers['Authorization'] = f'Bearer {self.token}'
                auth = None
            else:
                auth = self.auth
            
            # Tentar com autenticação básica primeiro
            try:
                response = requests.post(
                    f"{self.api_url}/media",
                    auth=auth,
                    headers=headers,
                    data=media_data,
                    timeout=self.default_timeout
                )
                response.raise_for_status()
            except requests.exceptions.HTTPError as e:
                # Se falhar com 401 e tivermos um token, tentar com o token
                if e.response.status_code == 401 and self.token:
                    logger.info("Tentando upload com token JWT após falha na autenticação básica")
                    headers['Authorization'] = f'Bearer {self.token}'
                    response = requests.post(
                        f"{self.api_url}/media",
                        headers=headers,
                        data=media_data,
                        timeout=self.default_timeout
                    )
                    response.raise_for_status()
                # Se ainda não tivermos token, tentar com app-password
                elif e.response.status_code == 401:
                    logger.info("Tentando upload com app-password")
                    app_pass = os.getenv('WP_APP_PASSWORD')
                    if app_pass:
                        app_auth = (self.username, app_pass)
                        response = requests.post(
                            f"{self.api_url}/media",
                            auth=app_auth,
                            headers={'Content-Disposition': f'attachment; filename="{filename}"',
                                    'Content-Type': mimetype},
                            data=media_data,
                            timeout=self.default_timeout
                        )
                        response.raise_for_status()
                    else:
                        raise
                else:
                    raise
            
            media_id = response.json()['id']
            logger.info(f"Mídia '{filename}' enviada com ID {media_id}")
            
            # Remover arquivo temporário se foi baixado
            if file_path.startswith('temp_images/'):
                try:
                    os.remove(file_path)
                    logger.info(f"Arquivo temporário removido: {file_path}")
                except:
                    pass
                
            return media_id
        except requests.RequestException as e:
            logger.error(f"Erro ao fazer upload da mídia: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao fazer upload da mídia: {str(e)}")
            return None

    def create_post(self, 
                   title: str, 
                   content: str, 
                   category_id: Optional[int] = None,
                   featured_media_id: Optional[int] = None,
                   tags: Optional[List[Union[int, str]]] = None,
                   status: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Cria um novo post no WordPress.
        
        Args:
            title: Título do post
            content: Conteúdo do post (HTML)
            category_id: ID da categoria (opcional)
            featured_media_id: ID da imagem destacada (opcional)
            tags: Lista de IDs ou nomes de tags (opcional)
            status: Status do post ('draft', 'publish', 'pending')
            
        Returns:
            Dados do post criado ou None se falhar
        """
        status = status or self.post_status
        
        post_data = {
            'title': title,
            'content': content,
            'status': status,
        }
        
        if category_id:
            post_data['categories'] = [category_id]
            
        if featured_media_id:
            post_data['featured_media'] = featured_media_id
            
        # Processar tags
        if tags:
            tag_ids = []
            
            # Processar strings de tags
            str_tags = [tag for tag in tags if isinstance(tag, str)]
            if str_tags:
                tag_ids.extend(self.process_tags(str_tags))
                
            # Adicionar IDs de tags já existentes
            tag_ids.extend([tag for tag in tags if isinstance(tag, int)])
            
            if tag_ids:
                post_data['tags'] = tag_ids
        
        try:
            response = requests.post(
                f"{self.api_url}/posts",
                auth=self.auth,
                json=post_data,
                timeout=self.default_timeout
            )
            response.raise_for_status()
            post = response.json()
            logger.info(f"Post criado com ID {post['id']} e status '{status}'")
            return post
        except requests.RequestException as e:
            error_message = f"Erro ao criar post: {str(e)}"
            if hasattr(e, 'response') and e.response is not None:
                error_message += f" - Resposta: {e.response.text}"
            logger.error(error_message)
            return None
        except Exception as e:
            logger.error(f"Erro inesperado ao criar post: {str(e)}")
            return None

    def html_to_wordpress(self, html_content: str, title: Optional[str] = None) -> Tuple[str, str]:
        """
        Processa o conteúdo HTML para publicação no WordPress.
        
        Args:
            html_content: Conteúdo HTML do artigo
            title: Título do artigo (se não fornecido, extrai do HTML)
            
        Returns:
            Tupla com (título, conteúdo formatado)
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Remover quaisquer tags style ou comentários de código
        for tag in soup.find_all('style'):
            tag.decompose()
        
        # Remover comentários HTML
        for comment in soup.find_all(text=lambda text: isinstance(text, Comment)):
            comment.extract()
        
        # Remover qualquer bloco de código CSS inline visível
        for text in soup.find_all(text=True):
            if 'body {' in text or 'h1 {' in text or '.section {' in text:
                if text.parent.name not in ['code', 'pre']:
                    text.replace_with('')
                
        # Remover backticks de código markdown
        for text in soup.find_all(text=lambda t: '```' in t or '`html' in t):
            clean_text = text.replace('```html', '').replace('```', '').replace('`html', '')
            text.replace_with(clean_text)
        
        # Extrair o título se não fornecido
        if not title:
            h1_tag = soup.find('h1')
            if h1_tag:
                title = h1_tag.text.strip()
                h1_tag.decompose()  # Remove o h1 do conteúdo para evitar duplicação
        
        # Limpar cabeçalhos vazios ou duplicados
        for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            if not tag.text.strip() or tag.text.strip() in ['Atenção', 'Confiança', 'Interesse', 'Decisão', 'Ação']:
                tag.decompose()
        
        # Formatar parágrafos
        for p in soup.find_all('p'):
            # Remover parágrafos vazios
            if not p.text.strip():
                p.decompose()
            elif not p.get('class'):
                p['class'] = 'wp-block-paragraph'
            
        # Formatar cabeçalhos
        for i in range(2, 7):
            for h in soup.find_all(f'h{i}'):
                if not h.get('class'):
                    h['class'] = 'wp-block-heading'
        
        # Formatar listas
        for ul in soup.find_all('ul'):
            if not ul.get('class'):
                ul['class'] = 'wp-block-list'
        
        for ol in soup.find_all('ol'):
            if not ol.get('class'):
                ol['class'] = 'wp-block-list'
        
        # Remover tags script indesejadas
        for script in soup.find_all('script'):
            script.decompose()
        
        # Verificar se há blocos <!-- wp: --> e converter para formato correto se necessário
        content = str(soup)
        
        # Converter blocos HTML simples para blocos Gutenberg
        if '<!-- wp:' not in content:
            # Adicionar blocos Gutenberg conforme necessário
            processed_content = ""
            in_paragraph = False
            
            for line in content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if line.startswith('<h2') and line.endswith('</h2>'):
                    # Extrair o texto do cabeçalho
                    heading_text = BeautifulSoup(line, 'html.parser').text
                    processed_content += f'<!-- wp:heading -->\n{line}\n<!-- /wp:heading -->\n\n'
                elif line.startswith('<p') and line.endswith('</p>'):
                    processed_content += f'<!-- wp:paragraph -->\n{line}\n<!-- /wp:paragraph -->\n\n'
                elif line.startswith('<ul') and line.endswith('</ul>'):
                    processed_content += f'<!-- wp:list -->\n{line}\n<!-- /wp:list -->\n\n'
                elif line.startswith('<ol') and line.endswith('</ol>'):
                    processed_content += f'<!-- wp:list {{"ordered":true}} -->\n{line}\n<!-- /wp:list -->\n\n'
                else:
                    processed_content += line + "\n"
            
            content = processed_content
        
        logger.info(f"HTML processado para WordPress. Título: {title}")
        return title, content

    def extract_tags_from_content(self, content: str, max_tags: int = 5) -> List[str]:
        """
        Extrai possíveis tags do conteúdo do artigo.
        
        Args:
            content: Conteúdo HTML ou texto do artigo
            max_tags: Número máximo de tags a extrair
            
        Returns:
            Lista de tags extraídas
        """
        # Simplificar para texto
        if '<' in content:
            soup = BeautifulSoup(content, 'html.parser')
            text = soup.get_text()
        else:
            text = content
            
        # Lista de palavras-chave comuns a evitar
        stop_words = [
            'a', 'e', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas', 'de', 'para', 'com', 'por',
            'em', 'no', 'na', 'nos', 'nas', 'do', 'da', 'dos', 'das', 'que', 'como', 'mais',
            'também', 'muito', 'muita', 'muitos', 'muitas', 'é', 'são', 'ser', 'estar'
        ]
        
        # Extrair frases potenciais
        words = text.lower().split()
        words = [w for w in words if w not in stop_words and len(w) > 3]
        
        # Contar frequência
        word_counts = {}
        for word in words:
            word_counts[word] = word_counts.get(word, 0) + 1
            
        # Ordenar por frequência
        sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
        
        # Extrair as mais frequentes
        tags = [word for word, count in sorted_words[:max_tags]]
        
        return tags

    def publish_article_from_html(self, 
                                 html_content: str, 
                                 category_slug: str, 
                                 featured_image_path: Optional[str] = None,
                                 title: Optional[str] = None,
                                 tags: Optional[List[str]] = None,
                                 auto_tags: bool = True,
                                 status: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Publica um artigo a partir de conteúdo HTML.
        
        Args:
            html_content: Conteúdo HTML do artigo
            category_slug: Slug da categoria
            featured_image_path: Caminho para a imagem destacada ou URL (opcional)
            title: Título do artigo (se None, será extraído do HTML)
            tags: Lista de tags para o artigo (opcional)
            auto_tags: Se True, gera tags automaticamente a partir do conteúdo
            status: Status do post ('draft', 'publish', 'pending')
            
        Returns:
            Dados do post publicado ou None se falhar
        """
        # Processar HTML para WordPress
        extracted_title, processed_content = self.html_to_wordpress(html_content, title)
        
        # Obter ID da categoria
        category_id = self.get_category_id(category_slug)
        if not category_id:
            logger.warning(f"Categoria '{category_slug}' não encontrada. Post será publicado sem categoria.")
        
        # Upload da imagem destacada
        featured_media_id = None
        if featured_image_path:
            featured_media_id = self.upload_media(featured_image_path)
            if not featured_media_id:
                logger.warning("Não foi possível fazer upload da imagem destacada.")
        
        # Processar tags
        article_tags = []
        if tags:
            article_tags.extend(tags)
            
        # Gerar tags automáticas se solicitado
        if auto_tags:
            auto_generated_tags = self.extract_tags_from_content(html_content)
            # Adicionar apenas tags que ainda não estão na lista
            for tag in auto_generated_tags:
                if tag not in article_tags:
                    article_tags.append(tag)
        
        # Criar o post
        result = self.create_post(
            title=extracted_title,
            content=processed_content,
            category_id=category_id,
            featured_media_id=featured_media_id,
            tags=article_tags,
            status=status
        )
        
        if result:
            logger.info(f"Artigo publicado com sucesso: {result['link']}")
        else:
            logger.error("Falha ao publicar o artigo")
            
        return result 