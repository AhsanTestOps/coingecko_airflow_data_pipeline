# ==============================================================================
# CRYPTO ETL PIPELINE - DOCKERFILE
# ==============================================================================
#
# Description:
#   Container image for Apache Airflow with custom crypto ETL pipeline
#   Includes all dependencies for fetching CoinGecko data and storing to PostgreSQL
#
# Base Image: apache/airflow:2.8.0-python3.11
# Platform: linux/amd64
#
# Build Command:
#   podman build -t crypto-airflow .
#
# Run Command:
#   podman run -d -p 8080:8080 --name crypto-airflow crypto-airflow
#
# Author: Data Engineering Team
# Version: 1.0.0
# ==============================================================================

# -----------------------------------------------------------------------------
# STAGE 1: Base Image
# -----------------------------------------------------------------------------
# Use official Apache Airflow image with Python 3.11
# This image includes: Airflow core, PostgreSQL drivers, and common dependencies
FROM apache/airflow:2.8.0-python3.11

# -----------------------------------------------------------------------------
# STAGE 2: System Dependencies (as root)
# -----------------------------------------------------------------------------
# Switch to root user to install system-level packages
# Required for: PostgreSQL client libraries, build tools, etc.
USER root

# Update package lists and install system dependencies
# --no-install-recommends: Minimize image size by skipping optional packages
# Clean up apt cache to reduce final image size
RUN apt-get update && apt-get install -y --no-install-recommends \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# -----------------------------------------------------------------------------
# STAGE 3: Python Dependencies (as airflow user)
# -----------------------------------------------------------------------------
# Switch back to airflow user for security best practices
# Running as non-root prevents potential security vulnerabilities
USER airflow

# Copy requirements file first (enables Docker layer caching)
# If requirements.txt hasn't changed, this layer is cached
COPY requirements.txt .

# Install Python packages from requirements.txt
# --no-cache-dir: Don't store pip cache (reduces image size)
# Packages installed: requests, pandas, psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

# -----------------------------------------------------------------------------
# STAGE 4: Application Files
# -----------------------------------------------------------------------------
# Copy DAG and ETL scripts to Airflow's DAGs directory
# These files define the crypto ETL pipeline workflow

# Main Airflow DAG definition
COPY crypto_dag_airflow.py /opt/airflow/dags/

# ETL script: Fetches data from CoinGecko API
COPY crypto_etl.py /opt/airflow/dags/

# Database loader: Stores data to PostgreSQL
COPY db.py /opt/airflow/dags/

# -----------------------------------------------------------------------------
# STAGE 5: Working Directories
# -----------------------------------------------------------------------------
# Create directory for storing CSV output files
# This directory persists data between task runs
RUN mkdir -p /opt/airflow/data

# ==============================================================================
# END OF DOCKERFILE
# ==============================================================================