import pandas as pd
import psycopg2
from psycopg2 import sql

# PostgreSQL connection details
PG_HOST = "host.containers.internal"  # Container name when running with docker-compose
PG_PORT = "5432"
PG_USER = "postgres"        # <-- PostgreSQL username
PG_PASSWORD = "1234"     # <-- PostgreSQL password
PG_DB = "coingecko"      # <-- Database name
TABLE_NAME = "coingecko_top100"

def store_to_pg():
    # Read CSV
    try:
        df = pd.read_csv("/opt/airflow/dags/coingecko_top100.csv")
        print(f"CSV loaded successfully: {len(df)} rows")
    except Exception as e:
        print("Failed to read CSV:", e)
        return

    # Connect to PostgreSQL
    try:
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            user=PG_USER,
            password=PG_PASSWORD,
            database=PG_DB
        )
        conn.autocommit = True
        cursor = conn.cursor()
        print("Connected to PostgreSQL successfully")
    except Exception as e:
        print("Connection failed:", e)
        return

    # Create table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        rank INT,
        symbol VARCHAR(10),
        name VARCHAR(100),
        price_usd NUMERIC,
        change_1h_percent NUMERIC,
        change_24h_percent NUMERIC,
        change_7d_percent NUMERIC,
        volume_24h BIGINT,
        market_cap BIGINT,
        last_updated TIMESTAMP,
        fetched_at_utc TIMESTAMP
    )
    """
    cursor.execute(create_table_query)
    print(f"Table `{TABLE_NAME}` is ready")

    # Insert CSV data into PostgreSQL
    inserted_rows = 0
    for _, row in df.iterrows():
        try:
            insert_query = sql.SQL("""
                INSERT INTO {table} (
                    rank, symbol, name, price_usd, change_1h_percent, change_24h_percent,
                    change_7d_percent, volume_24h, market_cap, last_updated, fetched_at_utc
                )
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """).format(table=sql.Identifier(TABLE_NAME))

            cursor.execute(insert_query, (
                int(row['rank']),
                row['symbol'],
                row['name'],
                float(row['price_usd']),
                float(row['change_1h_percent']) if not pd.isna(row['change_1h_percent']) else None,
                float(row['change_24h_percent']) if not pd.isna(row['change_24h_percent']) else None,
                float(row['change_7d_percent']) if not pd.isna(row['change_7d_percent']) else None,
                int(float(row['volume_24h'])),
                int(float(row['market_cap'])),
                pd.to_datetime(row['last_updated']),
                pd.to_datetime(row['fetched_at_utc'])
            ))
            inserted_rows += 1
        except Exception as e:
            print(f"Failed to insert row {row['rank']} ({row['symbol']}):", e)

    cursor.close()
    conn.close()
    print(f"Data inserted successfully: {inserted_rows} rows")

if __name__ == "__main__":
    store_to_pg()