<div align="center">

# 🪙 CoinGecko Airflow Data Engineering Pipeline

<img src="https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Apache%20Airflow-2.9.2-017CEE?style=for-the-badge&logo=apacheairflow&logoColor=white"/>
<img src="https://img.shields.io/badge/PostgreSQL-15-4169E1?style=for-the-badge&logo=postgresql&logoColor=white"/>
<img src="https://img.shields.io/badge/Podman-5.7.1-892CA0?style=for-the-badge&logo=podman&logoColor=white"/>
<img src="https://img.shields.io/badge/CoinGecko-API%20v3-8DC63F?style=for-the-badge"/>
<img src="https://img.shields.io/badge/License-MIT-F7B731?style=for-the-badge"/>

<br/><br/>

> **A production-ready, fully containerized ETL pipeline that automatically fetches real-time cryptocurrency market data from the CoinGecko API, transforms it, and loads it into PostgreSQL — orchestrated end-to-end with Apache Airflow running inside Podman containers on Windows.**

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-AhsanTestOps-181717?style=flat-square&logo=github)](https://github.com/AhsanTestOps/coingecko_airflow_data_pipeline)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad%20Ahsan-0A66C2?style=flat-square&logo=linkedin)](https://www.linkedin.com/in/muhammad-ahsan-b8a643253)
[![Email](https://img.shields.io/badge/Email-mrahsanawan911@gmail.com-EA4335?style=flat-square&logo=gmail)](mailto:mrahsanawan911@gmail.com)

</div>

---

## 📌 Project Overview

This is a complete **end-to-end Data Engineering project** built from scratch on Windows using Podman containers. The pipeline runs automatically every day and performs a full ETL cycle:

| Step | Action | Tool |
|------|--------|------|
| **Extract** | Fetches top 100 coins by market cap | CoinGecko API v3 |
| **Transform** | Cleans, types, and structures price/volume/market cap | Python / Pandas |
| **Load** | Inserts 100 rows into PostgreSQL with timestamps | psycopg2 |
| **Orchestrate** | Schedules, monitors, and retries tasks | Apache Airflow |
| **Containerize** | Runs everything in isolated Podman containers | Podman Desktop |

> ✅ **Live Status:** 2 successful DAG runs | Avg duration: **4 seconds** | All tasks green ✅

---

## 📸 Live Screenshots

### 🌐 1. Data Source — CoinGecko Live Market Data
> Real-time top 100 cryptocurrency data source. Bitcoin at **$68,828.51** (+3.3%), Ethereum at **$2,024.19** (+3.0%), total crypto market cap at **$2.43 Trillion**. This is the exact data our pipeline fetches via the CoinGecko public API.

![CoinGecko Live Data](coingecko.JPG)

---

### 🐳 2. Podman Desktop — Both Containers Running
> Two containers running simultaneously:
> - **`airflow`** → `docker.io/apache/airflow:2.9.2` | PORT **8080** | Uptime: 36 minutes ✅
> - **`crypto-postgres`** → `docker.io/library/postgres:15` | PORT **5432** | Uptime: 1 hour ✅

![Podman Containers Running](podman.jpeg)

---

### ✈️ 3. Airflow UI — DAG Live and Active
> `crypto_coingecko_pipeline` DAG is **enabled and running**, scheduled `@daily`, last triggered on `2026-03-03 01:23:11 UTC`. Tagged with `crypto` and `etl`. Active: **1** | Running: **0** | Failed: **0**

![Airflow DAG Dashboard](airflow.jpeg)

---

### ✅ 4. Pipeline Execution — 2 Successful Runs
> Full DAG execution summary:
> - **Total Runs:** 2 | **Success Rate:** 100% ✅
> - **First Run:** `2026-03-03, 01:23:10 UTC`
> - **Last Run:** `2026-03-03, 01:23:12 UTC`
> - **Max Duration:** 5s | **Mean:** 4s | **Min:** 2s
> - Both tasks visible as green bars in the Gantt chart ✅

![Airflow Successful Pipeline](airflow_graph.jpeg)

---

## 🏗️ Architecture

```
┌──────────────────────────────────────────────────────────────────────────┐
│               COINGECKO AIRFLOW DATA ENGINEERING PIPELINE                │
│                    Windows 10/11 + Podman + WSL2                         │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌──────────────────┐    ┌───────────────────────┐   ┌──────────────┐  │
│   │  CoinGecko API   │    │    Apache Airflow      │   │  PostgreSQL  │  │
│   │      v3          │───▶│       2.9.2            │──▶│      15      │  │
│   │                  │    │                        │   │              │  │
│   │  /coins/markets  │    │  DAG: @daily           │   │  DB:         │  │
│   │  ?vs_currency=usd│    │  Executor: Local       │   │  coingecko   │  │
│   │  &per_page=100   │    │  Retries: 1 (5min)     │   │              │  │
│   │                  │    │  Task1 → Task2         │   │  Table:      │  │
│   │  $2.43T Market   │    │                        │   │  top100      │  │
│   │  Cap (live)      │    │  localhost:8080        │   │  :5432       │  │
│   └──────────────────┘    └───────────────────────┘   └──────────────┘  │
│                                                                          │
├──────────────────────────────────────────────────────────────────────────┤
│                        PODMAN CONTAINER LAYER                            │
│                                                                          │
│  ┌──────────────────────────────┐  ┌──────────────────────────────────┐  │
│  │  Container: airflow          │  │  Container: crypto-postgres       │  │
│  │  Image: airflow:2.9.2        │  │  Image: postgres:15               │  │
│  │  Port: 8080 → 8080           │  │  Port: 5432 → 5432               │  │
│  │  Volume: ./dags mounted      │  │  Env: POSTGRES_DB=coingecko      │  │
│  │  Status: ✅ RUNNING           │  │  Status: ✅ RUNNING               │  │
│  └──────────────────────────────┘  └──────────────────────────────────┘  │
│                                                                          │
│  Network: host.containers.internal (Podman WSL2 bridge)                  │
└──────────────────────────────────────────────────────────────────────────┘
```

### DAG Task Dependency Flow

```
  ┌──────────────────────────────────────────┐
  │       fetch_top100_from_coingecko        │   ← Task 1 (PythonOperator)
  │  ────────────────────────────────────    │
  │  • GET api.coingecko.com/api/v3/coins    │
  │  • Parse JSON response (100 coins)       │
  │  • Build structured DataFrame            │
  │  • Save CSV to /opt/airflow/dags/        │
  │                                          │
  │  ✅ Status: SUCCESS | avg 2 sec           │
  └──────────────────┬───────────────────────┘
                     │
                     │  ← triggers only on upstream SUCCESS
                     ▼
  ┌──────────────────────────────────────────┐
  │          store_to_postgresql             │   ← Task 2 (PythonOperator)
  │  ────────────────────────────────────    │
  │  • Read CSV from shared DAGs path        │
  │  • Connect to host.containers.internal   │
  │  • CREATE TABLE IF NOT EXISTS            │
  │  • INSERT 100 rows with typed columns    │
  │  • Auto-retry once on failure (5 min)    │
  │                                          │
  │  ✅ Status: SUCCESS | avg 2 sec           │
  └──────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology | Version | Purpose |
|-------|-----------|---------|---------|
| Language | Python | 3.12 | Core scripting & logic |
| Orchestration | Apache Airflow | 2.9.2 | Pipeline scheduling & monitoring |
| Database | PostgreSQL | 15 | Persistent structured storage |
| Containerization | Podman Desktop | 5.7.1 | Container runtime (Windows WSL2) |
| Data Source | CoinGecko API | v3 (free) | Real-time crypto market data |
| Data Processing | Pandas | 2.1.4 | DataFrame manipulation |
| DB Connector | psycopg2-binary | 2.9.9 | PostgreSQL Python driver |
| HTTP Client | Requests | 2.31.0 | REST API calls |

---

## 📁 Project Structure

```
coingecko_airflow_data_pipeline/
│
├── 📄 crypto_dag_airflow.py     # Airflow DAG — defines pipeline, schedule & dependencies
├── 📄 crypto_etl.py             # Extract: CoinGecko API → structured CSV
├── 📄 db.py                     # Load: CSV data → PostgreSQL table
├── 📄 Dockerfile                # Custom Airflow container image
├── 📄 docker-compose.yml        # Alternative multi-container orchestration
├── 📄 requirements.txt          # Python package dependencies
├── 📄 coingecko_top100.csv      # Sample pipeline output data
├── 🖼️ coingecko.JPG             # Screenshot: CoinGecko live market data
├── 🖼️ podman.jpeg               # Screenshot: Podman Desktop containers
├── 🖼️ airflow.jpeg              # Screenshot: Airflow DAG dashboard
├── 🖼️ airflow_graph.jpeg        # Screenshot: Successful pipeline runs
└── 📄 README.md                 # This file
```

---

## 🚀 Quick Start

### Prerequisites

- [Podman Desktop](https://podman.io/) installed with WSL2 backend
- Git

### Step 1 — Clone the Repository

```bash
git clone https://github.com/AhsanTestOps/coingecko_airflow_data_pipeline.git
cd coingecko_airflow_data_pipeline
```

### Step 2 — Start PostgreSQL

```bash
podman run -d \
  --name crypto-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=1234 \
  -e POSTGRES_DB=coingecko \
  -p 5432:5432 \
  postgres:15
```

### Step 3 — Initialize Airflow Database

```bash
podman run --rm \
  -e AIRFLOW__CORE__EXECUTOR=LocalExecutor \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:1234@host.containers.internal:5432/coingecko" \
  -e AIRFLOW__CORE__LOAD_EXAMPLES=False \
  apache/airflow:2.9.2 \
  airflow db init
```

### Step 4 — Create Admin User

```bash
podman run --rm \
  -e AIRFLOW__DATABASE__SQL_ALCHEMY_CONN="postgresql+psycopg2://postgres:1234@host.containers.internal:5432/coingecko" \
  apache/airflow:2.9.2 \
  airflow users create \
    --username admin --password admin \
    --firstname Admin --lastname User \
    --role Admin --email admin@example.com
```

### Step 5 — Launch Airflow

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

### Step 6 — Open Airflow UI

```
URL:       http://localhost:8080
Username:  admin
Password:  admin
```

**Find `crypto_coingecko_pipeline` → Toggle ON → Click ▶ Trigger DAG → Watch tasks turn green ✅**

---

## 📊 Data Schema

### Table: `coingecko_top100`

| Column | Type | Description |
|--------|------|-------------|
| `rank` | INT | Market cap ranking (1–100) |
| `symbol` | VARCHAR(10) | Ticker symbol (BTC, ETH, USDT...) |
| `name` | VARCHAR(100) | Full cryptocurrency name |
| `price_usd` | NUMERIC | Current price in USD |
| `change_1h_percent` | NUMERIC | Price change % — last 1 hour |
| `change_24h_percent` | NUMERIC | Price change % — last 24 hours |
| `change_7d_percent` | NUMERIC | Price change % — last 7 days |
| `volume_24h` | BIGINT | 24-hour trading volume (USD) |
| `market_cap` | BIGINT | Total market capitalization (USD) |
| `last_updated` | TIMESTAMP | CoinGecko's last data update |
| `fetched_at_utc` | TIMESTAMP | Pipeline fetch timestamp (UTC) |

### Sample Output

```
rank | symbol | name      | price_usd  | change_24h_% | market_cap
-----|--------|-----------|------------|--------------|--------------------
1    | BTC    | Bitcoin   | 68828.51   | +3.3         | 1,376,369,329,573
2    | ETH    | Ethereum  | 2024.19    | +3.0         |   244,421,763,448
3    | USDT   | Tether    | 0.9998     |  0.0         |   183,534,966,357
4    | BNB    | BNB       | 636.92     | +2.4         |     1,507,249,247
5    | XRP    | XRP       | 0.62       | +2.89        |       107,845,192
```

---

## ⚙️ Configuration

### Change Pipeline Schedule

Edit `crypto_dag_airflow.py`:

```python
schedule_interval='@hourly'     # every hour
schedule_interval='@daily'      # every day ← current
schedule_interval='@weekly'     # every week
schedule_interval='0 8 * * *'   # daily at 8AM UTC (cron syntax)
```

### Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `POSTGRES_USER` | `postgres` | PostgreSQL username |
| `POSTGRES_PASSWORD` | `1234` | PostgreSQL password |
| `POSTGRES_DB` | `coingecko` | Target database name |
| `AIRFLOW__CORE__EXECUTOR` | `LocalExecutor` | Airflow task executor type |
| `AIRFLOW__WEBSERVER__SECRET_KEY` | `mysecretkey123` | Webserver security key |

---

## 🔍 Verify Data in PostgreSQL

```bash
# Connect to the running database
podman exec -it crypto-postgres psql -U postgres -d coingecko

# Count total rows
SELECT COUNT(*) FROM coingecko_top100;

# View top 10 coins by rank
SELECT rank, symbol, name, price_usd, change_24h_percent
FROM coingecko_top100
ORDER BY rank
LIMIT 10;

# Check when pipeline last ran
SELECT MAX(fetched_at_utc) AS last_pipeline_run
FROM coingecko_top100;
```

---

## 🐳 Useful Container Commands

```bash
# Check both containers are running
podman ps

# Follow Airflow logs live
podman logs -f airflow

# Stop everything
podman stop airflow crypto-postgres

# Restart everything
podman start crypto-postgres && podman start airflow
```

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/add-historical-data`
3. Commit: `git commit -m 'feat: add 30-day historical data support'`
4. Push: `git push origin feature/add-historical-data`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — free to use, modify, and distribute.

---

## 👤 Author

<div align="center">

### Muhammad Ahsan
*Data Engineer | Python Developer*

<br/>

[![GitHub](https://img.shields.io/badge/GitHub-AhsanTestOps-181717?style=for-the-badge&logo=github)](https://github.com/AhsanTestOps/coingecko_airflow_data_pipeline)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Muhammad%20Ahsan-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/muhammad-ahsan-b8a643253)
[![Email](https://img.shields.io/badge/Gmail-mrahsanawan911@gmail.com-EA4335?style=for-the-badge&logo=gmail)](mailto:mrahsanawan911@gmail.com)

</div>

---

## 🙏 Acknowledgments

- [CoinGecko](https://www.coingecko.com/) — free public cryptocurrency API (18,638+ coins tracked)
- [Apache Airflow](https://airflow.apache.org/) — open-source workflow orchestration platform
- [Podman](https://podman.io/) — daemonless, rootless, secure container engine

---

<div align="center">

**⭐ Star this repo if it helped you learn data engineering!**

*Built with ❤️ by [Muhammad Ahsan](https://github.com/AhsanTestOps) | Rawalpindi, Pakistan*

</div>
