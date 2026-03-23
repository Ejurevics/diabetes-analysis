import os
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# =============================================================
# CONFIGURAÇÃO DE CONEXÃO
# load_dotenv() lê o arquivo .env e injeta as variáveis
# no ambiente — os.getenv() as recupera pelo nome.
# Isso mantém usuário e senha fora do código.
# =============================================================
load_dotenv()

DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_PORT     = os.getenv("DB_PORT")
DB_NAME     = os.getenv("DB_NAME")

# =============================================================
# ENGINE
# O SQLAlchemy usa uma "engine" como ponto central de conexão.
# Ela não abre conexão ainda — só configura como conectar.
# O formato da string é:
#   dialeto+driver://usuario:senha@host:porta/banco
# =============================================================
engine = create_engine(
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# =============================================================
# TESTE DE CONEXÃO
# Antes de enviar dados, confirmamos que o banco responde.
# O bloco with abre e fecha a conexão automaticamente.
# text() converte a string em um comando SQL executável.
# =============================================================
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("Conexão com o banco estabelecida.")
except Exception as e:
    print(f"Falha na conexão: {e}")
    raise  # interrompe o script se não conectar

# =============================================================
# CARREGAMENTO DO DATAFRAME LIMPO
# Adapte o caminho ou substitua por sua variável em memória.
# Se você já tem o df limpo no notebook, pode chamar
# esta função passando o df direto como argumento.
# =============================================================
df = pd.read_csv(r"C:\Estudos\projetos_pessoais\diabetes-analysis\01_data\processed\diabetes_012_processed.csv")

print(f"Shape do DataFrame: {df.shape}")
print(df.dtypes)

# =============================================================
# INGESTÃO NO POSTGRESQL
# to_sql() envia o DataFrame para o banco.
#
# name        → nome da tabela que será criada
# con         → a engine configurada acima
# schema      → schema de destino (criado no pgAdmin)
# if_exists   → "replace" recria a tabela a cada execução
#               use "append" para adicionar sem apagar
# index       → False para não criar coluna de índice do pandas
# chunksize   → envia em lotes de 1000 linhas (evita timeout)
# =============================================================
from sqlalchemy.types import Boolean, SmallInteger, Integer, Text

dtype_map = {
    "Diabetes_012":          SmallInteger(),  # era category (0, 1, 2)
    "HighBP":                Boolean(),
    "HighChol":              Boolean(),
    "CholCheck":             Boolean(),
    "BMI":                   SmallInteger(),  # era int16
    "Smoker":                Boolean(),
    "Stroke":                Boolean(),
    "HeartDiseaseorAttack":  Boolean(),
    "PhysActivity":          Boolean(),
    "Fruits":                Boolean(),
    "Veggies":               Boolean(),
    "HvyAlcoholConsump":     Boolean(),
    "AnyHealthcare":         Boolean(),
    "NoDocbcCost":           Boolean(),
    "GenHlth":               SmallInteger(),  # era category (1–5)
    "MentHlth":              SmallInteger(),  # era int8
    "PhysHlth":              SmallInteger(),  # era int8
    "DiffWalk":              Boolean(),
    "Sex":                   Boolean(),
    "Age":                   SmallInteger(),  # era category (1–13)
    "Education":             SmallInteger(),  # era category (1–6)
    "Income":                SmallInteger(),  # era category (1–8)
}

df.to_sql(
    name="diabetes_raw",
    con=engine,
    schema="raw",
    if_exists="replace",
    index=False,
    chunksize=1000,
    dtype=dtype_map
)

print("\nDados carregados em raw.diabetes_raw com sucesso!")

# =============================================================
# VALIDAÇÃO PÓS-CARGA
# Lê as primeiras linhas de volta do banco para confirmar
# que os dados chegaram corretamente.
# =============================================================
df_check = pd.read_sql(
    sql=text("SELECT * FROM raw.diabetes_raw LIMIT 5"),
    con=engine
)

print("\n--- Amostra lida do banco ---")
print(df_check)