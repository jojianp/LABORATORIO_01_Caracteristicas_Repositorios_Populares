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


# ============================================================================
# RQ 03: Sistemas populares lançam releases com frequência?
# ============================================================================
def rq03_releases():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma
    axes[0].hist(df['releases'], bins=50, color='coral', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Total de Releases')
    axes[0].set_ylabel('Frequência')
    axes[0].set_title('Distribuição de Releases')
    axes[0].axvline(df['releases'].median(), color='red', linestyle='--', 
                    label=f'Mediana: {df["releases"].median():.0f}')
    axes[0].axvline(df['releases'].mean(), color='orange', linestyle='--', 
                    label=f'Média: {df["releases"].mean():.0f}')
    axes[0].legend()
    
    # Top 15 repositórios com mais releases
    top_releases = df.nlargest(15, 'releases')[['name', 'releases']].copy()
    top_releases['name'] = top_releases['name'].str.split('/').str[-1]
    axes[1].barh(range(len(top_releases)), top_releases['releases'], color='coral', alpha=0.7)
    axes[1].set_yticks(range(len(top_releases)))
    axes[1].set_yticklabels(top_releases['name'], fontsize=9)
    axes[1].set_xlabel('Total de Releases')
    axes[1].set_title('Top 15 Repositórios com Mais Releases')
    axes[1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq03_releases.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# RQ 04: Sistemas populares são atualizados com frequência?
# ============================================================================
def rq04_ultima_atualizacao():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma
    axes[0].hist(df['update_days'], bins=50, color='mediumpurple', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Dias desde última atualização')
    axes[0].set_ylabel('Frequência')
    axes[0].set_title('Distribuição do Tempo desde Última Atualização')
    axes[0].axvline(df['update_days'].median(), color='red', linestyle='--', 
                    label=f'Mediana: {df["update_days"].median():.0f} dias')
    axes[0].axvline(df['update_days'].mean(), color='orange', linestyle='--', 
                    label=f'Média: {df["update_days"].mean():.0f} dias')
    axes[0].legend()
    
    # Box plot
    axes[1].boxplot(df['update_days'], vert=True)
    axes[1].set_ylabel('Dias desde última atualização')
    axes[1].set_title('Box Plot do Tempo desde Última Atualização')
    axes[1].set_xticklabels(['Repositórios'])
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq04_ultima_atualizacao.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# RQ 05: Sistemas populares são escritos nas linguagens mais populares?
# ============================================================================
def rq05_linguagens():
    # Contar frequência de linguagens
    language_counts = df['language'].value_counts()
    
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Top 15 linguagens
    top_languages = language_counts.head(15)
    axes[0].barh(range(len(top_languages)), top_languages.values, color='teal', alpha=0.7)
    axes[0].set_yticks(range(len(top_languages)))
    axes[0].set_yticklabels(top_languages.index)
    axes[0].set_xlabel('Quantidade de Repositórios')
    axes[0].set_title('Top 15 Linguagens de Programação')
    axes[0].invert_yaxis()
    
    # Gráfico de pizza das top 10
    top10 = language_counts.head(10)
    outros = language_counts[10:].sum()
    
    if outros > 0:
        top10['Outras'] = outros
    
    colors = plt.cm.Set3(range(len(top10)))
    axes[1].pie(top10.values, labels=top10.index, autopct='%1.1f%%', 
                colors=colors, startangle=90)
    axes[1].set_title('Distribuição das Linguagens (Top 10 + Outras)')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq05_linguagens.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Gerar todos os gráficos
    rq01_idade_repositorios()
    rq02_pull_requests()


if __name__ == '__main__':
    main()
