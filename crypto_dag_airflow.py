"""
================================================================================
CRYPTO ETL PIPELINE - APACHE AIRFLOW DAG
================================================================================

Description:
    This DAG orchestrates a daily ETL (Extract, Transform, Load) pipeline that:
    1. Extracts top 100 cryptocurrency market data from CoinGecko API
    2. Transforms and cleans the data into a structured format
    3. Loads the processed data into a PostgreSQL database

Data Source:
    - CoinGecko API (https://api.coingecko.com/api/v3/coins/markets)
    - No API key required for basic usage
    - Rate limits: ~10-30 requests/minute (free tier)

Target Database:
    - PostgreSQL database: 'coingecko'
    - Table: 'coingecko_top100'

Schedule:
    - Runs daily at midnight UTC (@daily)
    - No backfill (catchup=False)

Author: Data Engineering Team
Created: January 2025
Last Modified: March 2026
Version: 1.0.0

Dependencies:
    - apache-airflow >= 2.8.0
    - requests >= 2.31.0
    - pandas >= 2.1.0
    - psycopg2-binary >= 2.9.0

================================================================================
"""

# =============================================================================
# IMPORTS
# =============================================================================

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# -----------------------------------------------------------------------------
# Configure Python Path
# -----------------------------------------------------------------------------
# Add the current directory to Python path to enable importing local modules
# This is necessary when running in containerized Airflow environments
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import custom ETL modules
from crypto_etl import get_top_coins_to_csv  # Extract & Transform: Fetch data from CoinGecko
from db import store_to_pg                    # Load: Store data to PostgreSQL

# =============================================================================
# DAG CONFIGURATION
# =============================================================================

# Default arguments applied to all tasks in this DAG
default_args = {
    'owner': 'airflow',              # Owner of the DAG (for filtering in UI)
    'retries': 1,                    # Number of retry attempts on task failure
    'retry_delay': timedelta(minutes=5),  # Wait time between retries
    'depends_on_past': False,        # Task does not depend on previous run
    'email_on_failure': False,       # Disable email notifications (configure SMTP if needed)
    'email_on_retry': False,         # Disable retry email notifications
}

# =============================================================================
# DAG DEFINITION
# =============================================================================

with DAG(
    # Unique identifier for this DAG
    dag_id='crypto_coingecko_pipeline',
    
    # Apply default arguments to all tasks
    default_args=default_args,
    
    # Human-readable description (shown in Airflow UI)
    description='Fetch CoinGecko top 100 coins and store to PostgreSQL',
    
    # Schedule: @daily = runs once a day at midnight
    # Other options: @hourly, @weekly, @monthly, or cron expression
    schedule_interval='@daily',
    
    # Start date for DAG scheduling (historical)
    start_date=datetime(2025, 1, 1),
    
    # Don't run for all past dates since start_date
    catchup=False,
    
    # Tags for filtering and organization in Airflow UI
    tags=['crypto', 'etl', 'coingecko', 'postgresql'],
    
    # Maximum number of active DAG runs
    max_active_runs=1,
    
) as dag:
    
    # -------------------------------------------------------------------------
    # TASK 1: EXTRACT & TRANSFORM
    # -------------------------------------------------------------------------
    # Fetches top 100 cryptocurrencies from CoinGecko API
    # Transforms data into structured format and saves to CSV
    # Output: coingecko_top100.csv
    
    fetch_coins = PythonOperator(
        task_id='fetch_top100_from_coingecko',
        python_callable=get_top_coins_to_csv,
        doc_md="""
        ### Fetch Top 100 Coins
        
        **Purpose:** Extract cryptocurrency market data from CoinGecko API
        
        **Data Points Collected:**
        - Rank, Symbol, Name
        - Current Price (USD)
        - Price Changes (1h, 24h, 7d)
        - 24h Trading Volume
        - Market Capitalization
        - Last Updated Timestamp
        
        **Output:** CSV file saved to working directory
        """,
    )

    # -------------------------------------------------------------------------
    # TASK 2: LOAD
    # -------------------------------------------------------------------------
    # Reads the CSV file and inserts data into PostgreSQL database
    # Creates table if it doesn't exist
    # Handles data type conversions and null values
    
    store_coins = PythonOperator(
        task_id='store_to_postgresql',
        python_callable=store_to_pg,
        doc_md="""
        ### Store to PostgreSQL
        
        **Purpose:** Load processed cryptocurrency data into database
        
        **Database:** coingecko
        **Table:** coingecko_top100
        
        **Operations:**
        1. Read CSV file from previous task
        2. Connect to PostgreSQL
        3. Create table if not exists
        4. Insert all records
        
        **Schema:**
        - rank (INT)
        - symbol (VARCHAR)
        - name (VARCHAR)
        - price_usd (NUMERIC)
        - change_1h/24h/7d_percent (NUMERIC)
        - volume_24h (BIGINT)
        - market_cap (BIGINT)
        - timestamps (TIMESTAMP)
        """,
    )

    # -------------------------------------------------------------------------
    # TASK DEPENDENCIES (DAG Flow)
    # -------------------------------------------------------------------------
    # Define execution order: Extract/Transform -> Load
    # The >> operator sets downstream dependencies
    
    fetch_coins >> store_coins

# =============================================================================
# END OF DAG DEFINITION
# =============================================================================