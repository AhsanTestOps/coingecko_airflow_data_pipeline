# 🪙 CoinGecko Airflow Data Engineering Pipeline

<div align="center">

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache%20Airflow-2.9.2-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![Podman](https://img.shields.io/badge/Podman-5.7.1-892CA0?style=for-the-badge&logo=podman&logoColor=white)
![CoinGecko](https://img.shields.io/badge/CoinGecko-API%20v3-8DC63F?style=for-the-badge)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**A production-ready, fully containerized ETL pipeline that automatically fetches real-time cryptocurrency market data from the CoinGecko API and loads it into PostgreSQL — orchestrated end-to-end with Apache Airflow.**

[Features](#-features) • [Architecture](#-architecture) • [Quick Start](#-quick-start) • [Schema](#-data-schema) • [Screenshots](#-screenshots)

</div>

---

## 📌 Project Overview

This project implements a complete **Data Engineering pipeline** for cryptocurrency market data:

- **Extract** — Fetches top 100 coins by market cap from the CoinGecko public API
- **Transform** — Cleans and structures price, volume, and market cap data
- **Load** — Persists records into a PostgreSQL database with full timestamps
- **Orchestrate** — Schedules and monitors daily runs via Apache Airflow
- **Containerize** — Runs entirely in Podman containers with zero local dependencies

> ✅ **Pipeline Status:** 2 successful DAG runs | Avg duration: 4 seconds | Both tasks green

---

## ✨ Features

| Feature | Details |
|---|---|
| 📊 **Real-time Data** | Top 100 cryptocurrencies from CoinGecko API |
| ⏰ **Automated Scheduling** | Daily ETL runs via Apache Airflow (`@daily`) |
| 🐳 **Fully Containerized** | Podman containers — no local Python setup needed |
| 🗄️ **PostgreSQL Storage** | Persistent structured storage with typed schema |
| 📈 **Rich Metrics** | Price (1h, 24h, 7d changes), volume, market cap |
| 🔄 **Fault Tolerant** | Automatic retries on failure (1 retry, 5 min delay) |
| 🧩 **Modular Design** | Separate ETL, DB, and DAG modules |
| 🔗 **Task Dependencies** | Airflow enforces fetch → store order |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    COINGECKO ETL PIPELINE                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌─────────────┐      ┌──────────────────┐      ┌─────────────┐   │
│   │  CoinGecko  │      │  Apache Airflow   │      │ PostgreSQL  │   │
│   │   API v3    │─────▶│  (Orchestrator)  │─────▶│  Database   │   │
│   │             │      │                  │      │             │   │
│   │  EXTRACT    │      │   TRANSFORM      │      │    LOAD     │   │
│   └─────────────┘      └──────────────────┘      └─────────────┘   │
│                                                                     │
│   Top 100 coins         DAG: @daily schedule      DB: coingecko    │
│   Real-time prices      Task 1 → Task 2           Table: top100    │
│   Market cap / vol      Retry on failure          Timestamped      │
│                                                                     │
├─────────────────────────────────────────────────────────────────────┤
│                    CONTAINER INFRASTRUCTURE                         │
│                                                                     │
│   ┌──────────────────────────┐   ┌──────────────────────────────┐  │
│   │  Podman: airflow         │   │  Podman: crypto-postgres     │  │
│   │  apache/airflow:2.9.2    │   │  postgres:15                 │  │
│   │  PORT: 8080              │   │  PORT: 5432                  │  │
│   └──────────────────────────┘   └──────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### DAG Workflow

```
  ┌─────────────────────────────────┐
  │   fetch_top100_from_coingecko   │
  │  ───────────────────────────── │
  │  • Call CoinGecko /markets API  │
  │  • Parse & clean JSON response  │
  │  • Save to CSV (intermediate)   │
  └────────────────┬────────────────┘
                   │  triggers on success
                   ▼
  ┌─────────────────────────────────┐
  │      store_to_postgresql        │
  │  ───────────────────────────── │
  │  • Read intermediate CSV        │
  │  • Connect to PostgreSQL        │
  │  • CREATE TABLE IF NOT EXISTS   │
  │  • INSERT 100 rows with types   │
  └─────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version |
|---|---|---|
| Language | Python | 3.12 |
| Orchestration | Apache Airflow | 2.9.2 |
| Database | PostgreSQL | 15 |
| Containerization | Podman | 5.7.1 |
| Data Source | CoinGecko API | v3 (free tier) |
| Key Libraries | pandas, psycopg2, requests | latest |

---

## 📁 Project Structure

```
coingecko-airflow-data-pipeline/
│
├── 📄 crypto_dag_airflow.py      # Airflow DAG — defines pipeline & schedule
├── 📄 crypto_etl.py              # Extract — fetches data from CoinGecko API
├── 📄 db.py                      # Load — inserts data into PostgreSQL
├── 📄 Dockerfile                 # Custom Airflow image with dependencies
├── 📄 docker-compose.yml         # Multi-container setup (alternative)
├── 📄 requirements.txt           # Python dependencies
├── 📄 coingecko_top100.csv       # Sample output data
└── 📄 README.md                  # You are here
```

---

## 🚀 Quick Start

### Prerequisites

- [Podman Desktop](https://podman.io/) (or Docker)
- WSL2 enabled (Windows only)
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/coingecko-airflow-data-pipeline.git
cd coingecko-airflow-data-pipeline
```

### 2. Start PostgreSQL Container

```bash
podman run -d \
  --name crypto-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=coingecko \
  -p 5432:5432 \
  postgres:15
```

### 3. Initialize Airflow Database

```bash
podman run --rm \
  -e AIRFLOW__CORE__EXECUTOR=LocalExecutor \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:1234@host.containers.internal:5432/coingecko" \
  -e AIRFLOW__CORE__LOAD_EXAMPLES=False \
  apache/airflow:2.9.2 \
  airflow db init
```

### 4. Create Admin User

```bash
podman run --rm \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:1234@host.containers.internal:5432/coingecko" \
  apache/airflow:2.9.2 \
  airflow users create \
    --username admin --password admin \
    --firstname Admin --lastname User \
    --role Admin --email admin@example.com
```

### 5. Start Airflow

```bash
podman run -d \
  --name airflow \
  -p 8080:8080 \
  -e AIRFLOW__CORE__EXECUTOR=LocalExecutor \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:1234@host.containers.internal:5432/coingecko" \
  -e AIRFLOW__CORE__LOAD_EXAMPLES=False \
  -e AIRFLOW__WEBSERVER__SECRET_KEY="mysecretkey123" \
  -v ./:/opt/airflow/dags \
  apache/airflow:2.9.2 \
  airflow standalone
```

### 6. Access the UI

```
URL:      http://localhost:8080
Username: admin
Password: admin
```

Find `crypto_coingecko_pipeline` → Toggle ON → Click ▶ Trigger

---

## 📊 Data Schema

### Table: `coingecko_top100`

| Column | Type | Description |
|---|---|---|
| `rank` | INT | Market cap ranking (1–100) |
| `symbol` | VARCHAR(10) | Ticker symbol (BTC, ETH...) |
| `name` | VARCHAR(100) | Full coin name |
| `price_usd` | NUMERIC | Current USD price |
| `change_1h_percent` | NUMERIC | Price change last 1 hour |
| `change_24h_percent` | NUMERIC | Price change last 24 hours |
| `change_7d_percent` | NUMERIC | Price change last 7 days |
| `volume_24h` | BIGINT | 24h trading volume (USD) |
| `market_cap` | BIGINT | Total market capitalization |
| `last_updated` | TIMESTAMP | CoinGecko last update time |
| `fetched_at_utc` | TIMESTAMP | Pipeline fetch timestamp |

### Sample Data

```
rank | symbol | name     | price_usd | change_24h | market_cap
-----|--------|----------|-----------|------------|------------------
1    | BTC    | Bitcoin  | 68828.51  | +3.3%      | 1,376,369,329,573
2    | ETH    | Ethereum | 2024.19   | +3.0%      |   244,421,763,448
3    | USDT   | Tether   | 0.9998    |  0.0%      |   183,534,966,357
4    | BNB    | BNB      | 636.92    | +2.4%      |     1,507,249,247
```

---

## ⚙️ Configuration

### Schedule Options

Edit `crypto_dag_airflow.py`:

```python
schedule_interval='@daily'    # once per day
schedule_interval='@hourly'   # once per hour
schedule_interval='@weekly'   # once per week
schedule_interval='0 9 * * *' # every day at 9AM UTC (cron)
```

### Environment Variables

| Variable | Default | Description |
|---|---|---|
| `POSTGRES_USER` | `postgres` | DB username |
| `POSTGRES_PASSWORD` | `1234` | DB password |
| `POSTGRES_DB` | `coingecko` | Database name |
| `AIRFLOW__CORE__EXECUTOR` | `LocalExecutor` | Airflow executor type |

---

## 📸 Screenshots

### Airflow DAG — 2 Successful Runs
> Both `fetch_top100_from_coingecko` and `store_to_postgresql` tasks completed successfully in under 5 seconds.

### Podman Containers Running
> `airflow` (PORT 8080) and `crypto-postgres` (PORT 5432) both running.

### Live CoinGecko Data
> Real-time market cap, price changes, and volume fetched directly from CoinGecko.

---

## 🧪 Verify Data in PostgreSQL

```bash
podman exec -it crypto-postgres psql -U postgres -d coingecko

# Inside psql:
SELECT rank, symbol, name, price_usd, change_24h_percent
FROM coingecko_top100
ORDER BY rank
LIMIT 10;
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/add-more-coins`
3. Commit your changes: `git commit -m 'feat: add historical data support'`
4. Push to the branch: `git push origin feature/add-more-coins`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Muhammad Ahsan**
- GitHub: [@YOUR_USERNAME](https://github.com/YOUR_USERNAME)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)

---

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) — free crypto market API
- [Apache Airflow](https://airflow.apache.org/) — workflow orchestration
- [Podman](https://podman.io/) — daemonless container engine

---

<div align="center">
⭐ Star this repo if it helped you learn data engineering!
</div>
