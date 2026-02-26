"""Script principal para coleta e analise dos repositorios populares do GitHub.

Este script coordena o processo completo das outras classes e módulos
"""

from datetime import datetime, timezone
from cliente_github import TokenManager, fetch_top_repositories
from configuracao import Config
from metricas_rqs import normalize_repository, summarize_metrics, print_results

def main():
    """Funcao principal que executa o fluxo de coleta e analise de dados.
    
    Processo:
    1. Carrega configuracoes (tokens e limite de repositorios)
    2. Inicializa gerenciador de tokens para rotacao automatica
    3. Busca repositorios populares do GitHub via API GraphQL
    4. Normaliza dados e calcula metricas
    5. Exibe resultados já formatados no terminal
	PS.: importante aumentar as linhas do terminal para visualizar os 100 repos (File > Preferences > Settings > Terminal > Integrated: Scrollback)
    """
    # Carregar configuracoes (tokens e limite de repositorios)
    config = Config()
    
    # Inicializar gerenciador de tokens com rotacao automatica
    token_manager = TokenManager(config.tokens)
    
    # Buscar repositorios mais populares do GitHub
    raw_repositories = fetch_top_repositories(
        token_manager=token_manager,
        limit=config.limit,
    )
    
    # Obter timestamp atual para calculos de idade e atualizacao
    now_utc = datetime.now(timezone.utc)
    
    # Normalizar dados brutos em formato padronizado
    repositories = [normalize_repository(repo, now_utc) for repo in raw_repositories]
    
    # Calcular metricas agregadas e estatisticas
    summary = summarize_metrics(repositories)
    
    # Exibir resultados formatados
    print_results(summary, repositories)
    
    print("\nColeta finalizada. \nTotal de repositórios coletados:", len(repositories), "\n")


if __name__ == "__main__":
    main()