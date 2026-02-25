"""
Módulo de configuração do sistema.
Gerencia variáveis de ambiente e constantes da API do GitHub.
"""

import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# URL base da API GraphQL do GitHub
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"

# Query de busca: repositórios públicos ordenados por estrelas (descendente)
REPOSITORY_SEARCH_QUERY = "stars:>1 sort:stars-desc is:public"

# Número de repositórios a buscar por requisição (para evitar erros 502)
PAGE_SIZE = int(os.getenv("PAGE_SIZE", "10"))

class Config:
    """
    Classe de configuração que carrega parâmetros do arquivo .env.
    
    Atributos:
        limit: Número máximo de repositórios a coletar (padrão: 100, máximo: 100)
        tokens: Lista de tokens do GitHub (um ou vários separados por vírgula)
    """
    
    def __init__(self):
        # Limite de repositórios a serem coletados (máximo 100 em uma requisição)
        self.limit = int(os.getenv("LIMIT", "100"))
        
        # Carrega os tokens do GitHub (GITHUB_TOKENS pode ter 1 ou vários tokens)
        self.tokens = self._load_tokens()
    
    def _load_tokens(self):
        """
        Carrega tokens do GitHub a partir da variável GITHUB_TOKENS.
        Aceita um único token ou múltiplos separados por vírgula.
        
        Returns:
            list: Lista de tokens válidos (strings não vazias)
        """
        tokens_str = os.getenv("GITHUB_TOKENS", "")
        if not tokens_str.strip():
            return []
        
        return [t.strip() for t in tokens_str.split(",") if t.strip()]
