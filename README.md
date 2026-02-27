# LABORATORIO_01_Caracteristicas_Repositorios_Populares

Neste laboratório estudamos características de repositórios populares open-source no GitHub. O projeto coleta metadados (estrelas, issues, pull requests, releases, linguagem, datas) dos repositórios mais estrelados e gera métricas agregadas para análise.

**Como usar**

1) Crie um ambiente Python e ative-o:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2) Instale dependências:

```powershell
pip install -r scripts\requirements.txt
```

3) Crie um arquivo `.env` na raiz do repositório com suas variáveis.

Exemplo de `.env` em `.env.example`.


- `GITHUB_TOKENS`: um ou mais tokens separados por vírgula. A aplicação faz rotação entre tokens para mitigar rate limits.
- `LIMIT`: máximo de repositórios a coletar (padrão 100).
- `PAGE_SIZE`: quantidade de repositórios por página na query GraphQL (padrão 10).

4) Execute o coletor:

```powershell
cd scripts
python main.py
```

