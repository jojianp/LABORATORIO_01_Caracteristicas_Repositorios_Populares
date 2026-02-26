"""Modulo para processamento e calculo de metricas de repositorios do GitHub.

Este modulo fornece funcoes para normalizar dados de repositorios,
calcular metricas estatisticas e formatar a saida de resultados.
"""

import statistics
from collections import Counter, defaultdict
from datetime import datetime

def iso_to_datetime(iso_value):
    """Converte uma string ISO 8601 em datetime.
    
    Args:
        iso_value: String no formato ISO 8601 (ex: '2025-04-17T17:04:31Z')
        
    Returns:
        datetime: Objeto datetime com timezone UTC
    """
    return datetime.fromisoformat(iso_value.replace("Z", "+00:00"))

def normalize_repository(repo, now_utc):
    """Normaliza os dados brutos de um repositorio para um formato padronizado.
    
    Converte os dados da API do GitHub em um dicionario com campos calculados
    e formatados para analise, incluindo idade do repositorio e metricas de issues.
    
    Args:
        repo: Dicionario com dados brutos do repositorio da API GraphQL do GitHub
        now_utc: Datetime atual em UTC para calculos de idade e atualizacao
        
    Returns:
        dict: Dicionario normalizado contendo:
            - name_with_owner: Nome completo do repositorio (owner/repo)
            - url: URL do repositorio
            - stars: Numero de estrelas
            - created_at: Data de criacao (ISO 8601)
            - pushed_at: Data do ultimo push (ISO 8601)
            - age_days: Idade do repositorio em dias
            - merged_pull_requests: Total de PRs aceitos
            - releases: Total de releases
            - days_since_last_update: Dias desde o ultimo push
            - primary_language: Linguagem principal do repositorio
            - closed_issues: Total de issues fechados
            - total_issues: Total de issues
            - closed_issues_ratio: Razao de issues fechados (None se sem issues)
    """
    # Converter timestamps ISO para datetime
    created_at = iso_to_datetime(repo["createdAt"])
    pushed_at = iso_to_datetime(repo["pushedAt"])

    # Calcular idade do repositorio e tempo desde ultima atualizacao
    age_days = (now_utc - created_at).days
    days_since_last_update = (now_utc - pushed_at).days

    # Extrair contadores de metricas
    merged_prs = repo["pullRequests"]["totalCount"]
    releases = repo["releases"]["totalCount"]
    total_issues = repo["totalIssues"]["totalCount"]
    closed_issues = repo["closedIssues"]["totalCount"]

    # Calcular razao de issues fechados (evitar divisao por zero)
    closed_issues_ratio = None
    if total_issues > 0:
        closed_issues_ratio = closed_issues / total_issues

    # Determinar linguagem principal (ou "Unknown" se nao houver)
    primary_language = "Unknown"
    if repo["primaryLanguage"] and repo["primaryLanguage"].get("name"):
        primary_language = repo["primaryLanguage"]["name"]

    return {
        "name_with_owner": repo["nameWithOwner"],
        "url": repo["url"],
        "stars": repo["stargazerCount"],
        "created_at": repo["createdAt"],
        "pushed_at": repo["pushedAt"],
        "age_days": age_days,
        "merged_pull_requests": merged_prs,
        "releases": releases,
        "days_since_last_update": days_since_last_update,
        "primary_language": primary_language,
        "closed_issues": closed_issues,
        "total_issues": total_issues,
        "closed_issues_ratio": closed_issues_ratio,
    }


def summarize_metrics(repositories):
    """Calcula metricas estatisticas agregadas dos repositorios coletados.
    
    Gera medianas para diversas metricas e analises por linguagem de programacao,
    respondendo as questoes de pesquisa (RQs) definidas no relatorio que deve ser
	 entregue ao final do lab.
    
    Args:
        repositories: Lista de repositorios normalizados
        
    Returns:
        dict: Dicionario contendo:
            - total_repositories: Total de repositorios analisados
            - rq01_median_age_days: Mediana da idade em dias
            - rq02_median_accepted_prs: Mediana de PRs aceitos
            - rq03_median_releases: Mediana de releases
            - rq04_median_days_since_last_update: Mediana de dias desde atualizacao
            - rq05_language_count: Counter com frequencia de linguagens
            - rq06_median_closed_issues_ratio: Mediana da razao de issues fechados
            - rq07_by_language: Lista de metricas agregadas por linguagem
    """
    # Extrair valores de metricas para calculo de medianas
    age_days_values = [repo["age_days"] for repo in repositories]
    merged_pr_values = [repo["merged_pull_requests"] for repo in repositories]
    releases_values = [repo["releases"] for repo in repositories]
    days_since_update_values = [repo["days_since_last_update"] for repo in repositories]
    issues_ratio_values = [repo["closed_issues_ratio"] for repo in repositories if repo["closed_issues_ratio"] is not None]

    # Contar frequencia de linguagens primarias
    language_counter = Counter(repo["primary_language"] for repo in repositories)

    # Agrupar repositorios por linguagem
    by_language = defaultdict(list)
    for repo in repositories:
        by_language[repo["primary_language"]].append(repo)

    # Calcular metricas por linguagem (RQ07)
    language_rq07 = []
    for language, repos in by_language.items():
        language_rq07.append(
            {
                "language": language,
                "repositories": len(repos),
                "median_merged_pull_requests": statistics.median(r["merged_pull_requests"] for r in repos),
                "median_releases": statistics.median(r["releases"] for r in repos),
                "median_days_since_last_update": statistics.median(r["days_since_last_update"] for r in repos),
            }
        )

    # Ordenar por quantidade de repositorios (decrescente)
    language_rq07.sort(key=lambda item: item["repositories"], reverse=True)

    summary = {
        "total_repositories": len(repositories),
        "rq01_median_age_days": statistics.median(age_days_values) if age_days_values else None,
        "rq02_median_accepted_prs": statistics.median(merged_pr_values) if merged_pr_values else None,
        "rq03_median_releases": statistics.median(releases_values) if releases_values else None,
        "rq04_median_days_since_last_update": (
            statistics.median(days_since_update_values) if days_since_update_values else None
        ),
        "rq05_language_count": language_counter,
        "rq06_median_closed_issues_ratio": statistics.median(issues_ratio_values) if issues_ratio_values else None,
        "rq07_by_language": language_rq07,
    }
    return summary


def print_results(summary, repositories):
    """Imprime os dados dos repositorios de forma mais organizada.
    
    Exibe informacoes detalhadas de cada repositorio em formato textual,
    com numeracao sequencial e campos bem legiveis.
    
    Args:
        summary: Dicionario com metricas agregadas dos repositorios
        repositories: Lista de repositorios normalizados para exibicao
    """
    print(f"\nTotal de repositorios: {summary['total_repositories']}")
    
    # Iterar sobre repositorios exibindo informacoes detalhadas
    for i, repo in enumerate(repositories, 1):
        print(f"\n[{i}] Repositorio: {repo['name_with_owner']}")
        print(f"URL: {repo['url']}")
        print(f"Estrelas: {repo['stars']}")
        print(f"Criado em: {repo['created_at']}")
        print(f"Ultimo push: {repo['pushed_at']}")
        print(f"Idade: {repo['age_days']} dias")
        print(f"Pull requests aceitos: {repo['merged_pull_requests']}")
        print(f"Releases: {repo['releases']}")
        print(f"Dias desde ultima atualizacao: {repo['days_since_last_update']}")
        print(f"Linguagem principal: {repo['primary_language']}")
        print(f"Issues fechados: {repo['closed_issues']}")
        print(f"Issues totais: {repo['total_issues']}")
        if repo['closed_issues_ratio'] is not None:
            print(f"Razao de issues fechados: {repo['closed_issues_ratio']:.4f}")
        else:
            print(f"Razao de issues fechados: N/A")
