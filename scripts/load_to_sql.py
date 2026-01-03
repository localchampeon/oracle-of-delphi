#TYPE A
import pandas as pd
import numpy as np
import pyodbc

def to_python_scalar(x):
    """Converts numpy/pandas types to native Python types for pyodbc."""
    if pd.isna(x):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x

def load_to_sql(df, server, driver, database, table_name='sales_hybrid'):
    df_clean = df.copy()

    # 1. Column Rename
    if 'sales_channel' in df_clean.columns:
        df_clean = df_clean.rename(columns={'sales_channel': 'saleschannel'})

    # 2. Numeric Cleaning (NO FILLNA - keeping np.nan)
    # UnitPrice and Revenue as float64 with 2 decimal rounding
    df_clean['unitprice'] = pd.to_numeric(df_clean['unitprice'], errors='coerce').round(2)
    df_clean['revenue'] = pd.to_numeric(df_clean['revenue'], errors='coerce').round(2)
    
    # Quantity as float64 first (because int64 cannot hold np.nan)
    df_clean['quantity'] = pd.to_numeric(df_clean['quantity'], errors='coerce')

    # 3. Date Cleaning
    # Invalid dates become NaT, which to_python_scalar turns into None
    df_clean['invoicedate'] = pd.to_datetime(df_clean['invoicedate'], errors='coerce')

    # 4. String Cleaning
    string_cols = ['invoiceno', 'stockcode', 'description', 'customerid', 'country', 'saleschannel']
    for col in string_cols:
        if col in df_clean.columns:
            # strip() and handle 'nan' strings
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace(['nan', 'None', ''], None)

    # 5. Deduplication
    df_clean = df_clean.drop_duplicates(subset=['invoiceno', 'description'], keep='first')

    # 6. SQL Connection
    '''conn_str = (
        "DRIVER={ODBC Driver 17 for SQL Server};"
        f"SERVER={server};"
        f"DATABASE={database};"
        "Trusted_Connection=yes;"
    )'''
    conn_str =  f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};Trusted_Connection=yes;"        
    
    try:
        conn = pyodbc.connect(conn_str)
        cursor = conn.cursor()
        print(f"Connected to {server}.{database}")
    except Exception as e:
        print(f"Connection failed: {e}")
        return

    # 7. Data Preparation
    # Exclude invoiceid (Identity column)
    available_cols = [col for col in df_clean.columns]
    data_to_insert = df_clean[available_cols]

    # Convert to list of tuples using your working scalar converter
    records = [
        tuple(to_python_scalar(v) for v in row)
        for row in data_to_insert.itertuples(index=False, name=None)
    ]

    # 8. Batch Insert
    placeholders = ', '.join(['?'] * len(available_cols))
    col_names = ', '.join(available_cols)
    insert_sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"

    batch_size = 100000
    for i in range(0, len(records), batch_size):
        batch = records[i:i + batch_size]
        try:
            cursor.fast_executemany = True
            cursor.executemany(insert_sql, batch)
            conn.commit()
            print(f"✓ Batch {i//batch_size + 1} inserted.")
        except Exception as e:
            conn.rollback()
            print(f"✗ Batch failed: {e}")
            raise 

def main():
    path = "C:/Users/Lenovo/hybrid_sales_data_deepseek.csv"
    df = pd.read_csv(path)
    
    # Define required columns for your validation
    required_cols = {'invoiceno', 'invoicedate', 'unitprice', 'quantity'} 
    
    load_to_sql(
        df=df,
        driver = 'ODBC Driver 17 for SQL Server',
        server='DESKTOP-ELTS2E5\\SQLEXPRESS',
        database='OracleOfDelphi'
    )

if __name__ == "__main__":
    main()
