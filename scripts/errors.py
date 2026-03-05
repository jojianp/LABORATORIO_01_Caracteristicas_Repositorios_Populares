"""Módulo de exceções customizadas para o cliente GitHub.

Define exceções específicas para tornar o tratamento de erros
mais claro e testável em todo o projeto.
"""

class GitHubError(Exception):
    """Base para exceções relacionadas ao GitHub."""
    pass


class TokenError(GitHubError):
    """Erro relacionado a tokens de autenticação (ausente/inválido)."""
    pass


class GraphQLError(GitHubError):
    """Erro retornado pela API GraphQL do GitHub."""
    pass


class RateLimitError(GitHubError):
    """Indica que o limite de requisições foi atingido."""
    pass


class RequestError(GitHubError):
    """Erro genérico em requisições HTTP/cliente."""
    pass
