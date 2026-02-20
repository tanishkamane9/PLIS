# PLIS – Production Log Insight System

PLIS is a CLI-based log analysis and observability tool that processes structured application logs, computes derived metrics, stores daily summaries in SQLite, and triggers threshold-based alerts.

It is designed as a lightweight MVP observability system with clean architecture and modular components.

---

## 🚀 Features

- CLI-based log ingestion
- Structured log analysis
- Daily summary storage in SQLite
- Derived metrics calculation (error rate, warning rate)
- Threshold-based alert engine
- JSON export of analysis results
- Idempotent daily processing (safe to rerun)

---

## 🏗 Architecture

PLIS follows a layered architecture:
# PLIS – Production Log Insight System

PLIS is a CLI-based log analysis and observability tool that processes structured application logs, computes derived metrics, stores daily summaries in SQLite, and triggers threshold-based alerts.

It is designed as a lightweight MVP observability system with clean architecture and modular components.

---

## 🚀 Features

- CLI-based log ingestion
- Structured log analysis
- Daily summary storage in SQLite
- Derived metrics calculation (error rate, warning rate)
- Threshold-based alert engine
- JSON export of analysis results
- Idempotent daily processing (safe to rerun)

---

## 🏗 Architecture

PLIS follows a layered architecture:

### Project Structure


plis/
│
├── analyzer/
│ └── analyzer.py
│
├── storage/
│ ├── db.py
│ └── models.py
│
├── logs/
│ └── sample.log
│
├── data/
│ └── plis.db
│
├── output/
│
├── main.py
├── schema.sql
├── requirements.txt
└── README.md


---

## 🧾 Supported Log Format

PLIS expects logs in the following structured format:


YYYY-MM-DD HH:MM:SS LEVEL message


Example:


2026-02-20 09:15:23 INFO User login successful
2026-02-20 09:16:11 ERROR Database timeout


---

## ⚙️ Installation

PLIS uses only Python standard library.

Ensure you have:


Python 3.9+


Clone the repository:


git clone https://github.com/
tanishkamane9/PLIS.git
cd PLIS


---

## ▶️ Usage

Run analysis:


python main.py --file logs/sample.log --env prod --app payment-service


Arguments:

- `--file` → Path to log file (required)
- `--env` → Environment (default: prod)
- `--app` → Application name (default: default-app)
- in place of 'logs/sample.log' add your log file path (**required)
- after env add environment like (prod,dev,staging) i.e. production ,development and staging
- after app add name of your app

---

## 📊 What PLIS Computes

For each log file, PLIS calculates:

- Total logs processed
- INFO count
- WARNING count
- ERROR count
- Most frequent error message
- Peak error hour
- Error rate
- Warning rate

---

## 🚨 Alert Logic

If:


error_rate > 20%


PLIS:

- Triggers a console alert
- Stores alert record in database

---

## 💾 Database Design

PLIS uses SQLite for persistence.

Tables:

- `applications`
- `daily_log_summary`
- `metrics_daily`
- `alerts`

Daily summaries are unique per application per date.

---

## 📤 JSON Export

Each run generates a JSON file in:


output/<app_name>_<date>.json


This allows integration with other systems.

---

## 🎯 MVP Scope

This version includes:

- CLI ingestion
- Structured parsing
- Persistent storage
- Metrics calculation
- Threshold alerts

Future enhancements may include:

- Web dashboard
- Multi-format log support
- Webhook integrations
- Trend analysis
- Distributed ingestion

---

## 📌 Version

Current Version: `v1.0.0-mvp`

---

