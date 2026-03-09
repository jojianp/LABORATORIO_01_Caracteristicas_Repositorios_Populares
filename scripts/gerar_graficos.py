import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Configuração de estilo
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Carregar dados
csv_path = Path(__file__).parent.parent / 'resultados' / 'repos.csv'
df = pd.read_csv(csv_path, delimiter=';')

# Converter issues_ratio de string para float
df['issues_ratio'] = df['issues_ratio'].str.rstrip('%').astype('float') / 100

# Criar diretório para salvar gráficos
output_dir = Path(__file__).parent.parent / 'resultados' / 'graficos'
output_dir.mkdir(exist_ok=True)


# ============================================================================
# RQ 01: Sistemas populares são maduros/antigos?
# ============================================================================
def rq01_idade_repositorios():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma de idade
    axes[0].hist(df['age_days'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Idade (dias)')
    axes[0].set_ylabel('Frequência')
    axes[0].set_title('Distribuição da Idade dos Repositórios')
    axes[0].axvline(df['age_days'].median(), color='red', linestyle='--', 
                    label=f'Mediana: {df["age_days"].median():.0f} dias')
    axes[0].axvline(df['age_days'].mean(), color='orange', linestyle='--', 
                    label=f'Média: {df["age_days"].mean():.0f} dias')
    axes[0].legend()
    
    # Box plot
    axes[1].boxplot(df['age_days'], vert=True)
    axes[1].set_ylabel('Idade (dias)')
    axes[1].set_title('Box Plot da Idade dos Repositórios')
    axes[1].set_xticklabels(['Repositórios'])
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq01_idade_repositorios.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# RQ 02: Sistemas populares recebem muita contribuição externa?
# ============================================================================
def rq02_pull_requests():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma (escala log devido à variação)
    axes[0].hist(df['prs'], bins=50, color='seagreen', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Total de Pull Requests Aceitas')
    axes[0].set_ylabel('Frequência')
    axes[0].set_title('Distribuição de Pull Requests Aceitas')
    axes[0].axvline(df['prs'].median(), color='red', linestyle='--', 
                    label=f'Mediana: {df["prs"].median():.0f}')
    axes[0].axvline(df['prs'].mean(), color='orange', linestyle='--', 
                    label=f'Média: {df["prs"].mean():.0f}')
    axes[0].legend()
    
    # Top 15 repositórios com mais PRs
    top_prs = df.nlargest(15, 'prs')[['name', 'prs']].copy()
    top_prs['name'] = top_prs['name'].str.split('/').str[-1]
    axes[1].barh(range(len(top_prs)), top_prs['prs'], color='seagreen', alpha=0.7)
    axes[1].set_yticks(range(len(top_prs)))
    axes[1].set_yticklabels(top_prs['name'], fontsize=9)
    axes[1].set_xlabel('Total de Pull Requests')
    axes[1].set_title('Top 15 Repositórios com Mais Pull Requests')
    axes[1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq02_pull_requests.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Gerar todos os gráficos
    rq01_idade_repositorios()
    rq02_pull_requests()


if __name__ == '__main__':
    main()
