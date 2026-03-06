"""Modulo para processamento e calculo de metricas de repositorios do GitHub.

Este modulo fornece funcoes para normalizar dados de repositorios,
calcular metricas estatisticas e formatar a saida de resultados.
"""

import csv
from datetime import datetime

def normalize_repository(repo, now_utc):
    """Normaliza os dados brutos de um repositorio para um formato padronizado.
    
    Converte os dados da API do GitHub em um dicionario com campos calculados
    e formatados para analise, incluindo idade do repositorio e metricas de issues.
    
    Args:
        repo: Dicionario com dados brutos do repositorio da API GraphQL do GitHub
        now_utc: Datetime atual em UTC para calculos de idade e atualizacao
        
    Returns:
        dict: Dicionario normalizado contendo metricas do repositorio
    """
    # Converter timestamps ISO para datetime
    created_at = datetime.fromisoformat(repo["createdAt"].replace("Z", "+00:00"))
    pushed_at = datetime.fromisoformat(repo["pushedAt"].replace("Z", "+00:00"))
    
    # Calcular metricas de issues
    total_issues = repo["totalIssues"]["totalCount"]
    closed_issues = repo["closedIssues"]["totalCount"]
    ratio = closed_issues / total_issues if total_issues > 0 else 0
    
    # Retornar dados normalizados
    return {
        "name": repo["nameWithOwner"],
        "stars": repo["stargazerCount"],
        "age_days": (now_utc - created_at).days,
        "prs": repo["pullRequests"]["totalCount"],
        "releases": repo["releases"]["totalCount"],
        "update_days": (now_utc - pushed_at).days,
        "language": repo["primaryLanguage"]["name"] if repo["primaryLanguage"] else "Unknown",
        "issues_ratio": ratio
    }

def save_to_csv(repositories, filename="repos.csv"):
    """Salva a lista de repositorios em um arquivo CSV.
    
    Exporta os dados dos repositorios normalizados para um arquivo CSV
    com todos os campos relevantes para analise.
    
    Args:
        repositories: Lista de repositorios normalizados
        filename: Nome do arquivo CSV a ser criado (padrao: repos.csv)
    """
    # Preparar e formatar dados antes de escrever no CSV
    rows = []
    for repo in repositories:
        row = repo.copy()
        # Formatar issues_ratio como porcentagem com 2 casas decimais
        try:
            ratio = float(row.get("issues_ratio", 0))
        except (TypeError, ValueError):
            ratio = 0.0
        row["issues_ratio"] = f"{ratio * 100:.2f}%"
        rows.append(row)

    # Criar caminho para salvar na pasta resultados
    import os
    output_dir = "resultados"
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    # Escrever dados no arquivo CSV
    with open(filepath, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["name", "stars", "age_days", "prs", "releases", "update_days", "language", "issues_ratio"],
            delimiter=';'
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"CSV salvo: {filepath}")

def summarize_metrics(repositories):
    """Calcula metricas estatisticas agregadas dos repositorios coletados.
    
    Args:
        repositories: Lista de repositorios normalizados
        
    Returns:
        dict: Dicionario com total de repositorios analisados
    """
    return {"total_repositories": len(repositories)}

def print_results(summary, repositories):
    """Imprime um resumo dos repositorios processados.
    
    Args:
        summary: Dicionario com metricas agregadas dos repositorios
        repositories: Lista de repositorios normalizados para exibicao
    """
    # Exibir total de repositorios
    print(f"\nTotal: {summary['total_repositories']} repositorios")
