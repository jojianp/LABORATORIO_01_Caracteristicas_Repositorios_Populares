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
    
    
# ============================================================================
# RQ 06: Sistemas populares possuem alto percentual de issues fechadas?
# ============================================================================
def rq06_issues_fechadas():
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Histograma
    axes[0].hist(df['issues_ratio'] * 100, bins=30, color='indianred', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Percentual de Issues Fechadas (%)')
    axes[0].set_ylabel('Frequência')
    axes[0].set_title('Distribuição do Percentual de Issues Fechadas')
    axes[0].axvline(df['issues_ratio'].median() * 100, color='red', linestyle='--', 
                    label=f'Mediana: {df["issues_ratio"].median()*100:.1f}%')
    axes[0].axvline(df['issues_ratio'].mean() * 100, color='orange', linestyle='--', 
                    label=f'Média: {df["issues_ratio"].mean()*100:.1f}%')
    axes[0].legend()
    
    # Box plot
    axes[1].boxplot(df['issues_ratio'] * 100, vert=True)
    axes[1].set_ylabel('Percentual de Issues Fechadas (%)')
    axes[1].set_title('Box Plot do Percentual de Issues Fechadas')
    axes[1].set_xticklabels(['Repositórios'])
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq06_issues_fechadas.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# RQ 07: Linguagens populares vs contribuição, releases e atualizações
# ============================================================================
def rq07_linguagens_vs_metricas():
    # Selecionar top 10 linguagens por quantidade
    top_languages = df['language'].value_counts().head(10).index
    df_top_lang = df[df['language'].isin(top_languages)].copy()
    
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. PRs por linguagem
    prs_by_lang = df_top_lang.groupby('language')['prs'].agg(['mean', 'median', 'sum'])
    prs_by_lang = prs_by_lang.sort_values('mean', ascending=False)
    
    axes[0, 0].barh(range(len(prs_by_lang)), prs_by_lang['mean'], color='steelblue', alpha=0.7)
    axes[0, 0].set_yticks(range(len(prs_by_lang)))
    axes[0, 0].set_yticklabels(prs_by_lang.index)
    axes[0, 0].set_xlabel('Média de Pull Requests')
    axes[0, 0].set_title('Média de Pull Requests por Linguagem (Top 10)')
    axes[0, 0].invert_yaxis()
    
    # 2. Releases por linguagem
    releases_by_lang = df_top_lang.groupby('language')['releases'].agg(['mean', 'median', 'sum'])
    releases_by_lang = releases_by_lang.sort_values('mean', ascending=False)
    
    axes[0, 1].barh(range(len(releases_by_lang)), releases_by_lang['mean'], color='coral', alpha=0.7)
    axes[0, 1].set_yticks(range(len(releases_by_lang)))
    axes[0, 1].set_yticklabels(releases_by_lang.index)
    axes[0, 1].set_xlabel('Média de Releases')
    axes[0, 1].set_title('Média de Releases por Linguagem (Top 10)')
    axes[0, 1].invert_yaxis()
    
    # 3. Dias desde última atualização por linguagem (menor = mais frequente)
    update_by_lang = df_top_lang.groupby('language')['update_days'].agg(['mean', 'median'])
    update_by_lang = update_by_lang.sort_values('mean', ascending=True)
    
    axes[1, 0].barh(range(len(update_by_lang)), update_by_lang['mean'], color='mediumpurple', alpha=0.7)
    axes[1, 0].set_yticks(range(len(update_by_lang)))
    axes[1, 0].set_yticklabels(update_by_lang.index)
    axes[1, 0].set_xlabel('Média de Dias desde Última Atualização')
    axes[1, 0].set_title('Frequência de Atualização por Linguagem (Top 10)')
    axes[1, 0].invert_yaxis()
    
    # 4. Contagem de repos por linguagem (popularidade)
    lang_counts = df['language'].value_counts().head(10)
    axes[1, 1].barh(range(len(lang_counts)), lang_counts.values, color='teal', alpha=0.7)
    axes[1, 1].set_yticks(range(len(lang_counts)))
    axes[1, 1].set_yticklabels(lang_counts.index)
    axes[1, 1].set_xlabel('Quantidade de Repositórios')
    axes[1, 1].set_title('Popularidade das Linguagens (Top 10)')
    axes[1, 1].invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq07_linguagens_vs_metricas.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Criar gráfico adicional: correlação entre quantidade de repos e métricas
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    
    # Preparar dados agregados por linguagem
    lang_stats = df_top_lang.groupby('language').agg({
        'prs': 'mean',
        'releases': 'mean',
        'update_days': 'mean',
        'name': 'count'
    }).rename(columns={'name': 'count'})
    
    # Criar scatter plot
    scatter = ax.scatter(lang_stats['count'], lang_stats['prs'], 
                        s=lang_stats['releases']*10, alpha=0.6, c=lang_stats['update_days'],
                        cmap='viridis', edgecolors='black', linewidth=1)
    
    # Adicionar labels para cada linguagem
    for idx, row in lang_stats.iterrows():
        ax.annotate(idx, (row['count'], row['prs']), fontsize=9, 
                   ha='center', va='bottom')
    
    ax.set_xlabel('Quantidade de Repositórios (Popularidade)')
    ax.set_ylabel('Média de Pull Requests')
    ax.set_title('Relação entre Popularidade da Linguagem e Contribuições\n' +
                 '(tamanho = releases, cor = dias desde atualização)')
    
    # Colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Dias desde última atualização')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'rq07_correlacao_linguagens.png', dpi=300, bbox_inches='tight')
    plt.close()


# ============================================================================
# DASHBOARD GERAL: Combinação de todas as análises para visão geral 
# ============================================================================
def gerar_dashboard_geral():
    fig = plt.figure(figsize=(18, 12))
    gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.5)
    
    # 1. Idade
    ax1 = fig.add_subplot(gs[0, 0])
    ax1.hist(df['age_days']/365, bins=30, color='steelblue', alpha=0.7, edgecolor='black')
    ax1.set_xlabel('Idade (anos)')
    ax1.set_ylabel('Frequência')
    ax1.set_title('RQ01: Idade dos Repositórios')
    ax1.axvline(df['age_days'].median()/365, color='red', linestyle='--', linewidth=2)
    
    # 2. PRs
    ax2 = fig.add_subplot(gs[0, 1])
    ax2.hist(np.log10(df['prs'] + 1), bins=30, color='seagreen', alpha=0.7, edgecolor='black')
    ax2.set_xlabel('Log10(PRs + 1)')
    ax2.set_ylabel('Frequência')
    ax2.set_title('RQ02: Pull Requests')
    
    # 3. Releases
    ax3 = fig.add_subplot(gs[0, 2])
    ax3.hist(np.log10(df['releases'] + 1), bins=30, color='coral', alpha=0.7, edgecolor='black')
    ax3.set_xlabel('Log10(Releases + 1)')
    ax3.set_ylabel('Frequência')
    ax3.set_title('RQ03: Releases')
    
    # 4. Atualização
    ax4 = fig.add_subplot(gs[1, 0])
    ax4.hist(df['update_days'], bins=30, color='mediumpurple', alpha=0.7, edgecolor='black')
    ax4.set_xlabel('Dias desde atualização')
    ax4.set_ylabel('Frequência')
    ax4.set_title('RQ04: Última Atualização')
    
    # 5. Linguagens (top 10)
    ax5 = fig.add_subplot(gs[1, 1])
    lang_counts = df['language'].value_counts().head(10)
    ax5.barh(range(len(lang_counts)), lang_counts.values, color='teal', alpha=0.7)
    ax5.set_yticks(range(len(lang_counts)))
    ax5.set_yticklabels(lang_counts.index, fontsize=8)
    ax5.set_xlabel('Repositórios')
    ax5.set_title('RQ05: Top 10 Linguagens')
    ax5.invert_yaxis()
    
    # 6. Issues fechadas
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.hist(df['issues_ratio'] * 100, bins=30, color='indianred', alpha=0.7, edgecolor='black')
    ax6.set_xlabel('% Issues Fechadas')
    ax6.set_ylabel('Frequência')
    ax6.set_title('RQ06: Issues Fechadas')
    
    # 7. Estatísticas gerais (texto)
    ax7 = fig.add_subplot(gs[2, :])
    ax7.axis('off')
    
    stats_text = f"""
    ESTATÍSTICAS GERAIS DOS REPOSITÓRIOS POPULARES
    
    Total de repositórios analisados: {len(df)}
    
    Idade média: {df['age_days'].mean()/365:.1f} anos  |  Mediana: {df['age_days'].median()/365:.1f} anos
    
    PRs média: {df['prs'].mean():.1f}  |  Mediana: {df['prs'].median():.1f}  |  Total: {df['prs'].sum()}
    
    Releases média: {df['releases'].mean():.1f}  |  Mediana: {df['releases'].median():.1f}  |  Sem releases: {(df['releases']==0).sum()} ({(df['releases']==0).sum()/len(df)*100:.1f}%)
    
    Atualização média: {df['update_days'].mean():.1f} dias  |  Última semana: {(df['update_days']<=7).sum()} ({(df['update_days']<=7).sum()/len(df)*100:.1f}%)
    
    Linguagens: {len(df['language'].unique())} diferentes  |  Top 3: {', '.join([f"{lang} ({count})" for lang, count in df['language'].value_counts().head(3).items()])}
    
    Issues fechadas média: {df['issues_ratio'].mean()*100:.1f}%  |  ≥80% fechadas: {(df['issues_ratio']>=0.8).sum()} ({(df['issues_ratio']>=0.8).sum()/len(df)*100:.1f}%)
    """
    
    ax7.text(0.1, 0.5, stats_text, fontsize=11, verticalalignment='center',
             fontfamily='monospace', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.suptitle('Dashboard: Análise de Repositórios Populares do GitHub', 
                 fontsize=16, fontweight='bold', y=0.98)
    
    plt.savefig(output_dir / 'dashboard_geral.png', dpi=300, bbox_inches='tight')
    plt.close()


def main():
    # Gerar todos os gráficos
    rq01_idade_repositorios()
    rq02_pull_requests()
    rq03_releases()
    rq04_ultima_atualizacao()
    rq05_linguagens()
    rq06_issues_fechadas()
    rq07_linguagens_vs_metricas()
    gerar_dashboard_geral()

if __name__ == '__main__':
    main()
