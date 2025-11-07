import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
import streamlit as st

st.set_page_config(page_title="Superstore", layout="wide")
st.title("Superstore Dashboard")

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DB_PATH = PROJECT_ROOT / "data" / "db.sqlite"
SQL_PATH = PROJECT_ROOT / "sql" / "03_KPI.sql"
engine = create_engine(f"sqlite:///{DB_PATH}")
min_date = pd.read_sql('SELECT MIN("Order Date") as min_date FROM orders', engine)
max_date = pd.read_sql('SELECT MAX("Order Date") as max_date FROM orders', engine)
cat = pd.read_sql('SELECT DISTINCT "Category" as Categories FROM orders', engine)
categories = cat["Categories"].tolist()

min_dt = pd.to_datetime(min_date.iloc[0, 0]).date()
max_dt = pd.to_datetime(max_date.iloc[0, 0]).date()
date_range = st.sidebar.date_input("Диапазон дат", (min_dt, max_dt))
start_dt, end_dt = date_range
date_from = pd.to_datetime(start_dt).strftime("%Y-%m-%d")
date_to = pd.to_datetime(end_dt).strftime("%Y-%m-%d")

selected_categories = st.multiselect("Категории", categories, default=[])
placeholders = ",".join([f":cat{i}" for i in range(len(selected_categories))])
params_cat = {f"cat{i}": v for i, v in enumerate(selected_categories)}
params = {"date_from": date_from, "date_to": date_to}

query = SQL_PATH.read_text(encoding="utf-8")

where_cat = ""
if len(selected_categories) == 0:
    where_cat = ""
else:
    where_cat = f' AND "Category" IN ({placeholders})'
    params.update(params_cat)

query = query.replace("-- CAT_FILTER", where_cat)

df_sql = pd.read_sql(query, engine, params=params)

tot = int(df_sql["tot"].iat[0])
tot_los = int(df_sql["tot_los"].iat[0])
loss = float(df_sql["loss_rate_pct"].iat[0])

if df_sql.empty or df_sql["tot"].iat[0] == 0:
    st.warning("Нет данных для выбранных фильтров")
else:
    c1, c2 = st.columns([1, 2])
    c1.metric("Убыточные", f"{loss:.2f}%")
    c2.write(f"из {tot:,} заказов, {tot_los:,} убыточных")

tot_dis = int(df_sql["dis"].iat[0])
tot_los_dis = int(df_sql["dis_los"].iat[0])
loss_dis = float(df_sql["dis_loss_rate_pct"].iat[0])
if df_sql.empty or df_sql["dis"].iat[0] == 0:
    st.warning("Нет данных для выбранных фильтров")
else:
    c1, c2 = st.columns([1, 2])
    c1.metric("Убыточные среди заказов со скидкой", f"{loss_dis:.2f}%")
    c2.write(f"из {tot_dis:,} заказов, {tot_los_dis:,} убыточных")
