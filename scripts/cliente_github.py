"""Cliente para a API GraphQL do GitHub.

Este módulo gerencia a comunicação com a API do GitHub, incluindo:
- Rotação automática de múltiplos tokens para evitar rate limiting
- Tratamento de erros e rate limiting da API
- Busca de repositórios populares usando GraphQL
"""

import time

import requests

from configuracao import GITHUB_GRAPHQL_URL, PAGE_SIZE, REPOSITORY_SEARCH_QUERY

GRAPHQL_QUERY = """
query ($searchQuery: String!, $first: Int!, $after: String) {
  search(query: $searchQuery, type: REPOSITORY, first: $first, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on Repository {
        nameWithOwner
        url
        stargazerCount
        createdAt
        pushedAt
        primaryLanguage {
          name
        }
        pullRequests(states: MERGED, first: 1) {
          totalCount
        }
        releases(first: 1) {
          totalCount
        }
        totalIssues: issues(first: 1) {
          totalCount
        }
        closedIssues: issues(states: CLOSED, first: 1) {
          totalCount
        }
      }
    }
  }
}
"""

class TokenManager:
    """Gerenciador de tokens do GitHub com rotação automática.
    
    Gerencia múltiplos tokens da API do GitHub, fazendo rotação automática
    quando um token atinge o limite de requisições (rate limit).
    
    Atributos:
        tokens (list): Lista de tokens válidos do GitHub.
        index (int): Índice do token atualmente em uso.
    """
    
    def __init__(self, tokens):
        """Inicializa o gerenciador com uma lista de tokens.
        
        Args:
            tokens (list): Lista de tokens do GitHub (strings).
            
        Raises:
            RuntimeError: Se nenhum token válido for fornecido.
        """
        cleaned_tokens = [token.strip() for token in tokens if token and token.strip()]
        if not cleaned_tokens:
            raise RuntimeError("Nenhum token informado. Defina GITHUB_TOKEN ou GITHUB_TOKENS.")
        self.tokens = cleaned_tokens
        self.index = 0

    @property
    def current_token(self):
        """Retorna o token atualmente em uso.
        
        Returns:
            str: Token do GitHub sendo usado no momento.
        """
        return self.tokens[self.index]

    def next_token(self):
        """Avança para o próximo token na rotação circular.
        
        Incrementa o índice e volta ao início quando chega ao fim da lista.
        """
        self.index = (self.index + 1) % len(self.tokens)

    def auth_headers(self):
        """Gera os headers de autenticação para requisições HTTP.
        
        Returns:
            dict: Dicionário com headers Authorization e Content-Type.
        """
        return {
            "Authorization": f"Bearer {self.current_token}",
            "Content-Type": "application/json",
        }

    def sleep_until_reset(self, reset_timestamp):
        """Aguarda até o reset do rate limit da API.
        
        Args:
            reset_timestamp (int): Timestamp Unix de quando o rate limit será resetado.
        """
        wait_seconds = max(1, int(reset_timestamp) - int(time.time()) + 2)
        wait_minutes = round(wait_seconds / 60, 2)
        print(f"Todos os tokens no limite. Aguardando {wait_minutes} min para reset...")
        time.sleep(wait_seconds)


def graphql_request(token_manager, query, variables):
    """Executa uma requisição GraphQL para a API do GitHub com retry automático.
    
    Faz requisições à API GraphQL do GitHub com tratamento robusto de erros,
    incluindo rotação automática de tokens e retry em caso de rate limiting.
    
    Args:
        token_manager (TokenManager): Gerenciador de tokens para autenticação.
        query (str): Query GraphQL a ser executada.
        variables (dict): Variáveis da query GraphQL.
        
    Returns:
        dict: Dados retornados pela API no campo 'data'.
        
    Raises:
        RuntimeError: Se a requisição falhar após todas as tentativas ou
                     se ocorrer um erro GraphQL não relacionado a rate limit.
    """
    attempts = 0
    max_attempts = max(5, len(token_manager.tokens) * 3)

    while attempts < max_attempts:
        attempts += 1
        response = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers=token_manager.auth_headers(),
            timeout=120,
        )

        remaining = int(response.headers.get("X-RateLimit-Remaining", "1"))
        reset_at = int(response.headers.get("X-RateLimit-Reset", "0"))

        if response.status_code == 200:
            payload = response.json()
            if "errors" in payload:
                errors_text = str(payload["errors"]).lower()
                if "rate limit" in errors_text:
                    token_manager.next_token()
                    if token_manager.index == 0 and reset_at > 0:
                        token_manager.sleep_until_reset(reset_at)
                    continue
                raise RuntimeError(f"Erro GraphQL: {payload['errors']}")

            if remaining <= 1:
                token_manager.next_token()
            return payload["data"]

        response_text = response.text.lower()
        if response.status_code in (403, 429) or "rate limit" in response_text:
            token_manager.next_token()
            if token_manager.index == 0 and reset_at > 0:
                token_manager.sleep_until_reset(reset_at)
            continue
        
        # Retry em erros temporários do servidor (502, 503, 504, 500)
        if response.status_code in (500, 502, 503, 504):
            wait_time = 5 + (attempts * 2)
            print(f"Erro temporário {response.status_code}. Tentativa {attempts}/{max_attempts}. Aguardando {wait_time}s...")
            time.sleep(wait_time)
            continue

        raise RuntimeError(f"Falha na chamada GraphQL: HTTP {response.status_code} - {response.text}")

    raise RuntimeError("Não foi possível concluir a chamada GraphQL após múltiplas tentativas.")


def fetch_top_repositories(token_manager, limit=100):
    """Busca os top repositórios do GitHub ordenados por estrelas.
    
    Executa uma busca GraphQL para obter repositórios públicos mais populares,
    ordenados decrescentemente por número de estrelas.
    
    Args:
        token_manager (TokenManager): Gerenciador de tokens para autenticação.
        limit (int, optional): Número máximo de repositórios a buscar.
                              Padrão é 100 (máximo permitido pela API).
    
    Returns:
        list: Lista de dicionários com informações dos repositórios, incluindo:
              - nameWithOwner: Nome completo (owner/repo)
              - url: URL do repositório
              - stargazerCount: Número de estrelas
              - createdAt: Data de criação
              - pushedAt: Data do último push
              - primaryLanguage: Linguagem principal
              - pullRequests: Contagem de PRs merged
              - releases: Contagem de releases
              - totalIssues: Total de issues
              - closedIssues: Issues fechadas
    """
    if limit <= 0:
        return []

    all_repos = []
    cursor = None
    remaining = limit

    print(f"Buscando {limit} repositórios...")
    
    while remaining > 0:
        batch_size = min(PAGE_SIZE, remaining)
        variables = {
            "searchQuery": REPOSITORY_SEARCH_QUERY,
            "first": batch_size,
            "after": cursor
        }

        data = graphql_request(token_manager, GRAPHQL_QUERY, variables)
        search_result = data["search"]
        repos = [node for node in search_result["nodes"] if node is not None]
        
        all_repos.extend(repos)
        remaining -= len(repos)
        
        print(f"Coletados {len(all_repos)}/{limit} repositórios")
        
        # Verifica se tem mais páginas
        page_info = search_result.get("pageInfo", {})
        if not page_info.get("hasNextPage") or remaining <= 0:
            break
            
        cursor = page_info.get("endCursor")
        time.sleep(1)
    
    return all_repos
