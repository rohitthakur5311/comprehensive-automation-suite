# Comprehensive Automation Suite

An integrated Python automation suite inspired by the supplied project specification.

## Included modules

- **File Organizer** — pattern matching, auto-categorization, duplicate detection and dry-run support.
- **Web Scraper** — HTML extraction, configurable user-agent/proxy rotation, rate limiting and robots.txt awareness.
- **Email Automation** — reusable templates, SMTP sending, campaign scheduling and dry-run mode.
- **System Monitor** — CPU, memory, disk and network metrics with threshold alerts and JSON/CSV reporting.
- **Task Scheduler** — cron-like schedules using `schedule` plus persistent JSON task definitions.
- **Tkinter GUI** — tabs for all modules, dashboard, logs and workflow execution.
- **Workflow Designer** — create ordered automation steps and execute them sequentially.
- **Exports** — CSV, JSON and XLSX.
- **Logging & configuration** — centralized settings and rotating application logs.

## Quick start

### 1. Create a virtual environment

Windows:
```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the GUI

```bash
python main.py
```

### 4. Run the CLI

```bash
python cli.py status
python cli.py organize --source ./data/sample_downloads --dry-run
python cli.py scrape --url https://example.com --selector "h1"
python cli.py monitor
python cli.py scheduler
```

## Configuration

Copy `.env.example` to `.env` and set SMTP values if email sending is required.

The main configuration is in `configs/config.json`. Never commit real SMTP passwords or proxy credentials.

## Safety notes

The scraper is intended for legitimate data collection. It uses a configurable request delay, honors `robots.txt` by default, and does not attempt CAPTCHA bypassing, authentication bypass, rate-limit circumvention, or other access-control evasion. Use only sources you are authorized to access.

## Project structure

```text
automation_suite/
├── main.py
├── cli.py
├── config.py
├── file_organizer/
├── web_scraper/
├── email_automation/
├── system_monitor/
├── task_scheduler/
├── gui/
├── utils/
├── logs/
├── templates/
├── configs/
├── tests/
├── docs/
├── data/
└── exports/
```

## Testing

```bash
python -m unittest discover -s tests -v
```
