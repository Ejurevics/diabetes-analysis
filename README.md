# 🩺 Análise de Indicadores de Diabetes — CDC USA

> Pipeline completo de dados: coleta, limpeza, modelagem em PostgreSQL e visualização no Power BI.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Python](https://img.shields.io/badge/Python-3.12-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-18-336791)
![Power BI](https://img.shields.io/badge/Power%20BI-dashboard-F2C811)

---

## 📌 Contexto

O diabetes afeta mais de 37 milhões de americanos e é uma das principais causas de mortalidade evitável nos EUA. Este projeto analisa dados reais do **CDC (Centers for Disease Control and Prevention)** para identificar quais perfis demográficos e socioeconômicos estão mais associados ao diagnóstico da doença.

**Perguntas que este projeto responde:**
- Quais faixas etárias têm maior prevalência de diabetes?
- A prática de atividade física reduz o risco de diagnóstico?
- Existe correlação entre nível de renda e acesso a cuidados preventivos?
- Quais combinações de fatores de risco são mais críticas?

---

## 🗂️ Estrutura do Projeto

```
diabetes-analysis/
│
├── .env.example                      # variáveis de ambiente necessárias (sem valores)
├── .gitignore
├── README.md
├── requirements.txt
│
├── data/
│   ├── raw/                          # CSV original do Kaggle — nunca editar
│   └── processed/                    # arquivos intermediários gerados pelo Python
│
├── notebooks/
│   ├── 01_data_profiling.ipynb       # inspeção inicial: shape, dtypes, nulos
│   ├── 02_eda.ipynb                  # análise exploratória e hipóteses
│   └── 03_validacao_staging.ipynb    # conferência dos dados após carga no banco
│
├── scripts/
│   ├── download_data.py              # baixa o dataset via API do Kaggle
│   ├── ingest.py                     # carrega dados limpos no PostgreSQL
│   └── clean.py                      # funções de limpeza reutilizáveis
│
├── sql/
│   ├── 01_schema.sql                 # cria os 3 schemas: raw, staging, analytics
│   ├── 02_staging.sql                # tabela staging com tipos e constraints
│   ├── 03_analytics_views.sql        # views para consumo no Power BI
│   └── queries/
│       ├── prevalencia_idade.sql
│       ├── fatores_risco_ranking.sql
│       └── perfil_socioeconomico.sql
│
├── reports/
│   ├── insights_diabetes.pdf         # relatório de storytelling final
│   └── images/                       # prints do dashboard
│
└── powerbi/
    └── dashboard.pbix
```

---

## 🔄 Pipeline de Dados

```
Kaggle API  →  data/raw/  →  Python (limpeza)  →  PostgreSQL  →  Power BI
               CSV bruto      pandas / EDA         3 camadas      dashboard
```

| Etapa | Ferramenta | Descrição |
|-------|-----------|-----------|
| Coleta | Kaggle API + uv | Download do dataset via terminal |
| Limpeza | pandas | Tratamento de nulos, tipos e outliers |
| Ingestão | SQLAlchemy | Carga do DataFrame no schema `raw` |
| Modelagem | PostgreSQL | Schemas raw → staging → analytics |
| Análise | SQL (CTEs, Window Functions) | Queries respondendo perguntas de negócio |
| Visualização | Power BI (ODBC) | Dashboard conectado direto nas views |

---

## 🗄️ Arquitetura do Banco

O banco é organizado em **3 camadas**, padrão utilizado em times de dados:

```
raw         → dados brutos carregados diretamente do CSV
staging     → dados limpos, tipados e com constraints de integridade
analytics   → views agregadas expostas para consumo no Power BI
```

**Views criadas no schema `analytics`:**
- `vw_prevalencia_por_idade` — taxa de diabetes por faixa etária
- `vw_fatores_de_risco_ranqueados` — ranking dos fatores mais prevalentes
- `vw_perfil_socioeconomico` — cruzamento de renda × atividade física × diagnóstico

---

## 📊 Dashboard

> 🔧 *Em desenvolvimento — prints serão adicionados ao concluir o Power BI.*

O dashboard é composto por 3 páginas, cada uma respondendo uma pergunta de negócio:

- **Página 1 — Panorama Geral:** KPIs principais e prevalência por faixa etária
- **Página 2 — Fatores de Risco:** ranking dos fatores mais associados ao diagnóstico
- **Página 3 — Perfil Socioeconômico:** cruzamento de renda, atividade física e diagnóstico

---

## ⚙️ Como Reproduzir

### Pré-requisitos
- Python 3.11+
- [uv](https://docs.astral.sh/uv/) instalado
- PostgreSQL 15+ rodando localmente
- Conta no Kaggle com API token configurado

### 1. Clonar o repositório
```bash
git clone https://github.com/seu-usuario/diabetes-analysis.git
cd diabetes-analysis
```

### 2. Instalar dependências
```bash
uv sync
```

### 3. Configurar variáveis de ambiente
```bash
cp .env.example .env
# edite o .env com suas credenciais do PostgreSQL
```

### 4. Baixar o dataset
```bash
uv run python scripts/download_data.py
```

### 5. Executar o pipeline
```bash
uv run python scripts/clean.py       # limpeza
uv run python scripts/ingest.py      # ingestão no PostgreSQL
```

### 6. Criar estrutura no banco
```bash
psql -U seu_usuario -d diabetes_project -f sql/01_schema.sql
psql -U seu_usuario -d diabetes_project -f sql/02_staging.sql
psql -U seu_usuario -d diabetes_project -f sql/03_analytics_views.sql
```

---

## 📦 Dataset

| Campo | Detalhe |
|-------|---------|
| Fonte | [Kaggle — Diabetes Health Indicators](https://www.kaggle.com/datasets/alexteboul/diabetes-health-indicators-dataset) |
| Origem | CDC — Behavioral Risk Factor Surveillance System (BRFSS) |
| Volume | ~250.000 registros |
| Variáveis | 22 colunas (demográficas, clínicas e socioeconômicas) |
| Licença | Public Domain |

---

## 🧰 Tecnologias

| Ferramenta | Uso |
|-----------|-----|
| Python 3.12 + uv | Gerenciamento de ambiente e execução |
| pandas | Limpeza e transformação dos dados |
| SQLAlchemy | Conexão Python ↔ PostgreSQL |
| PostgreSQL 18 | Modelagem, análise e armazenamento |
| Power BI | Dashboard e visualização final |
| Jupyter Notebook | EDA documentada |
| Git + GitHub | Versionamento |

---

## 📁 Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto com base no `.env.example`:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=diabetes_project
DB_USER=seu_usuario
DB_PASSWORD=sua_senha
KAGGLE_USERNAME=seu_usuario_kaggle
KAGGLE_KEY=sua_chave_kaggle
```

---

## 👤 Autor

**Seu Nome**
[LinkedIn](https://www.linkedin.com/in/enzojurevics/) · [GitHub](https://github.com/Ejurevics)

---

*Projeto desenvolvido como portfólio pessoal para demonstrar habilidades em análise de dados com Python, PostgreSQL e Power BI.*
