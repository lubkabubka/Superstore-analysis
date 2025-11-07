import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine
from pandas import read_csv

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_PATH = BASE_DIR / "data" / "Sample - Superstore.csv"
BD_PATH = DB_PATH = BASE_DIR / "data" / "db.sqlite"

df = pd.read_csv(RAW_PATH, low_memory=False, encoding="utf-8")
print("Форма до чистки:", df.shape)


def clean_dataset(df):
    col = ["Order Date", "Ship Date"]
    for i in col:
        df[i] = pd.to_datetime(df[i],
                               errors="coerce")  # последнее нужно чтобы если нельзя преобразовать стало пустым а не ошибкой

    nums = ["Sales", "Quantity", "Discount", "Profit", "Postal Code"]
    for i in nums:
        df[i] = pd.to_numeric(df[i], errors="coerce")


clean_dataset(df)


def drop_bad_rows(df):
    # удаляем строки, где все значения являются NaN
    df = df.dropna(how='all')
    required = ["Order ID", "Order Date", "Customer ID", "Product ID", "Sales"]
    for i in required:
        df = df.dropna(subset=[i])
    df = df.drop_duplicates(subset=["Order ID"])
    return df


df = drop_bad_rows(df)


def add_time_cols(df):
    df["Order Year"] = df["Order Date"].dt.year
    df["Order Month"] = df["Order Date"].dt.to_period("M").astype(str)
    df["Order Week"] = df["Order Date"].dt.to_period("W").astype(str)
    return df


df = add_time_cols(df)


def normalize_strings(df):
    str_cols = [
        "Ship Mode", "Customer ID", "Customer Name", "Segment",
        "Country", "City", "State", "Region",
        "Product ID", "Category", "Sub-Category", "Product Name"
    ]
    for i in str_cols:
        df[i] = df[i].astype(str).str.strip()
    return df


df = normalize_strings(df)

print("Форма после чистки:", df.shape)


def save_to_sqlite(df):
    engine = create_engine(f"sqlite:///{DB_PATH}")
    df.to_sql("orders", con=engine, if_exists="replace", index=False)
    print("Записали в базу данных")
    rows_in_db = pd.read_sql("SELECT COUNT(*) AS cnt FROM orders", engine)["cnt"].iloc[0]
    print("Строк в df:", len(df), "| Строк в БД:", rows_in_db)


save_to_sqlite(df)
